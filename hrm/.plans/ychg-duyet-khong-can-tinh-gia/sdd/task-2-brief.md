# Task 2 — `TempNoPriceResolver`: phân loại & resolve giá (TH1/TH2)

Repo: `hrm-api` (Laravel 8 / PHP 7.4, `Modules/MasterData`). Branch `develop`.

## Global Constraints
- Dữ liệu nhạy cảm (giá vốn/giá nhập) gate server-side. Service này CHỈ resolve giá để ghi khi duyệt (không phải màn xem) — không cần gate quyền ở đây; gate PTKD nằm ở route/ptkdApprove.
- TH1 CHỈ hợp lệ khi giá nhập = 0 **VÀ** giá bán = 0 **tường minh** (null/thiếu dòng = KHÔNG đủ điều kiện).
- TH2 quy đổi VND bằng tỷ giá **hiện tại** (KHÔNG dùng tỷ giá đóng băng trên báo giá). Số en-US.

## Files
- Create: `Modules/MasterData/Services/PriceCalculation/TempNoPriceResolver.php`
- Test: `Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php` (TẠO MỚI file này — mirror scaffolding của `Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php`: `DatabaseTransactions`, trait `Concerns\ActsAsProductUser` nếu cần dựng hàng×công ty + `product_company_coefficients`). Task 3 & 4 sẽ THÊM test vào chính file này.

## Interfaces — Produces (Task 4 phụ thuộc)
```php
// null = KHÔNG đủ điều kiện "duyệt không cần tính giá"
// ['case' => 'won_bid'|'zero', 'cost' => float, 'sale' => float, 'unit_id' => int]
public function resolve(int $productId, int $companyId): ?array
```
- `cost` = giá nhập (đã quy đổi VND), `sale` = giá bán (đã quy đổi VND), `unit_id` = ĐVT gốc của giá (ĐVT dòng báo giá cho TH2; ĐVT gốc hàng cho TH1).

## Recon BẮT BUỘC trước khi code (xác minh tên cột/chữ ký thực tế — đừng tin trí nhớ)
1. `Modules/Assign/Services/QuotationService.php` — hàm `resolveCurrentExchangeRate(...)` (~dòng 1428): xác nhận chữ ký (nhận gì — `Quotation`? currency_id?), trả `float`, VND/none trả `1.0`. Dùng ĐÚNG như nó yêu cầu.
2. `Quotation` entity — hằng `STATUS_TRUNG_THAU` (kỳ vọng `= 7`). Xác nhận.
3. Bảng `quotation_product_prices`: cột `erp_product_id` (join `products.id`), `quotation_id`, `estimated_price` (giá nhập/cost), `quoted_price` (giá bán, decimal(15,2) theo loại tiền báo giá). **XÁC MINH tên cột ĐVT trên bảng này** (vd `unit_id`/`product_unit_id`?) — đây là điểm cần pin. Nếu không có cột ĐVT trên dòng báo giá → fallback ĐVT gốc của hàng và GHI RÕ trong report.
4. Join lấy loại tiền để truyền vào `resolveCurrentExchangeRate`: xác minh `quotations` có `currency_id` hay tương đương.
5. TH1 — điểm đọc giá hiện tại của hàng tại công ty (PIN và ghi report):
   - giá nhập (cost): `product_company_units.cost_price` của ĐVT gốc hàng tại `company_id`.
   - giá bán: giá hiệu lực **loại 1 (Bán lẻ)** trên `product_unit_prices` của ĐVT gốc tại `company_id`.
   - "0 tường minh" = có bản ghi với giá trị `0` (phân biệt với NULL / không có bản ghi → KHÔNG hợp lệ).

## Steps (TDD)

**Step 1 — Viết test** (tạo file, 6 ca):
```php
public function test_resolve_won_bid_vnd(): void {
    // quotation STATUS_TRUNG_THAU, qpp.estimated_price=100, quoted_price=150, tiền=VND
    // => ['case'=>'won_bid','cost'=>100.0,'sale'=>150.0,'unit_id'=>...]
}
public function test_resolve_won_bid_foreign_currency_multiplies_rate(): void {
    // currency rate hiện tại=25000, estimated=2, quoted=3 => cost=50000.0, sale=75000.0
}
public function test_resolve_won_bid_picks_latest_quotation(): void {
    // nhiều báo giá trúng thầu cho cùng product => lấy quotations.id lớn nhất
}
public function test_resolve_zero_when_explicit_zero_prices(): void {
    // cost_price=0 explicit + retail price row=0 explicit, không báo giá trúng thầu
    // => ['case'=>'zero','cost'=>0.0,'sale'=>0.0,'unit_id'=>...]
}
public function test_resolve_null_when_price_missing(): void {
    // cost null / không có dòng giá / không báo giá trúng thầu => assertNull
}
public function test_resolve_null_when_no_won_bid_and_nonzero(): void {
    // có báo giá nhưng status != 7 và giá KHÔNG phải 0 tường minh => assertNull
}
```

**Step 2 — Chạy test, xác nhận FAIL** (class chưa tồn tại).
`php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php`

**Step 3 — Implement `resolve()`**:
- **TH2 trước**: query `quotation_product_prices qpp` join `quotations q on q.id=qpp.quotation_id` where `qpp.erp_product_id=$productId` AND `q.status=Quotation::STATUS_TRUNG_THAU` AND `qpp.estimated_price IS NOT NULL` AND `qpp.quoted_price IS NOT NULL`, `order by q.id desc limit 1`. Nếu có: `rate = resolveCurrentExchangeRate(...)`; `cost=estimated_price*rate`, `sale=quoted_price*rate`, `unit_id`=ĐVT dòng báo giá (hoặc fallback ĐVT gốc). `case='won_bid'`.
- **TH1**: đọc cost_price (ĐVT gốc) + giá bán lẻ loại 1 tại company. Chỉ hợp lệ khi CẢ HAI = 0 tường minh. `case='zero'`, cost=0, sale=0, unit_id=ĐVT gốc.
- Ngược lại trả `null`.
- Cast số về `float`.

**Step 4 — Chạy test, xác nhận PASS.**

**Step 5 — Commit** (`develop`):
`feat(ychg): TempNoPriceResolver classifies TH1/TH2 + VND conversion`
Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Full report vào file report. Nêu RÕ: tên cột ĐVT thực tế trên `quotation_product_prices` (đã pin), chữ ký `resolveCurrentExchangeRate`, điểm đọc giá TH1 đã pin, test command+output, concerns. Trả về CHỈ status + commit + 1-dòng test + concerns. KHÔNG dispatch subagent.

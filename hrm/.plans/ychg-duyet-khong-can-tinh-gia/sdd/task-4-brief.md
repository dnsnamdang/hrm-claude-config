# Task 4 — Integration `ptkdApprove`: validate + ghi giá + promote + đóng phiếu

Repo: `hrm-api` (Laravel 8 / PHP 7.4, `Modules/MasterData`). Branch `develop`.

## Global Constraints
- **Atomic**: toàn bộ đổi trạng thái + ghi giá của một lần Duyệt phiếu phải nằm TRỌN trong transaction của `ptkdApprove`. Promote một phần rồi lỗi = cấm (rollback sạch).
- Ghi giá danh mục khi duyệt KHÔNG gate quyền giá vốn (đây là hành vi ghi lúc duyệt, không phải màn xem); gate PTKD đã ở route.
- TH2 ngoại tệ đã quy đổi VND ở resolver (Task 2) — T4 dùng `cost`/`sale` resolver trả, KHÔNG nhân lại.
- Đồng giá cả 6 loại giá bán = `sale` (ghi đè auto-compute TMĐT loại 6). Số en-US.
- Không đổi luồng dòng Đồng ý (7→2 đi XNK) và Từ chối (8).

## Đã có từ Task 1/2/3
- `ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE = 9`, `STATUS_TRADING = 3`, `PRICING_FLOW_STATUSES=[2,5]`.
- `TempNoPriceResolver::resolve(int $productId,int $companyId): ?array` → `null` | `['case'=>'won_bid'|'zero','cost'=>float,'sale'=>float,'unit_id'=>int]`. (TH1/TH2 + quy đổi VND đã xong.)
- Endpoint `approve-no-price` set dòng = 9 (Task 3).

## Files
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php` — `ptkdApprove()` (~591-700); đặc biệt các site chỉ xử lý `[7]`:
  - `:648` promote/move on Duyệt phiếu (hiện chỉ `[7]`→WAITING_PRICE(2)); dòng **9 phải → TRADING(3)**, KHÔNG qua WAITING_PRICE.
  - `:684` revert (7 only) — cân nhắc 9.
- Test: THÊM vào `Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php`.

## Chữ ký hiện có (recon — xác nhận lại)
- `ptkdApprove(int $id, array $input): void` (~591): blocks nếu còn dòng status===6; partition nhóm toàn-từ-chối→STATUS_CANCELLED; resolve XNK; nhóm→WAITING_XNK(5); phiếu→ASKING(10); `moveProducts(productIds,companyId,[7],2,me,...)`; `markGroupClosed`; `refreshHead`.
- `moveProducts(array $productIds,int $companyId,array $from,int $to,$me,?string $requestCode=null)` (~813).
- `refreshHead(...)` (~796) → phiếu `STATUS_PRICED`(4) | `STATUS_NO_PRICE`(9-phiếu) khi mọi nhóm đã đóng. **LƯU Ý: `9` ở ĐÂY là status PHIẾU (price_asking_requests.status), KHÁC status DÒNG `9`** — đừng lẫn.
- `markGroupClosed(...)` (~765), `log(...)` (~825).
- `ProductPriceWriter::apply(int $productId,int $productUnitId,int $companyId,array $resolved,float $cost,?string $reason,int $by): void` (~31) + `resolvePrices(array $prices,int $companyId): array` (~66, loại 6 auto trừ khi cờ is_manual). `ProductPriceSetWriter::ensureProductSet(int $productId,int $companyId,int $by)`.
- `PriceCalculateFinalizer::promoteProducts()` (~256): khuôn promote — `trackStatus` wrap, cập nhật pcc `PRICING_FLOW_STATUSES`→`STATUS_TRADING(3)`, rồi `ensureProductSet`. **Mirror khuôn này cho 9→3.**

## Interfaces — Produces
- `ptkdApprove` xử lý trọn dòng `9` trong cùng transaction: validate → ghi giá → promote 9→3 → đóng nhóm/phiếu. Không thêm public method mới bắt buộc (có thể tách private helper `promoteNoPriceLine(...)` nếu gọn hơn).

## Steps (TDD)

**Step 1 — Viết test** (end-to-end: dựng phiếu Chờ PTKD, set trạng thái dòng qua endpoint Task 3, rồi `POST {id}/approve`):
```php
public function test_ptkd_approve_promotes_th1_zero(): void {
    // dòng giá 0 => set 9 => Duyệt phiếu => pcc.status=3; cost_price=0; cả 6 loại giá bán=0
}
public function test_ptkd_approve_promotes_th2_writes_all_six_prices_flat(): void {
    // TH2 VND: cost_price=estimated; cả 6 loại giá bán = quoted (TMĐT loại 6 KHÔNG tự nhân hệ số)
}
public function test_ptkd_approve_th2_foreign_currency(): void {
    // giá ghi = resolver trả (đã ×rate); khẳng định giá VND đúng
}
public function test_ptkd_approve_blocks_ineligible_no_price_line(): void {
    // dòng set 9 nhưng resolve()=null => 422 key 'temp_products', message chứa mã hàng; KHÔNG dòng nào bị promote (rollback)
}
public function test_parent_no_price_child_normal_route_independently(): void {
    // Cha=9 => promote 3; Con=Đồng ý(7) => đi XNK (status 2), độc lập
}
public function test_request_all_no_price_closes_priced(): void {
    // phiếu toàn dòng 9 (±dòng 8) => phiếu đóng STATUS_PRICED(4)
}
public function test_request_mixed_goes_asking_but_promotes_no_price_now(): void {
    // có dòng Đồng ý(1/7) => phiếu STATUS_ASKING(10); dòng 9 vẫn promote 3 NGAY
}
public function test_promote_is_atomic_on_failure(): void {
    // ép resolve lỗi/null giữa chừng => không dòng nào đổi trạng thái (rollback)
}
```

**Step 2 — Chạy test, xác nhận FAIL.**

**Step 3 — Implement** trong transaction của `ptkdApprove`, sau khi gom `$statuses` (các dòng Cha+Con và trạng thái), TRƯỚC phần XNK/moveProducts:
- Gom tập id dòng đang `9`.
- **Validate**: mỗi id `9` → `resolve(id,companyId)`. Dòng trả `null` → gom `$invalid` (kèm mã hàng, query `products.code`). Nếu `$invalid` không rỗng → `throw \Illuminate\Validation\ValidationException::withMessages(['temp_products' => ['<mã1>, <mã2>: chưa đủ điều kiện duyệt không cần tính giá']])`. (Ném TRƯỚC khi ghi gì → transaction rollback sạch.)
- **Ghi giá + promote** mỗi dòng `9` hợp lệ:
  - Dựng mảng 6 loại giá bán phẳng = `sale`. Để "đồng giá" (kể cả TMĐT loại 6), KHÔNG để `resolvePrices` auto-nhân hệ số loại 6: truyền đủ 6 loại với giá = `sale` và set cờ manual cho loại 6 (xem cách `resolvePrices`/`apply` nhận cờ is_manual_price_online hoặc tương đương). Nếu cơ chế cờ không đủ, ghi thẳng qua `writePrices`. Mục tiêu assert được: cả 6 loại = `sale`.
  - Áp giá cho ĐVT gốc (`unit_id` từ resolver) + `cost` qua `ProductPriceWriter::apply(...)`. ĐVT phụ dẫn theo bộ giá chuẩn (`ensureProductSet`).
  - Promote: mirror `promoteProducts` — `trackStatus(companyId,[id], fn()=> update pcc 9→STATUS_TRADING(3))` + `ensureProductSet(id,companyId,me)`.
  - Log 1 dòng lịch sử (type mới ví dụ `temp_approve_no_price`) qua `log(...)`.
- **Nhóm & phiếu**: dòng `9` KHÔNG đi `moveProducts(7→2)`. Nhóm mà sau xử lý mọi dòng đã `3`/`8` (không còn dòng cần XNK) → đóng. Dùng lại `markGroupClosed`/`refreshHead` để phiếu về `STATUS_PRICED(4)` khi KHÔNG còn nhóm `WAITING_XNK`; còn nhóm thường (có dòng 1/7) → giữ `STATUS_ASKING(10)` như cũ. Dòng 7 vẫn move 7→2 như hiện tại.

**Step 4 — Audit hạ nguồn "status 3 phải kèm Phiếu tính giá"** (Review Focus): grep join `price_calculate*` / đồng bộ ERP / lập HĐ xem có coi hàng `3` bắt buộc có một `price_calculate`/Phiếu tính giá không. Nếu có, bổ sung guard hoặc đảm bảo dòng 9→3 không vỡ các màn đó. Ghi kết quả vào report.

**Step 5 — Chạy test mới, xác nhận PASS.**
`php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php`

**Step 6 — Chạy lại test cũ** `php artisan test Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php` — luồng Đồng ý/Từ chối không vỡ.

**Step 7 — Commit** (`develop`):
`feat(ychg): ptkdApprove validates+writes price+promotes no-price lines (3), closes request`
Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Full report vào report file. Nêu: cách ép đồng giá 6 loại (ghi đè TMĐT), cơ chế promote/atomic, kết quả audit hạ nguồn, test command+output (mới+cũ), concerns. Trả về CHỈ status + commit + 1-dòng test + concerns. KHÔNG dispatch subagent.

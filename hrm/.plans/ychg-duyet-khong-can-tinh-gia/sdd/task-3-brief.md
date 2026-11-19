# Task 3 — Endpoint set trạng thái `9` + gate nhận `9` + cờ FE

Repo: `hrm-api` (Laravel 8 / PHP 7.4, `Modules/MasterData`). Branch `develop`.

## Global Constraints
- Quyền dùng chung "PTKD duyệt yêu cầu hỏi giá" + middleware `dueConfig:Duyệt hàng tạm`. KHÔNG thêm quyền, KHÔNG seed.
- Không đổi luồng dòng Đồng ý (1/7) và Từ chối (8). Endpoint này KHÔNG validate/ghi giá (việc đó dồn về `ptkdApprove` ở Task 4).
- Dữ liệu nhạy cảm gate server-side.

## Đã có từ Task 1 (dùng được ngay)
- `ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE = 9`; `TEMP_STATUSES=[6,7,8,9]`; `isTemp(9)===true`.

## Files
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php` — thêm `tempApproveNoPrice()`; xử lý reopen tại ~dòng 546.
- Modify: `Modules/MasterData/Http/Controllers/V1/PriceCalculation/PriceAskingRequestController.php` — action mới (cạnh `tempApprove` dòng ~156).
- Modify: `Modules/MasterData/Routes/api.php` — route mới trong group temp-products (~dòng 416-423).
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestService.php` — `tempForm()` thêm cờ `can_approve_no_price` (~dòng 553-562).
- Modify: `Modules/MasterData/Services/Product/TempProductService.php:152` — edit reset 7/8→6: quyết định 9 có reset không (xem dưới).
- Test: THÊM vào `Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php` (file do Task 2 tạo).

## Chữ ký hiện có (recon đã pin — xác nhận lại nếu nghi ngờ)
- `assertTempGate(int $id, int $productId, array $statuses, bool $lock=false): array` → trả `[$request,$line,(int)$status]`; yêu cầu phiếu `status==STATUS_WAITING_PTKD` và `$status ∈ $statuses`.
- `setTempStatus($request, int $productId, int $to, ?string $action=null, ?string $note=null)`.
- `tempApprove(int $id,int $productId,array $input)` (~529) → set 7; `tempReject`→8; `tempSave`. Tất cả truyền `ProductCompany::TEMP_STATUSES` vào gate → nay đã gồm 9 nên reopen từ 9 hợp lệ.
- `tempForm(int $id,int $productId):array` trả `can_save/can_approve/can_reject` = `$open` = (phiếu WAITING_PTKD && isTemp(status)).

## Interfaces — Produces (Task 4, T5, T6 phụ thuộc)
```php
public function tempApproveNoPrice(int $id, int $productId): int   // trả về 9
```
- Route: `POST /api/v1/master-data/price-asking-requests/{id}/temp-products/{product}/approve-no-price`.
- `tempForm` meta thêm key `can_approve_no_price` (bool).

## Steps (TDD)

**Step 1 — Viết test** (thêm vào file test của Task 2):
```php
public function test_approve_no_price_sets_status_9(): void {
    // actAs PTKD; POST .../temp-products/{pid}/approve-no-price => 200, company_status=9; pcc.status=9
}
public function test_can_reopen_from_9_to_approve(): void {
    // pcc=9 => POST .../approve (tempApprove) => 200, status=7  (đổi ý được)
}
public function test_approve_no_price_gate(): void {
    // không phải PTKD => 403; dòng không thuộc phiếu => 404; phiếu không ở Chờ PTKD duyệt => 409 (hoặc mã assertTempGate dùng)
}
public function test_temp_form_exposes_can_approve_no_price(): void {
    // phiếu Chờ PTKD + dòng tạm => can_approve_no_price=true
}
```
(Xem `PriceAskingTempProductTest.php` để mirror cách actAs(company,[perms]), PTKD='PTKD duyệt yêu cầu hỏi giá', mock PriceAskingNotifier + CmcS3Helper, URL base '/api/v1/master-data/price-asking-requests'.)

**Step 2 — Chạy test, xác nhận FAIL.**

**Step 3 — Implement**:
- `tempApproveNoPrice($id,$productId)`: `DB::transaction` → `[$request] = assertTempGate($id,$productId, ProductCompany::TEMP_STATUSES, true)` → `setTempStatus($request,$productId, ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE, 'approved', 'Duyệt không cần tính giá')` → return `9`. KHÔNG validate/ghi giá ở đây.
- Controller: method `tempApproveNoPrice($id,$product)` gọi writer, trả `responseJson('Đã ghi nhận duyệt không cần tính giá', 200, ['product_id'=>(int)$product,'company_status'=>$status])`.
- Route: thêm `POST .../temp-products/{product}/approve-no-price` trong ĐÚNG group đã có gate `checkPermission:PTKD duyệt yêu cầu hỏi giá` + `middleware('dueConfig:Duyệt hàng tạm')` (giống route `approve`/`reject`).
- `tempForm`: thêm `'can_approve_no_price' => $open`.
- **Reopen (dòng ~546) + TempProductService:152**: hiện chỉ xử lý 7 (và 7/8). Vì gate nay nhận 9, PTKD mở lại dòng 9 rồi bấm Đồng ý/Không duyệt phải chạy được. Kiểm tra logic reopen/reset: nếu có nhánh riêng "nếu đang 7 thì …" cần thêm 9 song song (để dòng 9 khi sửa/đổi ý không bị kẹt). Nếu `TempProductService:152` reset 7/8→6 khi "Lưu" (edit), cân nhắc: dòng 9 khi PTKD bấm "Lưu" (tempSave) có nên về 6 không? QUYẾT ĐỊNH: để nhất quán với 7, khi tempSave trên dòng đang 9 thì reset về 6 (hàng tạm chờ) — vì "Lưu" nghĩa là sửa lại thông tin, phải duyệt lại. Ghi rõ quyết định trong report. (Nếu phát hiện khác biệt khiến quyết định này sai, nêu concern.)

**Step 4 — Chạy test, xác nhận PASS.**

**Step 5 — Chạy lại test cũ** `php artisan test Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php` — đảm bảo luồng Đồng ý/Từ chối/Lưu không vỡ.

**Step 6 — Commit** (`develop`):
`feat(ychg): per-line approve-no-price endpoint sets status 9 + reopen`
Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Full report vào report file. Nêu: quyết định reopen/reset cho dòng 9, các dòng code đã sửa, test command+output (cả test mới và test cũ), concerns. Trả về CHỈ status + commit + 1-dòng test + concerns. KHÔNG dispatch subagent.

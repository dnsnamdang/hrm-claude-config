# Task P2-7 Brief — BorrowSellService::store() (orchestrator tạo phiếu xuất bán hàng mượn)

> **ĐỌC FILE NÀY TRƯỚC — đây là requirements của bạn, giá trị exact dùng verbatim.**
> Đây là task orchestrator của Phase 2 feature `xuat-ban-hang-muon` (HRM, nhánh `gop_db`, DB gộp `erp_hrm_check`).
> Toàn bộ giao tiếp tiếng Việt. PHP 7.4 / Laravel 8. Namespace `Modules\Finance`.

## Bối cảnh 1 dòng

Phase 1 đã tạo **Yêu cầu xuất bán hàng mượn** (`BorrowSellRequest`, prefix `PXBHM-YC`). Task này = **lập phiếu xuất bán thực tế** (`BorrowSell`, prefix `PXBHM-`) từ 1 yêu cầu đã ở trạng thái "Chờ kế toán kho" (status=2). Đây là bước "Kế toán kho duyệt & xuất": tạo header + copy SP/detail, trừ kho atomic, hạch toán đầy đủ, rồi set yêu cầu cha sang DA_DUYET.

Các service posting (hạch toán) **ĐÃ TỒN TẠI** từ task T5/T6 — task này CHỈ orchestrate + viết code mới cho: tạo header, copy products/details, updateWarehouse, approve parent. **KHÔNG viết lại logic hạch toán.**

## File

- **Create:** `Modules/Finance/Services/BorrowSell/BorrowSellService.php`
- **Create test:** `Modules/Finance/Tests/Feature/BorrowSellStoreTest.php`
- **KHÔNG sửa:** `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php` (task khác đang sở hữu; chỉ GỌI public methods của nó).

## Tài liệu tham chiếu (được phép đọc)

- `/private/tmp/claude-501/-Users-nguyentrancu-DEV-code-ERP-HRM/f314a4a6-c7f6-44cf-99db-bad66dfea798/scratchpad/t7-investigation.md` — chứa verbatim ERP `store()`/`updateWarehouse()`/`generateCode()`, Phase 1 patterns, calculator, consts, payload shape. **Đọc để nắm ERP gốc.**
- `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php` (Phase 1) — pattern để MIRROR: dùng `DB::transaction(closure)`, throw `ValidationException::withMessages([...])`, code tạm → save → generateCode → sync children → validate hasChange. Chứa `computeAmounts()`, `returningQty()` để copy.
- `Modules/Finance/Support/BorrowSellRequestCalculator.php` — REUSE `availableSellQty` + `isQtyExceeded` (đường dẫn thật: tìm class `BorrowSellRequestCalculator` trong `Modules/Finance`).

## Interfaces bạn TIÊU THỤ (đã tồn tại — chỉ gọi, KHÔNG sửa)

### BorrowSellPostingService (public methods)
```php
namespace Modules\Finance\Services\BorrowSell;
class BorrowSellPostingService {
    // Hạch toán chính (giá vốn/chiết khấu/thưởng...). Tự mở DB::transaction, tự ghi account_details.
    public function postAccounting(BorrowSell $bs): array;              // trả [bool $ok, string $err]
    // Hạch toán chi phí vận chuyển (6427/3351). Tự mở DB::transaction. No-op nếu không có delivery trip.
    public function postDeliveryTripAccounting(BorrowSell $bs): array;  // trả [bool $ok, string $err]
    // (getDataAccounting chỉ build, không cần gọi ở đây)
}
```
Resolve qua `app(BorrowSellPostingService::class)`.

### BorrowSell entity (`Modules\Finance\Entities\BorrowSell\BorrowSell`)
```php
$table='borrow_sells'; $guarded=[];
const PREFIX='PXBHM'; const STATUS_DEFAULT=1;
const CONTRACT_FIRM='App\Model\Sale\Firm\Contract\FirmContract';
const CONTRACT_WR_SERVICE='App\Model\Customers\WrServiceContract';
// Relations: products(hasMany BorrowSellProduct parent_id), tabs(BorrowSellTab parent_id),
//            borrowSellRequest(belongsTo)
// generateCode() STATIC dùng max('id')+1 — KHÔNG DÙNG (Ruling T7-2, có race).
```
Child entities (`$guarded=[]`, FK `parent_id`): `BorrowSellProduct`, `BorrowSellProductDetail`, `BorrowSellTab`, `BorrowSellTabProduct`, `BorrowSellTabProductDetail`. Không có method sync sẵn — tự build trong Service.

### BorrowSellRequest entity (`Modules\...\BorrowSellRequest`)
```php
const DA_DUYET=1; const CHO_KE_TOAN_KHO=2; const DANG_TAO=3; const KHONG_DUYET=4;
const HANG_THUONG=1; const HANG_KM=2;
// canApprove(): status==CHO_KE_TOAN_KHO && currentEmployeeHasPermission('Kế toán kho')
// KHÔNG có method approve() — Service tự set status/approver_id/approved_time/save.
// Relations: products(BorrowSellRequestProduct), product_export_requests (dùng ở delivery trip posting).
```
Child: `BorrowSellRequestProduct` (cols: `objectable_id`,`objectable_type`,`unit_coefficient`,`approved_qty`,`export_price`,`price`,`extra_price`,`allocated_price`,`vat_percent`,`rebate_price`,...), `BorrowSellRequestProductDetail` (cols: `parent_id`,`product_export_request_id`,`product_export_request_detail_id`,`qty`,`approved_qty`).

### Calculator (REUSE — copy signature)
```php
availableSellQty(float $baseExportedQty, float $borrowReturnedQty, float $returningQty, float $unitCoefficient): float
    = ($base - $borrowReturned - $returning) / ($coef ?: 1);
isQtyExceeded(float $available, float $unitCoefficient, float $requestedQty): bool
    = $coef != 1 ? floor($available) < $requestedQty : $available < $requestedQty;
```

## Bảng DB đã verify (DB gộp)
- `borrow_sell_request_products.objectable_type` ∈ {`App\Model\Sale\Firm\Contract\FirmContractTabProduct` (Firm), `App\Model\Customers\WrServiceContractItem` (WrService)}. Có cols `objectable_id`, `unit_coefficient`, `approved_qty`, `export_price`.
- `product_export_request_details`: có `base_exported_qty`, `borrow_returned_qty`, `returned_by_sell`, `export_price`, `parent_id`, `product_id`.
- objectable tables: `firm_contract_tab_products` (có `exported_qty`,`quantity`), `wr_service_contract_items` (có `exported_qty`,`qty`).
- `borrow_sells` header có: `sum_amount_after_extra`, `sum_amount_after_extra_vat`, `sum_amount_after_extra_after_vat`, `sum_amount_allocated`, `sum_amount_allocated_after_vat`, `vat_cost_allocated`, `vat_percent`, `created_by`, `firm_contract_tab_id`, `bear_the_shipping`.
- **`need_check_exported` KHÔNG tồn tại** ở firm_contract_tab_products / wr_service_contract_items / borrow_sell_requests → guard quota ERP bỏ (Ruling T7-7).

## RULINGS đã chốt (BẮT BUỘC tuân theo — đã ghi ledger)

- **T7-1:** Tính LẠI header sums server-side (mirror `computeAmounts` của Phase 1) từ dòng SP server build. KHÔNG đọc `sum_amount_*`/`vat_cost_allocated` từ `$request`.
- **T7-2:** generateCode = real id sau save đầu: `code='TMP-'.uniqid()` → save() → `code=BorrowSell::PREFIX.'-'.str_pad((string)$bs->id,5,'0',STR_PAD_LEFT)` → save(). KHÔNG dùng static `generateCode()`.
- **T7-3:** updateWarehouse — cột cộng dồn (`borrow_returned_qty`,`returned_by_sell`,objectable `exported_qty`) dùng `increment()` atomic; cột gán (`approved_qty`) dùng `update()`/save.
- **T7-4:** store() 1 `DB::transaction(closure)`; gọi `postDeliveryTripAccounting($bs)` RỒI `postAccounting($bs)`; check `[ok,err]`, throw nếu ok=false để rollback.
- **T7-5:** `returningQty()` port thêm tham số loại trừ `$parent->id` khỏi nhánh sell (bsr.status=2).
- **T7-6:** HANG_THUONG only — bỏ `syncTabs` + nhánh tabs của updateWarehouse.
- **T7-7:** Bỏ guard `need_check_exported` (cột không tồn tại).

## Công thức tiền — mirror Phase 1 `computeAmounts` (Ruling T7-1)

Tích luỹ trong vòng lặp SP (dùng đúng biến giá server đã copy vào BorrowSellProduct):
```
$isFirm = ($object->contractable_type == BorrowSell::CONTRACT_FIRM);
// mỗi SP p sau khi build (qty = tổng detail qty đã bán):
$price        = $isFirm ? (float)$p->price : 0.0;   // WrService price=0
$extraPrice   = (float)$p->extra_price;
$allocated    = (float)$p->allocated_price;
$vatPercent   = (float)$p->vat_percent;
$qty          = (float)$p->qty;                     // tổng qty detail của SP
$amountAfterExtra    = ($extraPrice + $price) * $qty;
$amountAfterExtraVat = $amountAfterExtra * $vatPercent / 100;
$amountAllocated     = $allocated * $qty;
$vatAllocatedLine    = $amountAllocated * $vatPercent / 100;
$sumAfterExtra          += $amountAfterExtra;
$sumAfterExtraVat       += $amountAfterExtraVat;
$sumAllocated           += $amountAllocated;
$sumAllocatedAfterVat   += $amountAllocated + $vatAllocatedLine;
$vatCostAllocated       += $vatAllocatedLine;
```
Sau vòng lặp, set vào header TRƯỚC khi gọi posting:
```
$object->sum_amount_after_extra           = $sumAfterExtra;
$object->sum_amount_after_extra_vat       = $sumAfterExtraVat;
$object->sum_amount_after_extra_after_vat = $sumAfterExtra + $sumAfterExtraVat;
$object->sum_amount_allocated             = $sumAllocated;
$object->sum_amount_allocated_after_vat   = $sumAllocatedAfterVat;
$object->vat_cost_allocated               = $vatCostAllocated;
$object->save();
```

## Method signatures bạn PHẢI tạo

```php
namespace Modules\Finance\Services\BorrowSell;

class BorrowSellService
{
    /**
     * Lập phiếu xuất bán hàng mượn thực tế từ 1 yêu cầu (BorrowSellRequest) đã ở CHO_KE_TOAN_KHO.
     * Chạy trong 1 DB::transaction. Throw ValidationException khi không đủ điều kiện / tồn không đủ.
     */
    public function store(\Illuminate\Http\Request $request): BorrowSell;

    /** Trừ kho + cập nhật trạng thái mượn. Cột cộng dồn dùng increment() atomic (Ruling T7-3). */
    private function updateWarehouse(BorrowSell $bs): void;

    /** Port Phase 1 + loại trừ parent request (Ruling T7-5). */
    private function returningQty(int $exportRequestId, int $productId, int $excludeParentRequestId): float;
}
```

## Luồng store() (port ERP BorrowSellsController::store, đã bake rulings)

1. **Lấy parent:** `$parent = BorrowSellRequest::findOrFail($request->borrow_sell_request_id)` (tên field id yêu cầu: xem payload FE/ERP trong t7-investigation.md; nếu ERP dùng key khác thì theo ERP).
2. **Validate NGOÀI transaction:** nếu `!$parent->canApprove()` → `throw ValidationException::withMessages(['borrow_sell_request_id' => 'Yêu cầu không ở trạng thái Chờ kế toán kho hoặc bạn không có quyền Kế toán kho'])`. (canApprove đã gồm check status + quyền.)
3. **`DB::transaction(function() ... )`:**
   a. Tạo `$object = new BorrowSell([...])`: copy header từ `$parent` (contractable_id, contractable_type, customer..., type=$parent->type, firm_contract_tab_id nếu có), `status = BorrowSell::STATUS_DEFAULT` (=1, HARD như ERP), `created_by = auth()->id()`. **KHÔNG copy sum_amount_* từ parent/request** (sẽ tính lại — T7-1). code tạm `'TMP-'.uniqid()`. `$object->save()`.
   b. generateCode T7-2: `$object->code = BorrowSell::PREFIX.'-'.str_pad((string)$object->id,5,'0',STR_PAD_LEFT); $object->save();`.
   c. **Loop products** (từ `$request->products`, khớp với `$parent->products` theo objectable_id/objectable_type như ERP):
      - Tra `BorrowSellRequestProduct` cha theo objectable_id/type.
      - Tạo `BorrowSellProduct` copy snapshot (product_id, product_name, unit_id, unit_coefficient, price, extra_price, allocated_price, vat_percent, rebate_price, contract_qty...) + `parent_id=$object->id`.
      - **Loop details:** với mỗi detail (product_export_request_detail):
        - Lấy `ProductExportRequestDetail` theo id. Tính tồn khả dụng:
          `$returning = $this->returningQty($exportRequestId, $productId, $parent->id);`
          `$available = Calculator::availableSellQty($d->base_exported_qty, $d->borrow_returned_qty, $returning, $unitCoefficient);`
          nếu `Calculator::isQtyExceeded($available, $unitCoefficient, $reqQty)` → throw ValidationException (SP tồn không đủ, kèm product_name).
        - Tạo `BorrowSellProductDetail` (parent_id = borrow_sell_product id, product_export_request_id, product_export_request_detail_id, qty).
        - Cộng dồn qty + weighted total_export_price (`$totalExportPrice += $export_price_của_detail * $qty`), theo ERP.
      - Set `$p->qty = $sumQty`, `$p->export_price = $sumQty>0 ? $totalExportPrice/$sumQty : 0` (weighted avg như ERP), save.
      - Ghi `export_price` weighted trở lại `BorrowSellRequestProduct` (ERP làm vậy).
      - Tích luỹ header sums (công thức T7-1 ở trên).
   d. Kiểm tra `!$hasChange` (không SP nào được xuất) → throw ValidationException (không có gì để xuất) — mirror ERP.
   e. Set 6 header sums + save (T7-1).
   f. `$this->updateWarehouse($object);` (T7-3).
   g. **Posting (T7-4):**
      ```php
      [$okTrip, $errTrip] = app(BorrowSellPostingService::class)->postDeliveryTripAccounting($object);
      if (!$okTrip) throw new \RuntimeException($errTrip ?: 'Hạch toán vận chuyển thất bại');
      [$okAcc, $errAcc] = app(BorrowSellPostingService::class)->postAccounting($object);
      if (!$okAcc) throw new \RuntimeException($errAcc ?: 'Hạch toán phiếu xuất bán thất bại');
      ```
      (Throw để rollback outer transaction. ValidationException/RuntimeException đều rollback.)
   h. **Approve parent:** `$parent->status = BorrowSellRequest::DA_DUYET; $parent->approver_id = auth()->id(); $parent->approved_time = now(); $parent->save();`
   i. `return $object;`

## updateWarehouse() — port ERP (Ruling T7-3, T7-6)

ERP gốc (t7-investigation.md, dòng ~410-462): với mỗi BorrowSellProduct p, mỗi detail d, `$qty = $d->qty * $p->unit_coefficient`:
- **increment atomic** trên `product_export_request_details` id = `$d->product_export_request_detail_id`:
  ```php
  DB::table('product_export_request_details')->where('id', $d->product_export_request_detail_id)
      ->increment('borrow_returned_qty', $qty);
  DB::table('product_export_request_details')->where('id', $d->product_export_request_detail_id)
      ->increment('returned_by_sell', $qty);
  ```
- Set `approved_qty` (gán, không cộng) trên request_product/request_detail nếu ERP làm.
- **objectable exported_qty (increment):** resolve objectable của `BorrowSellRequestProduct` (objectable_type/objectable_id) → bảng `firm_contract_tab_products` (Firm) hoặc `wr_service_contract_items` (WrService):
  ```php
  $table = $bsrProduct->objectable_type == BorrowSell::CONTRACT_... ? 'firm_contract_tab_products' : 'wr_service_contract_items';
  DB::table($table)->where('id', $bsrProduct->objectable_id)->increment('exported_qty', $qty);
  ```
  (Map objectable_type FQN → table theo 2 giá trị đã verify.)
- **borrow_status:** nếu ERP set `borrow_status=DA_TRA` khi `base_exported_qty` đã trả hết — port nếu áp dụng cho hàng thường; dùng update() (gán).
- **BỎ nhánh tabs** (Ruling T7-6): không xử lý `count($this->tabs)`; luôn đi path SP thường.
- **BỎ guard need_check_exported** (Ruling T7-7).

## returningQty() — port Phase 1 + exclude parent (Ruling T7-5)

Copy nguyên `returningQty($exportRequestId, $productId)` của Phase 1 (private, sums import + sell bsr.status=2 + other borrow returns × unit_coefficient), THÊM param `$excludeParentRequestId` và ở **nhánh sell** (subquery lọc bsr.status=2) thêm `->where('bsr.id', '!=', $excludeParentRequestId)`. Các nhánh khác giữ nguyên. Đọc verbatim body ở Phase 1 service (dòng ~266-297) và t7-investigation.md.

## Throw/validate
- Mọi lỗi nghiệp vụ → `throw \Illuminate\Validation\ValidationException::withMessages([...])` (KHÔNG return JSON, KHÔNG catch chung Exception — CLAUDE.md bắt buộc rethrow ValidationException). Lỗi hạch toán → RuntimeException.
- `DB::transaction(closure)` tự rollback khi có exception ném ra.

## Test — `Modules/Finance/Tests/Feature/BorrowSellStoreTest.php`

Chạy: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php vendor/bin/phpunit --filter=BorrowSellStoreTest Modules/Finance/Tests/Feature/BorrowSellStoreTest.php` (KHÔNG dùng `php artisan test` — TTY fail).

Dùng `use DatabaseTransactions;`. Vì store() phụ thuộc auth()->id() + quyền + dữ liệu thật phức tạp, viết test theo hướng **đơn vị hoá phần thuần tính toán** + skip-guard giống `BorrowSellPostingWrServiceTest`:
1. **Test computeAmounts/header sums** (qua reflection hoặc tách 1 private helper `computeHeaderSums(array $products): array` để test trực tiếp): assert sum_amount_after_extra = Σ(extra+price)×qty, vat theo %, allocated. Firm vs WrService (price=0). — Đây là test QUAN TRỌNG NHẤT (khoá Ruling T7-1).
2. **Test returningQty exclude parent:** nếu dựng được fixture DB, assert qty của chính parent request bị loại. Nếu không dựng được → markTestSkipped với lý do rõ.
3. **Test isQtyExceeded/availableSellQty** đã có ở calculator — không lặp; thay vào đó 1 test tồn không đủ → ValidationException (nếu dựng được fixture; else skip).

Ưu tiên: ít nhất **1 test xanh thật** cho header sums (không skip). Nếu 1 assertion cần private → tách helper `computeHeaderSums` để vừa test vừa dùng trong store() (DRY).

## Ràng buộc bắt buộc (CLAUDE.md — nhánh gop_db)
- KHÔNG `DB_CONNECTION_SECOND`/`mysql2`. Bảng trùng tên → dùng bản ERP.
- ValidationException phải rethrow (không catch chung).
- KHÔNG commit/push git (chỉ `git add <path>` + `git commit` khi được yêu cầu trong report contract bên dưới).
- KHÔNG tự spawn subagent. KHÔNG git network ops.
- KHÔNG đọc `vendor/`, `node_modules/`.

## Report contract
Sau khi implement + test xanh:
1. `git add` đúng 2 file (service + test) và `git commit` với message tiếng Việt mô tả T7.
2. Ghi report đầy đủ vào: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-7-report.md`
3. Trả về (ngắn gọn): status (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED), (các) commit hash, 1 dòng tóm tắt kết quả test, và concerns (nếu có — vd chỗ nào phải giả định do t7-investigation.md thiếu chi tiết ERP).

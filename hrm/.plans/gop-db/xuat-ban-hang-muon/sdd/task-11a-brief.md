# Task 11a — Brief: 2 endpoint nguồn "phiếu xuất mượn" + siết `canBorrowSell` (BE)

> Đây là REQUIREMENTS của bạn. Các giá trị (route, tên method, cột, const) là chính xác — dùng **verbatim**, không tự đổi tên/đoán cột.

## Bối cảnh (1 dòng)

Màn tạo "Yêu cầu xuất bán hàng mượn" (PYCXBHM) cần: (a) danh sách phiếu **xuất mượn** hợp lệ theo hợp đồng đã chọn, (b) chi tiết SP + SL bán được của 1 phiếu xuất mượn. `store()` đã yêu cầu `product_export_request_ids[]` và `products[].details[].{product_export_request_id, product_export_request_detail_id, qty}`, nhưng **chưa có endpoint** để FE lấy 2 dữ liệu nguồn này. Task 11a bổ sung 2 endpoint READ đó + siết lỗ hổng ở `canBorrowSell`.

## Ràng buộc toàn cục (bắt buộc)

- **PHP 7.4** — KHÔNG constructor property promotion; khai property tường minh + gán trong thân constructor.
- Nhánh `gop_db`, DB gộp `erp_hrm_check`. **KHÔNG** dùng `DB_CONNECTION_SECOND`/`mysql2`. Bảng trùng tên → ưu tiên bản ERP (tên gốc).
- **Fail-closed**: mọi lọc quyền/điều kiện phải chặt; KHÔNG hard-code `true`. Lọc `created_by = auth()->id()` là ranh giới phạm vi — giữ nguyên.
- BE validate phải **rethrow `ValidationException`** (không catch chung `Exception`).
- **KHÔNG sửa** các method dùng chung ngoài phạm vi task này. Chỉ sửa đúng `canBorrowSell` như mục 4 (đã được chủ động cho phép trong task này — đây là siết fail-closed, ghi rõ ở report).
- Endpoint READ: gate bằng `created_by = self` trong query (user chỉ thấy phiếu xuất mượn của chính mình) — KHÔNG cần middleware checkPermission (đồng nhất với các route borrow-sell khác đã có).
- KHÔNG commit/push git.

## Nền tảng — dữ kiện đã trace (dùng làm chuẩn)

**Const đã có trong `BorrowSellRequestService`:** `XUAT_MUON = 3`.
**Const trong `ProductExportRequest` entity** (`Modules/Finance/Entities/ProductImportRequest/ProductExportRequest.php`): `XUAT_MUON = 3`, `DA_MUON = 2` (dùng cho `borrow_status`).
**Cột `product_export_requests` (đã verify Schema):** `id, code, type, status, borrow_status, created_by, created_at, warehouse_id, is_export_direct, firm_contract_id, wr_service_contract_id, ...`
**Cột `product_export_request_details`:** `id, parent_id, product_id, product_name, code, model_name, brand_name, unit_name, unit_id, unit_coefficient, detail_type, need_export, base_exported_qty, borrow_returned_qty, vat_percent, price, allocated_price, extra_price, rebate_price` (khớp SELECT của `dataForBorrowReturn`/`dataForSaleReturn`).

**Const `BorrowSellRequest`:** `CONTRACT_FIRM` / `CONTRACT_WR_SERVICE` (chuỗi class morph), và query param `contractable_type` nhận đúng 2 giá trị này (giống endpoint `contractBorrowSellData` đã có).

**Method có sẵn dùng lại (KHÔNG copy lại logic — gọi trực tiếp):**
- `BorrowSellRequestService::returningQty(int $exportRequestId, int $productId): float` (private, cùng class) — SL đang trả/bán/xuất dở của phiếu xuất mượn.
- `BorrowSellRequestCalculator::availableSellQty(float $baseExportedQty, float $borrowReturnedQty, float $returningQty, float $unitCoefficient): float` = `(base − returned − returning) / (coef ?: 1)`.

**Khớp store():** `syncProducts()` (dòng 199-238) tính available đúng bằng `availableSellQty(base_exported_qty, borrow_returned_qty, returningQty, unit_coefficient)`. Endpoint breakdown phải trả **cùng công thức** để FE hiển thị đúng SL bán tối đa.

---

## 1) Route — thêm 2 route vào `Modules/Finance/Routes/api.php`

File hiện có group (dòng 747-759, prefix `/borrow-sell-requests`, nằm trong outer group `/v1/finance` middleware `auth:api`). Thêm **2 route** vào group này:

- Route LIST: đặt **ngay sau** dòng `/contracts/{id}/borrow-sell-data`:
```php
Route::get('/contracts/{id}/export-requests', [BorrowSellRequestController::class, 'contractExportRequests']);
```
- Route BREAKDOWN: đặt **trước** dòng `GET /{id}` (show) cuối cùng — literal segment `export-requests` không đụng `/{id}` (khác số segment) nhưng vẫn giữ tĩnh-trước-động:
```php
Route::get('/export-requests/{id}', [BorrowSellRequestController::class, 'exportRequestBorrowSellData']);
```

Full path kết quả: `GET api/v1/finance/borrow-sell-requests/contracts/{id}/export-requests` và `GET api/v1/finance/borrow-sell-requests/export-requests/{id}`.

## 2) Controller — thêm 2 method vào `BorrowSellRequestController.php`

Đặt 2 method sau `contractBorrowSellData()` (nhóm load nguồn). Controller MỎNG — chỉ gọi service:

```php
/** Danh sách phiếu XUẤT MƯỢN hợp lệ theo hợp đồng đã chọn (để lập yêu cầu xuất bán hàng mượn). */
public function contractExportRequests(Request $request, $id)
{
    return $this->responseJson('OK', 200, $this->service->searchExportRequests(
        $request,
        (int) $id,
        (string) $request->get('contractable_type')
    ));
}

/** Chi tiết SP + SL bán được của 1 phiếu xuất mượn (dòng chi tiết nguồn cho grid nhập SL). */
public function exportRequestBorrowSellData($id)
{
    return $this->responseJson('OK', 200, $this->service->dataForBorrowSell((int) $id));
}
```

(`$this->service` đã là property có sẵn; `Request` đã `use Illuminate\Http\Request;` ở đầu file.)

## 3) Service — thêm 2 public method vào `BorrowSellRequestService.php`

Đặt **ngay sau** `searchContracts()` (dòng ~604, trước block `// Helpers`). Dùng đúng style query builder của file.

### 3a. `searchExportRequests` — danh sách phiếu xuất mượn theo hợp đồng

```php
/**
 * Danh sách phiếu XUẤT MƯỢN hợp lệ để lập yêu cầu xuất bán hàng mượn, lọc theo hợp đồng.
 * Điều kiện (fail-closed, strict AND): của CHÍNH mình + type=Xuất mượn + status=5 (đã hạch toán)
 * + borrow_status=Đã mượn(2) + đúng hợp đồng (firm_contract_id | wr_service_contract_id).
 * Port từ ProductExportRequest::searchForImportType() nhánh MUON_TRA_LAI, BỔ SUNG lọc hợp đồng.
 */
public function searchExportRequests(Request $request, int $contractId, string $contractableType): array
{
    $isFirm = $contractableType === BorrowSellRequest::CONTRACT_FIRM;
    $keyword = trim((string) $request->get('keyword', ''));

    $q = DB::table('product_export_requests')
        ->where('created_by', auth()->id())
        ->where('type', self::XUAT_MUON)
        ->where('status', 5)
        ->where('borrow_status', ProductExportRequest::DA_MUON)
        ->where($isFirm ? 'firm_contract_id' : 'wr_service_contract_id', $contractId);

    if ($keyword !== '') {
        $q->where('code', 'like', '%' . $keyword . '%');
    }

    $rows = $q->orderBy('created_at', 'DESC')->limit(50)->get(['id', 'code', 'created_at']);

    $result = [];
    foreach ($rows as $r) {
        $result[] = [
            'id' => $r->id,
            'code' => $r->code,
            'created_at' => $r->created_at,
        ];
    }

    return $result;
}
```

> **Import cần thêm** ở đầu file (nhóm `use`): `use Modules\Finance\Entities\ProductImportRequest\ProductExportRequest;` (để dùng `ProductExportRequest::DA_MUON`). Nếu đã có thì bỏ qua.
> **Ruling R-T11a-list:** trả mảng phẳng, `limit(50)`, KHÔNG paginate — 1 hợp đồng chỉ có vài phiếu xuất mượn của 1 user; FE picker (modal table) tự phân trang client-side. Nếu về sau count lớn thì bổ sung paginate — ghi ở report.

### 3b. `dataForBorrowSell` — chi tiết SP + SL bán được của 1 phiếu xuất mượn

```php
/**
 * Chi tiết dòng SP + SL bán được (available) của 1 phiếu XUẤT MƯỢN, để FE dựng grid nhập SL bán.
 * available = availableSellQty(base_exported_qty, borrow_returned_qty, returningQty, unit_coefficient)
 * — KHỚP đúng công thức store()/syncProducts() để FE và BE không lệch.
 * SELECT gồm cả field giá bán (price/allocated_price/extra_price/rebate_price/vat_percent) để FE điền sẵn.
 */
public function dataForBorrowSell(int $exportRequestId): array
{
    if (!$this->canBorrowSell($exportRequestId)) {
        throw ValidationException::withMessages([
            'product_export_request_id' => ['Phiếu xuất mượn không hợp lệ!'],
        ]);
    }

    $request = DB::table('product_export_requests')->where('id', $exportRequestId)->first(['id', 'code']);

    $rows = DB::table('product_export_request_details')
        ->where('parent_id', $exportRequestId)
        ->where('need_export', true)
        ->whereRaw('base_exported_qty > borrow_returned_qty')
        ->get([
            'id', 'id as product_export_request_detail_id', 'parent_id', 'product_id',
            'product_name', 'code', 'model_name', 'brand_name', 'unit_name', 'unit_id',
            'unit_coefficient', 'detail_type', 'base_exported_qty', 'borrow_returned_qty',
            'vat_percent', 'price', 'allocated_price', 'extra_price', 'rebate_price',
        ]);

    $products = [];
    foreach ($rows as $r) {
        $returning = $this->returningQty($exportRequestId, (int) $r->product_id);
        $available = BorrowSellRequestCalculator::availableSellQty(
            (float) $r->base_exported_qty,
            (float) $r->borrow_returned_qty,
            (float) $returning,
            (float) $r->unit_coefficient
        );
        $r->product_export_request_id = $exportRequestId;
        $r->available = $available;
        $products[] = (array) $r;
    }

    return [
        'id' => $request->id,
        'code' => $request->code,
        'products' => $products,
    ];
}
```

> **Ruling R-T11a-breakdown:** giữ mọi dòng thỏa `base_exported_qty > borrow_returned_qty` kể cả khi `available` đã về 0 do `returningQty` (in-flight) — trả field `available` để FE tự chặn nhập > available (đồng nhất `isQtyExceeded` ở store). KHÔNG lọc bỏ dòng available=0 ở BE (tránh ẩn dòng khiến user tưởng mất SP). Ghi ở report.
> `product_export_request_id` được nhét vào mỗi dòng để FE ghép thẳng vào payload `products[].details[]` mà không phải map lại.

## 4) Siết `canBorrowSell` (fail-closed) — `BorrowSellRequestService.php:674-681`

Hiện tại (LỎNG — OR, thiếu type):
```php
return ((int) $row->created_by === (int) auth()->id()) && ((int) $row->status === 5 || (int) $row->borrow_status === 2);
```
Sửa thành (CHẶT — AND đủ 4 điều kiện, thêm `type`):
```php
return ((int) $row->created_by === (int) auth()->id())
    && ((int) $row->type === self::XUAT_MUON)
    && ((int) $row->status === 5)
    && ((int) $row->borrow_status === ProductExportRequest::DA_MUON);
```
**Đồng thời** thêm `type` vào SELECT của dòng 676:
```php
$row = DB::table('product_export_requests')->where('id', $exportRequestId)->first(['created_by', 'type', 'status', 'borrow_status']);
```

**Lý do (ghi ở report):** spec §4.3#2 yêu cầu status=5 **VÀ** borrow_status=DA_MUON (không phải OR), và nguồn bắt buộc là phiếu **XUẤT MƯỢN** (type=3). OR + thiếu type cho phép chọn phiếu không phải xuất mượn / chưa mượn → lỗ hổng nghiệp vụ. Siết lại khớp filter của `searchExportRequests` (mục 3a) và của ERP. Đây là "HRM chặt hơn ERP".

Ảnh hưởng lan: `store()` (dòng 51) đã gọi `canBorrowSell` cho từng id trong `product_export_request_ids` → sau khi siết, store cũng chặt hơn (đồng bộ). KHÔNG có caller nào khác (verify bằng grep `canBorrowSell` trong Modules/Finance trước khi kết thúc).

---

## Verify (bắt buộc, ghi kết quả vào report)

1. `php -l` 3 file sửa (Routes/api.php, Controller, Service) → No syntax errors.
2. `composer dump-autoload -o` → chạy được.
3. Tinker smoke (KHÔNG cần auth, chỉ kiểm method tồn tại + không nổ khi gọi với id có thật nếu có):
   - `method_exists(\Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService::class, 'searchExportRequests')` → true
   - `method_exists(..., 'dataForBorrowSell')` → true
   - `method_exists(\Modules\Finance\Http\Controllers\V1\BorrowSellRequestController::class, 'contractExportRequests')` → true, `'exportRequestBorrowSellData'` → true
4. Route dump qua `Route::getRoutes()` (KHÔNG `php artisan route:list` — CRASH toàn cục do bug pre-existing ở module Timesheet `RequestUpdateTimeSheetController::__construct()`, không liên quan task này): xác nhận có 2 route mới, `GET /export-requests/{id}` nằm trên `GET /{id}` (show).
5. `grep -rn "canBorrowSell" Modules/Finance` → xác nhận chỉ `store()` + `dataForBorrowSell()` gọi (không caller nào khác bị ảnh hưởng ngoài dự kiến).

## Report

Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-11a-report.md`. Trả về (chỉ) STATUS (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED), danh sách commit (KHÔNG commit trong task này — để trống/ghi "không commit"), 1 dòng tóm tắt verify, và Concerns.

**KHÔNG dispatch subagent. KHÔNG commit git.**

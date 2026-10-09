# Task P2-9 Brief — BorrowSellController + 3 Resource + routes (API phiếu xuất bán hàng mượn)

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, dùng giá trị exact verbatim.**
> Feature `xuat-ban-hang-muon` Phase 2 (HRM, Laravel 8/PHP 7.4, nhánh `gop_db`). Giao tiếp tiếng Việt.
> Thư mục code: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`

## Bối cảnh 1 dòng

Lớp API cho phiếu xuất bán hàng mượn thực tế (`BorrowSell`, mã `PXBHM-`). Controller mỏng gọi `BorrowSellService::store()` (đã tồn tại — T7), list scope 4 cấp quyền, chi tiết nhúng tab Hạch toán, in JSON thuần. Đây là bước cuối của BE Phase 2.

## File

- **Create:** `Modules/Finance/Http/Controllers/V1/BorrowSellController.php`
- **Create:** `Modules/Finance/Transformers/BorrowSellResource/BorrowSellListResource.php`
- **Create:** `Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php`
- **Create:** `Modules/Finance/Transformers/BorrowSellResource/BorrowSellPrintResource.php`
- **Modify:** `Modules/Finance/Routes/api.php` (thêm group `/borrow-sells`)
- **Modify:** `Modules/Finance/Entities/BorrowSell/BorrowSell.php` (thêm searchByFilter/meta/userCanCreate/is_can_view — Ruling T9-entity-additions)
- **Create test:** `Modules/Finance/Tests/Feature/BorrowSellApiTest.php`

## Pattern để MIRROR (đọc trước khi viết — path thật, đã verify)

- Controller: `Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php` — thin controller, extends `ApiController`, inject service qua constructor, dùng `$this->responseJson($msg, $code, $data)`. Mirror index/store/show/printData.
- Entity scope: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` — `searchByFilter($request)` (nhánh 4 cấp quyền ~dòng 213-231), `meta()`, các hằng `PERMISSION_VIEW_ALL_COMPANY`/`PERMISSION_VIEW_COMPANY`/`PERMISSION_VIEW_DEPARTMENT`/`PERMISSION_KE_TOAN_KHO` (~dòng 38-42).
- Trait quyền dùng chung: `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php` — `currentEmployeeHasPermission()`, `currentCompanyId()`, `currentManagedDepartmentIds()` (protected static). BorrowSell entity ĐÃ `use ChecksEmployeePermission` (canView dùng nó).
- Resource: `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestListResource.php` + `BorrowSellRequestDetailResource.php` + `BorrowSellRequestPrintResource.php` — mirror cấu trúc toArray, batch tra contract_code (tránh N+1), nhúng products nested.
- Routes: `Modules/Finance/Routes/api.php` group `/borrow-sell-requests` (~dòng 747-760): **KHÔNG middleware checkPermission**, route `/{id}` (show) đặt CUỐI group.

## Interfaces TIÊU THỤ (đã tồn tại — chỉ gọi)

```php
// Service (T7) — resolve qua constructor inject hoặc app()
Modules\Finance\Services\BorrowSell\BorrowSellService::store(\Illuminate\Http\Request $request): BorrowSell;
// Posting (T4-6) — cho tab Hạch toán trong Detail Resource
Modules\Finance\Services\BorrowSell\BorrowSellPostingService::getDataAccounting(BorrowSell $bs): array; // [bool $ok, array $accounts, string $err]
// Entity (T1) — đã có
BorrowSell::canView(): bool  // = (Kế toán kho && status!=3) || created_by==auth id
BorrowSell consts: PREFIX='PXBHM', PERMISSION_KE_TOAN_KHO='Kế toán kho', CONTRACT_FIRM, CONTRACT_WR_SERVICE
// FormRequest (T8) — đã có
Modules\Finance\Http\Requests\BorrowSell\StoreBorrowSellRequest
```

## RULINGS đã chốt (BẮT BUỘC — đã ghi ledger)

- **T9-perm:** List scope tái dùng 4-tier NAME của BorrowSellRequest (KHÔNG dùng id 100315-100318 — không tồn tại). Cài `BorrowSell::searchByFilter($request)` mirror BorrowSellRequest, tham chiếu `BorrowSellRequest::PERMISSION_VIEW_ALL_COMPANY/_COMPANY/_DEPARTMENT`.
- **T9-store-gate:** KHÔNG middleware checkPermission. Controller store() gate tường minh 403 nếu thiếu 'Kế toán kho' qua `BorrowSell::userCanCreate()`; service canApprove() giữ defense-in-depth.
- **T9-print:** PrintResource JSON thuần, KHÔNG tra khóa mẫu in.
- **T9-accounting-in-detail:** Detail Resource nhúng `accounting` từ getDataAccounting (ok→accounts, else→accounting_error).
- **T9-entity-additions:** thêm searchByFilter/meta/userCanCreate/is_can_view accessor vào BorrowSell.

## Chi tiết bổ sung entity BorrowSell (Ruling T9-entity-additions)

```php
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;

// 4-tier list scope — mirror BorrowSellRequest::searchByFilter (nhánh phân quyền)
public static function searchByFilter(\Illuminate\Http\Request $request)
{
    $query = self::query()->with([/* relations nhẹ nếu cần cho list */])->orderByDesc('id');

    // lọc cơ bản theo $request (code, status, contractable_type, khoảng ngày...) — mirror BorrowSellRequest
    if ($request->filled('code'))   $query->where('code', 'like', '%'.$request->get('code').'%');
    if ($request->filled('status')) $query->where('status', $request->get('status'));
    // ... các filter khác tương tự BorrowSellRequest, GIỮ TỐI THIỂU nếu không rõ

    // Phân quyền 4 cấp (mirror BorrowSellRequest dòng ~213-231)
    if (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_ALL_COMPANY)) {
        // không lọc thêm
    } elseif (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_COMPANY)) {
        $query->where('company_id', self::currentCompanyId());
    } elseif (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_DEPARTMENT)) {
        $query->whereIn('department_id', self::currentManagedDepartmentIds());
    } else {
        $query->where('created_by', auth()->id());
    }
    return $query;
}

// Cờ FE cho màn list
public static function meta(): array
{
    return [
        'is_ke_toan_kho' => self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO),
    ];
}

// Gate tạo phiếu (dùng ở controller store → 403)
public static function userCanCreate(): bool
{
    return self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO);
}

// Accessor cho Resource
public function getIsCanViewAttribute(): bool
{
    return $this->canView();
}
```
LƯU Ý: kiểm tra `company_id`/`department_id` có tồn tại trên bảng `borrow_sells` không (đọc entity/migration); nếu tên cột khác thì chỉnh cho khớp. Nếu `borrow_sells` KHÔNG có `company_id`/`department_id` → lấy scope theo cột tương ứng có thật (vd join qua borrow_sell_request), GHI RÕ giả định trong report.

## Controller (mirror BorrowSellRequestController)

```php
namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Modules\Finance\Entities\BorrowSell\BorrowSell;
use Modules\Finance\Http\Requests\BorrowSell\StoreBorrowSellRequest;
use Modules\Finance\Services\BorrowSell\BorrowSellService;
use Modules\Finance\Transformers\BorrowSellResource\BorrowSellListResource;
use Modules\Finance\Transformers\BorrowSellResource\BorrowSellDetailResource;
use Modules\Finance\Transformers\BorrowSellResource\BorrowSellPrintResource;

class BorrowSellController extends ApiController   // dùng đúng base ApiController như BorrowSellRequestController
{
    private $service;
    public function __construct(BorrowSellService $service) { $this->service = $service; }

    public function index(Request $request)
    {
        $items = BorrowSell::searchByFilter($request)->paginate((int) $request->get('per_page', 20));
        return (new BorrowSellListResource($items))->additional(array_merge([
            'total' => $items->total(), 'lastPage' => $items->lastPage(),
            'currentPage' => $items->currentPage(), 'perPage' => (int) $items->perPage(),
        ], BorrowSell::meta()));
    }

    public function store(StoreBorrowSellRequest $request)
    {
        if (!BorrowSell::userCanCreate()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        $m = $this->service->store($request);
        return $this->responseJson('Lập phiếu xuất bán thành công', 200, [
            'id' => $m->id, 'code' => $m->code, 'status' => $m->status,
        ]);
    }

    public function show($id)
    {
        $m = BorrowSell::with([/* products.details, tabs nếu cần */])->findOrFail((int) $id);
        if (!$m->canView()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        return new BorrowSellDetailResource($m);
    }

    public function printData($id)
    {
        $m = BorrowSell::with([/* ... */])->findOrFail((int) $id);
        if (!$m->canView()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        return new BorrowSellPrintResource($m);
    }
}
```
Kiểm tra tên/response helper của `ApiController` thật (mở `BorrowSellRequestController` xem base + `responseJson` signature) và dùng đúng.

## 3 Resource

- **BorrowSellListResource** (mirror BorrowSellRequestListResource): các field phẳng `id, code, status, status_name, contractable_type, contract_code, customer_name, creator_name, created_at`, tổng tiền header (`sum_amount_after_extra_after_vat` hoặc field tổng phù hợp), và cờ `is_can_view` (dùng accessor). Batch tra `contract_code` theo firm/wr ids tránh N+1 nếu mirror được; nếu phức tạp, GIỮ tối thiểu (tra từng cái) và ghi chú.
- **BorrowSellDetailResource** (mirror BorrowSellRequestDetailResource + THÊM accounting): full header + products nested (mỗi product có details) + khối `accounting`:
  ```php
  // trong toArray():
  [$ok, $accounts, $err] = app(\Modules\Finance\Services\BorrowSell\BorrowSellPostingService::class)->getDataAccounting($this->resource);
  // ...
  'accounting' => $ok ? $accounts : [],
  'accounting_error' => $ok ? null : $err,
  'contract_type' => $this->contractable_type === BorrowSell::CONTRACT_FIRM ? 'firm' : 'wr_service',
  ```
- **BorrowSellPrintResource** (mirror BorrowSellRequestPrintResource): JSON thuần cho FE render — mã phiếu, tên khách, danh sách SP (`stt, code, product_name, model_name, unit_name, qty, export_price, thành tiền`). KHÔNG tra khóa mẫu in (Ruling T9-print).

## Routes (thêm vào Modules/Finance/Routes/api.php)

Thêm group (KHÔNG middleware checkPermission — Ruling T9-store-gate; show `/{id}` đặt CUỐI):
```php
Route::group(['prefix' => '/borrow-sells'], function () {
    Route::get('/', [BorrowSellController::class, 'index']);
    Route::post('/', [BorrowSellController::class, 'store']);
    Route::get('/{id}/print-data', [BorrowSellController::class, 'printData']);
    Route::get('/{id}', [BorrowSellController::class, 'show']); // CUỐI CÙNG
});
```
Nhớ `use Modules\Finance\Http\Controllers\V1\BorrowSellController;` ở đầu file routes (mirror cách import controller khác). Đặt group ở vị trí hợp lý trong file (gần group borrow-sell-requests).

## Test — `Modules/Finance/Tests/Feature/BorrowSellApiTest.php`

Chạy: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php vendor/bin/phpunit --filter=BorrowSellApiTest Modules/Finance/Tests/Feature/BorrowSellApiTest.php` (KHÔNG `php artisan test`).

Test API thật cần auth + quyền + dữ liệu phức tạp → khó dựng full. Ưu tiên test những gì dựng được, XANH THẬT:
1. **Route đăng ký đúng:** assert `route` tồn tại / gọi `GET /api/v1/finance/borrow-sells` (không auth hoặc auth thường) trả về đúng dạng (200 hoặc 401/403 tùy middleware auth toàn cục) — tối thiểu KHÔNG lỗi 500. Kiểm prefix thật của module (đọc RouteServiceProvider/api.php để biết prefix `/api/v1/finance` hay khác).
2. **store không quyền → 403:** giả lập user KHÔNG có 'Kế toán kho' → `POST /borrow-sells` → 403. Nếu khó giả lập quyền, dùng unit test gọi thẳng `BorrowSell::userCanCreate()` với auth context, hoặc markTestSkipped ghi lý do.
3. **Detail Resource có key `accounting`:** dựng 1 BorrowSell tối thiểu (hoặc reuse fixture kiểu BorrowSellPostingWrServiceTest) → gọi `(new BorrowSellDetailResource($bs))->toArray(request())` → assert có key `accounting` + `accounting_error`.

Chấp nhận markTestSkipped cho case cần DB/auth phức tạp NHƯNG phải có ít nhất 1-2 test XANH THẬT (vd test #3 Resource shape, hoặc userCanCreate logic). Ghi rõ skip lý do.

## Ràng buộc
- KHÔNG DB_CONNECTION_SECOND/mysql2. Bảng trùng tên dùng bản ERP.
- ValidationException phải rethrow (service tự làm). Controller trả 403 cho thiếu quyền (không catch chung).
- Cờ quyền fail-closed: KHÔNG hardcode `= true`. `is_can_view` lấy từ `canView()`.
- KHÔNG đọc vendor/node_modules. KHÔNG spawn subagent. KHÔNG git network op.
- KHÔNG sửa entity dùng chung ngoài BorrowSell (Ruling T9-entity-additions chỉ cho phép BorrowSell).

## Report contract
1. Test xanh → `git add` đúng các file trên (controller, 3 resource, routes, entity BorrowSell, test) + `git commit` message tiếng Việt.
2. Ghi report vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-9-report.md` — nêu rõ: cột company_id/department_id trên borrow_sells có thật không (searchByFilter scope), base ApiController + responseJson dùng đúng chưa, các giả định.
3. Trả về ngắn: status, commit hash, 1 dòng test summary, concerns.

# Task 5 — Controller + Routes + Seed quyền cho Hợp đồng mua

Implementer, module Supply (Laravel 8 / PHP 7.4) tại D:\laragon\www\dns. Tiếng Việt. KHÔNG git commit. KHÔNG đọc vendor/.

Task 1-4 đã xong: 4 bảng `purchase_contracts*`, 4 entity, `StorePurchaseContractRequest`, `PurchaseContractService`, 2 transformer trong `Transformers/PurchaseContract/`.

## File

- Tạo: `hrm-thanhan-api/Modules/Supply/Http/Controllers/Api/V1/PurchaseContractController.php`
- Sửa: `hrm-thanhan-api/Modules/Supply/Routes/api.php` (thêm nhóm `/purchase-contracts` + import controller)
- Tạo seeder idempotent: `hrm-thanhan-api/Modules/Supply/Database/Seeders/PurchaseContractPermissionSeeder.php`
- Sửa seeder gốc (fresh install): `hrm-thanhan-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm 3 dòng sau id 517)

## Đọc trước (nguồn chân lý — KHÔNG đoán)

- Mẫu controller: `Modules/Supply/Http/Controllers/Api/V1/SupplyHandlingController.php` (pattern index/store/show/update/approve/rejectApprove/destroy + DB::transaction + try/catch → Log::error + responseJson HTTP_BAD_REQUEST).
- Base controller: `Modules/Supply/Http/Controllers/Api/V1/ApiController.php` (có `responseJson`, `apiGetList`).
- Service đã viết: `Modules/Supply/Services/PurchaseContractService.php` — CHÚ Ý tên method list là **`getList($request)`** (KHÔNG phải `index`); còn có `previewNextCode()`, `store($request)`, `update($request,$contract)`, `approve($contract)`, `rejectApprove($contract, ?string $reason)`.
- Transformer: `Modules/Supply/Transformers/PurchaseContract/PurchaseContractResource.php` + `DetailPurchaseContractResource.php`.
- Request: `Modules/Supply/Http/Requests/StorePurchaseContractRequest.php`.
- Routes hiện có: `Modules/Supply/Routes/api.php` (theo đúng style: static route TRƯỚC wildcard `/{...}`; `checkPermission:<Tên quyền>` chỉ trên store/update/destroy/approve/reject-approve).
- Reuse nguồn hàng: `Modules/Supply/Services/SupplyReportService.php::purchaseDemand(array $filters)` trả `['kpi','rows','filters']`, mỗi row có product_id/product_code/product_hh_code/product_name/unit_name/group_name/total_buy_qty/lines[]. Và `Modules/Supply/Services/SupplyProposalService.php::goodsPool($type)` — gọi `goodsPool(2)` trả danh mục hàng hóa chung (mảng item có product_id/product_code/product_hh_code/product_name/unit_id/unit_name...).
- Entity Bên A: `Modules/Human/Entities/Company.php` (cột: name, address, tax_code, phone, code, deputy_name, deputy_role — KHÔNG có cột ngân hàng).
- Entity Bên B: `Modules/Category/Entities/Supplier.php` (chỉ code/name/status; const ACTIVE=1). Snapshot ngân hàng/địa chỉ nhập tay ở FE.

## Controller — các action

Constructor inject `PurchaseContractService $service`. Import Request, Response, DB, Log, Exception, entity `PurchaseContract`, `StorePurchaseContractRequest`, 2 Resource. Mọi action ghi/duyệt bọc `DB::transaction` + try/catch → `Log::error($e)` + `responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST)`.

1. `index(Request $request)`:
   ```php
   $request->merge(['per_page' => $request->limit ?? $request->per_page ?? 10]);
   $result = $this->service->getList($request);
   return $this->apiGetList(PurchaseContractResource::apiPaginate($result, $request));
   ```
2. `nextCode(Request $request)`: try/catch → `responseJson('success', HTTP_OK, ['code' => $this->service->previewNextCode()])`.
3. `store(StorePurchaseContractRequest $request)`: transaction → `$model = $this->service->store($request);` → `responseJson('success', HTTP_OK, $model)`.
4. `show(PurchaseContract $purchaseContract)`:
   ```php
   $purchaseContract->load('products', 'paymentTerms', 'progress');
   $data = (new DetailPurchaseContractResource($purchaseContract))->toArray(request());
   return $this->responseJson('success', Response::HTTP_OK, $data);
   ```
5. `update(StorePurchaseContractRequest $request, PurchaseContract $purchaseContract)`: transaction → `$this->service->update($request, $purchaseContract)` → responseJson model.
6. `approve(PurchaseContract $purchaseContract)`: transaction → `$this->service->approve($purchaseContract)` → responseJson success.
7. `rejectApprove(Request $request, PurchaseContract $purchaseContract)`: transaction → `$this->service->rejectApprove($purchaseContract, $request->input('reason_deny'))` → responseJson success.
8. `destroy(PurchaseContract $purchaseContract)`:
   ```php
   if (!$purchaseContract->is_can_delete) {
       return $this->responseJson('Không thể xóa hợp đồng này', Response::HTTP_BAD_REQUEST);
   }
   // transaction → $purchaseContract->delete(); → responseJson success
   ```
9. `companies(Request $request)` — dropdown Bên A + snapshot:
   ```php
   $rows = \Modules\Human\Entities\Company::query()
       ->when($request->keyword, fn($q)=>$q->where('name','like','%'.$request->keyword.'%'))
       ->orderBy('name')->get();
   $data = $rows->map(fn($c)=>[
       'id'             => $c->id,
       'code'           => $c->code,
       'name'           => $c->name,
       'address'        => $c->address,
       'tax'            => $c->tax_code,
       'phone'          => $c->phone,
       'bank_no'        => '',
       'bank_name'      => '',
       'bank_branch'    => '',
       'representative' => $c->deputy_name,
       'title'          => $c->deputy_role,
   ]);
   return $this->responseJson('success', Response::HTTP_OK, $data);
   ```
10. `suppliers(Request $request)` — dropdown Bên B + snapshot (ngân hàng/đại diện để trống, FE nhập tay):
    ```php
    $rows = \Modules\Category\Entities\Supplier::query()
        ->where('status', \Modules\Category\Entities\Supplier::ACTIVE)
        ->when($request->keyword, fn($q)=>$q->where('name','like','%'.$request->keyword.'%'))
        ->orderBy('name')->get();
    $data = $rows->map(fn($s)=>[
        'id'=>$s->id, 'code'=>$s->code, 'name'=>$s->name,
        'address'=>'', 'tax'=>'', 'phone'=>'',
        'bank_no'=>'', 'bank_name'=>'', 'bank_branch'=>'',
        'representative'=>'', 'title'=>'', 'auth_doc'=>'',
    ]);
    return $this->responseJson('success', Response::HTTP_OK, $data);
    ```
11. `goodsPool(Request $request)` — nguồn hàng cho popup chọn hàng (2 nguồn: nhu cầu mua + danh mục chung):
    ```php
    try {
        $filters = ['group'=>$request->group, 'type'=>$request->type, 'customer_id'=>$request->customer_id, 'keyword'=>$request->keyword];
        $demand  = app(\Modules\Supply\Services\SupplyReportService::class)->purchaseDemand($filters)['rows'] ?? [];
        $catalog = app(\Modules\Supply\Services\SupplyProposalService::class)->goodsPool(2);

        $exclude = (array) $request->input('exclude_codes', []);
        if (!empty($exclude)) {
            $notExcluded = fn($code, $hh) => !in_array($code, $exclude, true) && !in_array($hh, $exclude, true);
            $demand  = array_values(array_filter($demand,  fn($r)=>$notExcluded($r['product_code'] ?? null, $r['product_hh_code'] ?? null)));
            $catalog = array_values(array_filter($catalog, fn($r)=>$notExcluded($r['product_code'] ?? null, $r['product_hh_code'] ?? null)));
        }

        return $this->responseJson('success', Response::HTTP_OK, ['demand'=>$demand, 'catalog'=>$catalog]);
    } catch (Exception $e) {
        Log::error($e);
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
    ```

## Routes — thêm vào `Modules/Supply/Routes/api.php`

- Thêm `use Modules\Supply\Http\Controllers\Api\V1\PurchaseContractController;` ở đầu file (cạnh các use controller khác).
- Thêm nhóm này BÊN TRONG group `['prefix' => '/v1/supply', 'middleware' => 'auth:api']` (sau nhóm supply-handlings, trước hoặc sau reports đều được):
  ```php
  Route::group(['prefix' => '/purchase-contracts'], function () {
      Route::get('/', [PurchaseContractController::class, 'index']);
      // Static route PHẢI đặt trước wildcard /{purchaseContract}
      Route::get('/next-code', [PurchaseContractController::class, 'nextCode']);
      Route::get('/companies', [PurchaseContractController::class, 'companies']);
      Route::get('/suppliers', [PurchaseContractController::class, 'suppliers']);
      Route::get('/goods-pool', [PurchaseContractController::class, 'goodsPool']);
      Route::post('/', [PurchaseContractController::class, 'store'])
          ->middleware('checkPermission:Lập hợp đồng mua');
      Route::get('/{purchaseContract}', [PurchaseContractController::class, 'show']);
      Route::put('/{purchaseContract}/approve', [PurchaseContractController::class, 'approve'])
          ->middleware('checkPermission:Duyệt hợp đồng mua');
      Route::put('/{purchaseContract}/reject-approve', [PurchaseContractController::class, 'rejectApprove'])
          ->middleware('checkPermission:Duyệt hợp đồng mua');
      Route::put('/{purchaseContract}', [PurchaseContractController::class, 'update'])
          ->middleware('checkPermission:Lập hợp đồng mua');
      Route::delete('/{purchaseContract}', [PurchaseContractController::class, 'destroy'])
          ->middleware('checkPermission:Lập hợp đồng mua');
  });
  ```
- Route model binding: param `{purchaseContract}` map vào `PurchaseContract $purchaseContract` (camelCase khớp — giữ đúng tên).

## Seed 3 quyền (id nối tiếp — max hiện tại là 517)

Quyền: `Xem hợp đồng mua` (id 518), `Lập hợp đồng mua` (id 519), `Duyệt hợp đồng mua` (id 520). group `'Cung ứng'`, type `7`, guard `api`.

(a) Thêm vào `PermissionsTableSeeder.php` NGAY SAU dòng tạo id 517 (dòng `Xem báo cáo tổng hợp nhu cầu mua hàng`, ~dòng 736), giữ đúng style `Permission::create([...])`:
```php
// Phân hệ Cung ứng - Hợp đồng mua
Permission::create(['id' => 518, 'guard_name' => 'api', 'name' => 'Xem hợp đồng mua', 'display_name' => 'Xem hợp đồng mua', 'group' => 'Cung ứng', 'type' => 7]);
Permission::create(['id' => 519, 'guard_name' => 'api', 'name' => 'Lập hợp đồng mua', 'display_name' => 'Lập hợp đồng mua', 'group' => 'Cung ứng', 'type' => 7]);
Permission::create(['id' => 520, 'guard_name' => 'api', 'name' => 'Duyệt hợp đồng mua', 'display_name' => 'Duyệt hợp đồng mua', 'group' => 'Cung ứng', 'type' => 7]);
```

(b) Tạo seeder idempotent (chạy được trên DB đang có, KHÔNG trùng id) — `PurchaseContractPermissionSeeder.php`:
```php
<?php
namespace Modules\Supply\Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Permission;

class PurchaseContractPermissionSeeder extends Seeder
{
    public function run()
    {
        $perms = [
            ['id' => 518, 'name' => 'Xem hợp đồng mua'],
            ['id' => 519, 'name' => 'Lập hợp đồng mua'],
            ['id' => 520, 'name' => 'Duyệt hợp đồng mua'],
        ];
        foreach ($perms as $p) {
            Permission::firstOrCreate(
                ['name' => $p['name'], 'guard_name' => 'api'],
                ['id' => $p['id'], 'display_name' => $p['name'], 'group' => 'Cung ứng', 'type' => 7]
            );
        }
        app()[\Spatie\Permission\PermissionRegistrar::class]->forgetCachedPermissions();
    }
}
```
(Đối chiếu namespace/`use` của spatie Permission bằng cách xem 1 file dùng `Permission::create` — nếu class Permission là `Spatie\Permission\Models\Permission` thì giữ nguyên; nếu project alias khác thì import cho khớp.)

## Verify (bắt buộc)

- `php -l` cho: controller, api.php, PurchaseContractPermissionSeeder.php, PermissionsTableSeeder.php — dán output.
- KHÔNG chạy migrate/seed/route:list (môi trường có thể không có DB). Chỉ kiểm cú pháp tĩnh.

## Report

Ghi đầy đủ vào `D:\laragon\www\dns\.plans\hop-dong-mua\task-05-report.md`. Trả về: STATUS, danh sách file tạo/sửa, kết quả `php -l` từng file, id quyền đã seed (518/519/520), và concern (nếu có). Nếu class Permission spatie khác namespace giả định → nêu rõ trong concern.

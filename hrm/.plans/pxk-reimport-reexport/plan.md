# Nhập lại / Xuất lại Phiếu xuất kho (PXK) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port 2 chức năng cuối vòng đời PXK từ ERP sang HRM module Assign: **Nhập lại** (phiếu độc lập `PNL-`, hoàn tồn ngay) và **Xuất lại** (PXK con, trừ tồn lại), ghi dữ liệu đúng y ERP.

**Architecture:** Nhập lại = entity `WarehouseReImport` (+4 con) map bảng gộp-DB sẵn có, controller/service riêng, danh sách phân quyền theo cấp; hoàn tồn qua `PhysicalStockWriter::importLot`. Xuất lại = method trên `WarehouseExportService` tạo PXK con (`parent_warehouse_export_id`) rồi chạy lại đúng luồng tạo PXK hiện có của HRM. FE mượn khung Finance, đặt dưới `pages/finance/warehouse-exports/` + `warehouse-reimports/`.

**Tech Stack:** hrm-api = Laravel 8 / PHP 7.4 / nwidart modules; hrm-client = Nuxt2 / Vue2. DB gộp `erp_hrm_check`. Test BE = PHPUnit feature (`DatabaseTransactions`, chạy LOCAL). Verify FE = Playwright MCP (http://127.0.0.1:3000).

**Spec:** `HRM/.plans/pxk-reimport-reexport/design.md` (đọc kèm plan này).

## Global Constraints

- **KHÔNG migration mới**: `warehouse_reimports`, `warehouse_reimport_lots`, `warehouse_reimport_lot_details`, `warehouse_reimport_tabs`, `warehouse_reimport_tab_products` và cột `warehouse_exports.parent_warehouse_export_id` **đã tồn tại** trong `erp_hrm_check` (verify tinker phiên trước + quy tắc gộp-DB: tái dùng bảng ERP). Chỉ tạo entity.
- **Bám ERP 1:1** cho nghiệp vụ; dữ liệu lưu phải đúng y ERP. Chỉ thị nền: rủi ro/lỗi cũng OK miễn giống ERP.
- **PHP 7.4**: KHÔNG `?->`, named args, constructor property promotion, enum.
- **Permission mới** `guard = api`, khai ở `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (KHÔNG seeder riêng, KHÔNG migration). Không tự gán cho role cũ.
- **Nhãn** "Người tạo"/"Ngày tạo" (cấm "Người lập"/"Ngày lập"); thông báo lấy nguyên văn bộ QLDA.
- **KHÔNG push** tới khi user yêu cầu; commit LOCAL trên `develop`. KHÔNG `git add -A`/`git add .` (chỉ path tường minh). KHÔNG sửa ERP (read-only). KHÔNG đụng WIP `ProductExportController.php` (status M của đồng đội).
- **KHÔNG sửa `PhysicalStockWriter`** (service dùng chung với Finance) — chỉ GỌI. Nếu buộc phải đổi → dừng, hỏi user.
- Trailer commit: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

### Rulings (quyết định đã chốt, không hỏi lại)

- **R1 — Không migration** (lý do ở Global Constraints). Entity extends `BaseModel` của Assign, khai `$guarded = []` (giống `WarehouseExport`).
- **R2 — Scope Xuất lại** = bám đúng năng lực luồng tạo PXK HRM hiện có: lots + details + `syncTabs` + chặn "không xuất quá tồn" + `exportStock` (trừ tồn) + `send` + copy field cha + `parent_warehouse_export_id` + lật trạng thái. **BỎ** (vì PXK gốc HRM chưa có): trips giao hàng, bốc xếp/thuê xe (`arrange_delivery`/`executors`), `syncPackages`, attachments PDF required, `checkInventory` (đang kiểm kho). Để sau cùng với việc nâng cấp PXK gốc.
- **R3 — Net-về-0**: `WarehouseReImport::updateWarehouse` truyền ctx `company_id = $this->warehouse_export->company_id`, `warehouse_id = $this->warehouse_export->warehouse_id`, `import_qty = lô gốc->export_qty`, `unit_coefficient = 1`, `details[].qty` theo đơn vị kho (đã quy sẵn), `lot_class`/`detail_class` = FQN ERP của **WarehouseReImportLot/WarehouseReImportLotDetail** (polymorphic objectable_type bám ERP `get_class($lot)`).
- **R4 — Không đổi PhysicalStockWriter**: khác biệt `qty_before` log (`importLot` :118 không lọc `type=NHAP_THUONG`) chỉ ảnh hưởng cột hiển thị log, không ảnh hưởng tồn thực → chấp nhận, không sửa service chung.

## Review Focus

- **Net-về-0 theo company**: lập PXK (trừ tồn) → từ chối → Nhập lại (cộng tồn) ⇒ `stocks.total_qty`, `stock_of_companies.qty`, `stock_positions.qty`, `stock_position_details.qty` trở về **đúng baseline** trước khi lập PXK, kể cả pool `company_id`. → Test Task 2.
- **Gate tuần tự**: Nhập lại chặn khi PXK.status≠4; Xuất lại chặn khi PXK.status≠5 hoặc chưa có phiếu Nhập lại → trả lỗi, không ghi gì. → Test Task 3 + Task 5.
- **`import_qty = export_qty`**: cộng đúng lượng ĐÃ xuất (không phải qty đặt). → Test Task 2/3.
- **Chặn "xuất quá tồn" ở Xuất lại**: sau hoàn tồn, `qty*coef > stock_position_detail.qty` → rollback. → Test Task 5.
- **Phân quyền cấp + ẩn nháp người khác** ở danh sách Nhập lại; Super Admin/tổng công ty không bị bó company_id. → Test Task 4.

---

## Task 1: Entity WarehouseReImport (+4 con) + gate trên WarehouseExport

**Files:**
- Create: `Modules/Assign/Entities/Warehouse/WarehouseReImport.php`
- Create: `Modules/Assign/Entities/Warehouse/WarehouseReImportLot.php`
- Create: `Modules/Assign/Entities/Warehouse/WarehouseReImportLotDetail.php`
- Create: `Modules/Assign/Entities/Warehouse/WarehouseReImportTab.php`
- Create: `Modules/Assign/Entities/Warehouse/WarehouseReImportTabProduct.php`
- Modify: `Modules/Assign/Entities/Warehouse/WarehouseExport.php` (thêm `canReImport`, `canReExport`, quan hệ `reImport()`)
- Test: `Modules/Assign/Tests/Feature/ReImportEntityTest.php`

**Interfaces:**
- Produces: `WarehouseReImport` (table `warehouse_reimports`): const `STATUS_CHO_XUAT_LAI=2`, `STATUS_DA_XUAT_LAI=1`; `$guarded=[]`; quan hệ `warehouseExport()` belongsTo `WarehouseExport` (`warehouse_export_id`), `products()` hasMany `WarehouseReImportLot` (`parent_id`), `tabs()` hasMany `WarehouseReImportTab` (`parent_id`), `creator()`; method `generateCode()`, `canView()`, `canReExport()`, `updateWarehouse()` (Task 2).
- Produces: `WarehouseReImportLot` (`warehouse_reimport_lots`, `details()` hasMany `WarehouseReImportLotDetail` qua `parent_id`), `WarehouseReImportLotDetail` (`warehouse_reimport_lot_details`), `WarehouseReImportTab` (`warehouse_reimport_tabs`, method `syncTabProducts(array)`), `WarehouseReImportTabProduct` (`warehouse_reimport_tab_products`).
- Produces: `WarehouseExport::canReImport()` = `($this->created_by == Auth::id() || Auth::user()->hasRole('Super Admin')) && $this->status == self::KHONG_DUYET` (4); `WarehouseExport::canReExport()` = `(...) && $this->status == self::STATUS_DA_NHAP_LAI` (5).

- [ ] **Step 1: Đọc mẫu entity sẵn có.** Đọc `Modules/Assign/Entities/Warehouse/WarehouseExport.php` (BaseModel nào, cách khai quan hệ, `syncTabs` :136-167) và `WarehouseExportTab.php`/`WarehouseExportLot.php` để copy đúng base class + style. Đối chiếu cột kỳ vọng với ERP `app/Model/Warehouse/WarehouseReImport.php` + `WarehouseReImportLot.php` + `WarehouseReImportLotDetail.php` + `WarehouseReImportTab.php` + `WarehouseReImportTabProduct.php` (READ-ONLY).

- [ ] **Step 2: Viết test thất bại** `ReImportEntityTest.php`:

```php
public function test_generate_code_has_pnl_prefix_and_relations_resolve()
{
    $pxk = \Modules\Assign\Entities\Warehouse\WarehouseExport::query()
        ->whereNotNull('warehouse_id')->orderByDesc('id')->first();
    if (!$pxk) { $this->markTestSkipped('No PXK on test DB'); }

    $ri = new \Modules\Assign\Entities\Warehouse\WarehouseReImport();
    $ri->code = \Str::random(20);
    $ri->type = $pxk->type;
    $ri->warehouse_export_id = $pxk->id;
    $ri->status = \Modules\Assign\Entities\Warehouse\WarehouseReImport::STATUS_CHO_XUAT_LAI;
    $ri->created_by = $pxk->created_by;
    $ri->save();
    $ri->generateCode();

    $this->assertStringStartsWith('PNL-', $ri->code);
    $this->assertTrue($ri->warehouseExport->is($pxk));
    $this->assertSame(2, (int) $ri->status);
}
```

- [ ] **Step 3: Run test → FAIL** (class not found). Run: `cd hrm-api && php artisan test --filter=ReImportEntityTest`

- [ ] **Step 4: Viết 5 entity.** Header ví dụ `WarehouseReImport`:

```php
<?php
namespace Modules\Assign\Entities\Warehouse;

use Illuminate\Support\Facades\Auth;
// ... BaseModel đúng như WarehouseExport dùng

class WarehouseReImport extends /* BaseModel của Assign */
{
    protected $table = 'warehouse_reimports';
    protected $guarded = [];

    const STATUS_DA_XUAT_LAI = 1;   // đã xuất lại
    const STATUS_CHO_XUAT_LAI = 2;  // chờ xuất lại (vừa nhập lại)

    public function warehouseExport() { return $this->belongsTo(WarehouseExport::class, 'warehouse_export_id'); }
    public function products()        { return $this->hasMany(WarehouseReImportLot::class, 'parent_id'); }
    public function tabs()            { return $this->hasMany(WarehouseReImportTab::class, 'parent_id'); }

    public function generateCode()
    {
        $this->code = 'PNL-' . /* helper sinh mã 5 chữ số như ERP generateCode(5,$id) — tra helper HRM tương đương */ ;
        $this->save();
    }

    public function canView()
    {
        return $this->created_by == Auth::id() || Auth::user()->hasRole('Super Admin');
    }

    public function canReExport()
    {
        return $this->created_by == Auth::id() && $this->status == self::STATUS_CHO_XUAT_LAI;
    }

    // updateWarehouse() — Task 2
}
```

`WarehouseReImportLot`: `$table='warehouse_reimport_lots'`, quan hệ `details()` hasMany `WarehouseReImportLotDetail` (`parent_id`), `parent()` belongsTo `WarehouseReImport`. `WarehouseReImportLotDetail`: `$table='warehouse_reimport_lot_details'`. `WarehouseReImportTab`: `$table='warehouse_reimport_tabs'`, `products()` hasMany `WarehouseReImportTabProduct` (`parent_id`), method `syncTabProducts(array $products)` bám ERP `WarehouseReImportTab::syncTabProducts` (gán `parent_id, warehouse_reimport_id, firm_contract_id, firm_contract_tab_id, firm_contract_tab_combo_product_id, product_id, unit_id, qty`). `WarehouseReImportTabProduct`: `$table='warehouse_reimport_tab_products'`.

> ⚠️ `generateCode` ERP = `"PNL-".generateCode(5, $this->id)`. Tra helper sinh mã của HRM (grep cách `WarehouseExport`/YCXH sinh code) để dùng đúng hàm HRM tương đương, giữ format `PNL-00001`.

- [ ] **Step 5: Thêm gate vào `WarehouseExport.php`**: `canReImport()`, `canReExport()` (chữ ký ở Interfaces) + quan hệ `reImport()` hasOne `WarehouseReImport` (`warehouse_export_id`). Dùng hằng `KHONG_DUYET`(4)/`STATUS_DA_NHAP_LAI`(5) sẵn có.

- [ ] **Step 6: Run test → PASS.** Run: `cd hrm-api && php artisan test --filter=ReImportEntityTest`

- [ ] **Step 7: Commit.**
```bash
git add Modules/Assign/Entities/Warehouse/WarehouseReImport.php Modules/Assign/Entities/Warehouse/WarehouseReImportLot.php Modules/Assign/Entities/Warehouse/WarehouseReImportLotDetail.php Modules/Assign/Entities/Warehouse/WarehouseReImportTab.php Modules/Assign/Entities/Warehouse/WarehouseReImportTabProduct.php Modules/Assign/Entities/Warehouse/WarehouseExport.php Modules/Assign/Tests/Feature/ReImportEntityTest.php
git commit -m "feat(assign): entity WarehouseReImport (+4 con) + gate canReImport/canReExport PXK"
```

---

## Task 2: WarehouseReImport::updateWarehouse() — hoàn tồn (net-về-0)

**Files:**
- Modify: `Modules/Assign/Entities/Warehouse/WarehouseReImport.php` (thêm `updateWarehouse()`)
- Test: `Modules/Assign/Tests/Feature/ReImportUpdateWarehouseTest.php`

**Interfaces:**
- Consumes: `Modules\Finance\Services\PhysicalStockWriter::importLot(array $ctx)` (:38) — ghi `stocks/stock_logs/stock_of_companies/stock_positions/stock_position_logs/stock_position_details/stock_position_of_companies/stock_position_detail_logs`, type `NHAP_THUONG`.
- Produces: `WarehouseReImport::updateWarehouse()` — lặp `$this->products` → gọi `importLot` với ctx R3; bọc `DB::transaction`.

- [ ] **Step 1: Đọc ctx chuẩn.** Đọc `Modules/Assign/Services/WarehouseExportService.php::exportStock()` (:199-237) để copy đúng cách dựng ctx (đặc biệt `company_id => $we->company_id` :216, `warehouse_id => $we->warehouse_id` :215, `lot_class`/`detail_class` :18-19) và đọc `Modules/Finance/Services/PhysicalStockWriter::importLot()` (:38-129) để biết key ctx kỳ vọng.

- [ ] **Step 2: Viết test net-về-0** `ReImportUpdateWarehouseTest.php` (cô lập 1 PXK đã xuất, snapshot tồn trước→chạy updateWarehouse→assert tăng đúng; nếu DB test có sẵn PXK hoàn chỉnh thì dùng, không thì `markTestSkipped`):

```php
use Illuminate\Foundation\Testing\DatabaseTransactions;
// Lấy 1 WarehouseReImportLot mẫu bằng cách: tạo reimport từ 1 PXK status bất kỳ (chỉ copy lô, KHÔNG set status cha),
// snapshot stocks.total_qty + stock_position_details.qty của từng (warehouse, product, position, import_lot),
// gọi $ri->updateWarehouse(), assert mỗi dòng tăng += import_qty / qty*coef.
public function test_update_warehouse_adds_back_exact_exported_qty_per_company_pool() { /* ... */ }
```

- [ ] **Step 3: Run → FAIL.** `php artisan test --filter=ReImportUpdateWarehouseTest`

- [ ] **Step 4: Viết `updateWarehouse()`** bám ERP `WarehouseReImport::updateWarehouse` :184-284 nhưng qua `importLot`:

```php
public function updateWarehouse()
{
    $writer = app(\Modules\Finance\Services\PhysicalStockWriter::class);
    $we = $this->warehouseExport;
    \DB::transaction(function () use ($writer, $we) {
        foreach ($this->products as $lot) {
            $ctx = [
                'warehouse_id' => $we->warehouse_id,
                'company_id'   => $we->company_id, // R3: pool công ty PXK gốc → net-về-0
                'lot' => [
                    'id'               => $lot->id,
                    'product_id'       => $lot->product_id,
                    'import_qty'       => $lot->import_qty,      // = export_qty lô gốc
                    'unit_coefficient' => 1,                      // qty detail đã quy đơn vị kho
                ],
                'details' => $lot->details->map(function ($d) {
                    return ['id' => $d->id, 'position_id' => $d->position_id,
                            'import_lot_id' => $d->import_lot_id, 'qty' => $d->qty];
                })->all(),
                'lot_class'    => 'App\\Model\\Warehouse\\WarehouseReImportLot',
                'detail_class' => 'App\\Model\\Warehouse\\WarehouseReImportLotDetail',
            ];
            $writer->importLot($ctx);
        }
    });
}
```

> ⚠️ Xác nhận key ctx khớp chữ ký thực tế của `importLot` ở Step 1 (tên field `import_lot_id` trong details có bắt buộc không — ERP match SPD theo `import_lot_id`). Nếu `importLot` không nhận `import_lot_id` trong details mà suy theo khác → chỉnh ctx cho khớp, KHÔNG sửa writer.

- [ ] **Step 5: Run → PASS.** `php artisan test --filter=ReImportUpdateWarehouseTest`

- [ ] **Step 6: Commit.**
```bash
git add Modules/Assign/Entities/Warehouse/WarehouseReImport.php Modules/Assign/Tests/Feature/ReImportUpdateWarehouseTest.php
git commit -m "feat(assign): WarehouseReImport::updateWarehouse hoàn tồn qua PhysicalStockWriter (net-về-0 theo company PXK)"
```

---

## Task 3: Service + Controller store Nhập lại + routes

**Files:**
- Create: `Modules/Assign/Services/WarehouseReImportService.php`
- Create: `Modules/Assign/Http/Controllers/Api/V1/WarehouseReImportController.php`
- Modify: `Modules/Assign/Routes/api.php` (thêm group `/assign/warehouse-reimports` + route `createData`)
- Test: `Modules/Assign/Tests/Feature/ReImportStoreTest.php`

**Interfaces:**
- Produces: `WarehouseReImportService::store(WarehouseExport $parent, string $note = null): WarehouseReImport` — port ERP `WarehouseReImportsController@store` :146-220 (tạo reimport status=2, copy lots `import_qty=export_qty`+`warehouse_export_lot_id`, copy details `warehouse_export_lot_detail_id`, copy tabs+`syncTabProducts`, `updateWarehouse()`, `parent->status=5`), transaction.
- Produces: `WarehouseReImportController@store(Request)` (validate `warehouse_export_id` required|exists, `note` nullable|max:255; gate `$parent->canReImport()` → 403-style json), `@createData($pxkId)` (gate canReImport, trả data PXK để dựng form).
- Consumes: `WarehouseExport::canReImport()` (Task 1), `WarehouseReImport::updateWarehouse()` (Task 2).

- [ ] **Step 1: Đọc mẫu.** ERP `WarehouseReImportsController@store` :116-225 + `WarehouseReImportsController@getDataForReImport` :240; HRM `WarehouseExportController@cancel` :222 (pattern transaction + `responseJson`) + `WarehouseExportService` style.

- [ ] **Step 2: Viết test** `ReImportStoreTest.php`:

```php
public function test_store_creates_reimport_flips_pxk_to_5_and_restores_stock()
{
    $pxk = /* PXK trên DB test có status=4 (hoặc ép status=4 trong transaction) + có products */;
    if (!$pxk) { $this->markTestSkipped('No rejected PXK with lots'); }
    \Auth::loginUsingId($pxk->created_by);

    $svc = app(\Modules\Assign\Services\WarehouseReImportService::class);
    $ri = $svc->store($pxk, 'test');

    $this->assertSame(2, (int) $ri->status);
    $this->assertStringStartsWith('PNL-', $ri->code);
    $this->assertSame(5, (int) $pxk->fresh()->status);
    $this->assertSame((float) $pxk->products->sum('export_qty'),
                      (float) $ri->products->sum('import_qty'));
}

public function test_store_blocked_when_pxk_not_rejected()
{
    $pxk = /* PXK status != 4 */;
    \Auth::loginUsingId($pxk->created_by);
    $this->expectException(\Exception::class); // hoặc assert canReImport()===false + service ném/không ghi
    app(\Modules\Assign\Services\WarehouseReImportService::class)->store($pxk);
}
```

- [ ] **Step 3: Run → FAIL.** `php artisan test --filter=ReImportStoreTest`

- [ ] **Step 4: Viết Service `store()`** (port 1:1, field theo ERP :154-217):
  - `new WarehouseReImport`: `code=Str::random(20)`, `type=$parent->type`, `warehouse_export_id=$parent->id`, `note`, `status=2`, `created_by=Auth::id()`; save; `generateCode()`.
  - foreach `$parent->products` → `WarehouseReImportLot` (product_id/product_name/model_id/model_name/unit_id/unit_name/brand_id/brand_name/code/detail_type/qty/unit_coefficient, `import_qty=$lot->export_qty`, `parent_id=$ri->id`, `warehouse_export_lot_id=$lot->id`); foreach `$lot->details` → `WarehouseReImportLotDetail` (product_id/product_name/unit_name/qty/position_id/import_lot_id/position_code, `parent_id=$l->id`, `warehouse_export_lot_detail_id=$d->id`).
  - foreach `$parent->tabs` → `WarehouseReImportTab` + `syncTabProducts($tab->products)`.
  - `$ri->updateWarehouse()`; `$parent->status = 5; $parent->save();`. Tất cả trong `DB::transaction`.

- [ ] **Step 5: Viết Controller** `store` (validate + gate `canReImport` + gọi service + `responseJson('Hàng đã được nhập lại',...)`) và `createData` (gate + trả detail PXK). Route-model-bind hoặc `findOrFail`.

- [ ] **Step 6: Thêm routes** vào `Modules/Assign/Routes/api.php` (group mới, tránh trùng 3 block `/assign/warehouse-exports` sẵn có):
```php
Route::group(['prefix' => '/assign/warehouse-reimports'], function () {
    Route::get('/re-import-data/{pxkId}', [WarehouseReImportController::class, 'createData']);
    Route::post('/', [WarehouseReImportController::class, 'store']);
    // index + show thêm ở Task 4
});
```

- [ ] **Step 7: Run → PASS.** `php artisan test --filter=ReImportStoreTest`

- [ ] **Step 8: Commit.**
```bash
git add Modules/Assign/Services/WarehouseReImportService.php Modules/Assign/Http/Controllers/Api/V1/WarehouseReImportController.php Modules/Assign/Routes/api.php Modules/Assign/Tests/Feature/ReImportStoreTest.php
git commit -m "feat(assign): store Nhập lại (copy lô/tab PXK gốc + hoàn tồn + PXK->5)"
```

---

## Task 4: Danh sách Nhập lại (phân quyền cấp) + show + Resource + permissions + cờ PXK

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/WarehouseReImportController.php` (thêm `index`, `show`)
- Create: `Modules/Assign/Transformers/WarehouseReImportResource.php` (hoặc đúng namespace Resource mà PXK dùng)
- Modify: `Modules/Assign/Transformers/WarehouseExportResource.php` (thêm `is_can_re_import`, `is_can_re_export`)
- Modify: `Modules/Assign/Routes/api.php` (thêm `index`, `/{id}` show)
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (4 quyền "Xem phiếu nhập lại theo …")
- Test: `Modules/Assign/Tests/Feature/ReImportListTest.php`

**Interfaces:**
- Consumes: `PermissionHelper::checkPermissionListWithColumn($query, array $perms, $table, $column)` (:336).
- Produces: `WarehouseReImportController@index` (scopedQuery theo 4 quyền mới, bảng `warehouse_reimports`, cột `created_by`; filter code/status/warehouse_export/created_by/product_name/date; trả resource paginate), `@show` (gate canView). Resource cờ `is_can_re_export`.
- Produces: `WarehouseExportResource` thêm `is_can_re_import` = `$object->canReImport()` tương đương điều kiện trong resource (isCreator||superAdmin && status==4), `is_can_re_export` = (…&& status==5).

- [ ] **Step 1: Đọc mẫu** `WarehouseExportController@index` :48 + `scopedQuery` :29 + `WarehouseExportResource` :13-49 (chỗ set `is_can_edit/is_can_cancel/...` :43-47) + `PermissionsTableSeeder` :1412-1415.

- [ ] **Step 2: Viết test** `ReImportListTest.php` (giả lập user theo phòng → chỉ thấy phiếu trong phạm vi; super admin thấy hết; ẩn phiếu người khác ngoài phạm vi):
```php
public function test_index_scopes_by_permission_level() { /* loginUsingId user thường, assert query không chứa phiếu created_by khác ngoài phạm vi */ }
```

- [ ] **Step 3: Run → FAIL.** `php artisan test --filter=ReImportListTest`

- [ ] **Step 4: Thêm 4 quyền** vào seeder (clone :1412-1415, đổi "xuất kho"→"nhập lại", `group='Phiếu nhập lại'`, `type=8`, sort 1-4). Chạy `php artisan db:seed --class="Modules\\Timesheet\\Database\\Seeders\\PermissionsTableSeeder"` trên LOCAL để seed.

- [ ] **Step 5: Viết `index`** (dùng `checkPermissionListWithColumn(WarehouseReImport::query()->with([...]), ['Xem phiếu nhập lại theo tổng công ty','...công ty','...phòng ban','...bộ phận', true], 'warehouse_reimports', 'created_by')` + filter + resource); **`show`** (gate canView); **Resource** `WarehouseReImportResource` (cột mã PNL-, tên, PXK gốc code, người tạo, ngày tạo, status + label, `is_can_re_export`).

- [ ] **Step 6: Thêm cờ vào `WarehouseExportResource`**: `is_can_re_import`, `is_can_re_export` (dùng biến `$isCreator`/`$isSuperAdmin` + status, giống pattern :43-47). Thêm routes `index` + `/{id}` show vào group `/assign/warehouse-reimports`.

- [ ] **Step 7: Run → PASS.** `php artisan test --filter=ReImportListTest`

- [ ] **Step 8: Commit.**
```bash
git add Modules/Assign/Http/Controllers/Api/V1/WarehouseReImportController.php Modules/Assign/Transformers/WarehouseReImportResource.php Modules/Assign/Transformers/WarehouseExportResource.php Modules/Assign/Routes/api.php Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php Modules/Assign/Tests/Feature/ReImportListTest.php
git commit -m "feat(assign): danh sách Nhập lại phân quyền cấp + 4 quyền xem + cờ is_can_re_import/re_export trên PXK"
```

---

## Task 5: Xuất lại — WarehouseExportService::reExport + controller + routes

**Files:**
- Modify: `Modules/Assign/Services/WarehouseExportService.php` (thêm `reExport(WarehouseExport $parent, array $data): WarehouseExport`)
- Modify: `Modules/Assign/Http/Controllers/Api/V1/WarehouseExportController.php` (thêm `reExportData`, `reExport`)
- Modify: `Modules/Assign/Routes/api.php` (thêm 2 route vào group `/assign/warehouse-exports` block :825)
- Test: `Modules/Assign/Tests/Feature/ReExportTest.php`

**Interfaces:**
- Consumes: `WarehouseExport::canReExport()` (status==5), `WarehouseReImport` (by `warehouse_export_id`), các method build/send sẵn có của `WarehouseExportService` (`buildOfficialLots` :271, `syncTabs`, `exportStock` :199, `send` :346 / `updateAndSend` :240).
- Produces: `WarehouseExportService::reExport($parent, $data)` — tạo PXK con copy field cha (R2) + `parent_warehouse_export_id=$parent->id` + `warehouse_export_request_id`, dựng lô từ `$data['lots']` (chặn "không xuất quá tồn" theo `stock_position_details`), `syncTabs`, nếu `status==2` → `exportStock()` (trừ tồn) + `send()`; set `WarehouseReImport(parent)->status=1`, `$parent->status=6`; transaction.
- Produces: `WarehouseExportController@reExport` (validate `status in 2,3`, `receiver_id` required|exists, `lots` required|array|min:1 + details qty/position_id/import_lot_id; gate `canReExport`), `@reExportData($pxkId)`.

- [ ] **Step 1: Đọc mẫu** ERP `WarehouseExportsController@reExportStore` :1493-1890 (lấy field copy cha :1620-1654, chặn tồn :1806-1835, reimport→1 :1866-1868, parent→6 :1870-1871, status2→updateWarehouse+send :1874-1878) **nhưng áp R2** (bỏ trips/bốc xếp/packages/attachments/checkInventory). HRM `WarehouseExportService::updateAndSend` :240 + `buildOfficialLots` :271 + `exportStock` :199 để tái dùng đúng cách dựng lô + trừ tồn.

- [ ] **Step 2: Viết test** `ReExportTest.php`:
```php
public function test_reexport_creates_child_pxk_deducts_stock_and_flips_statuses()
{
    // Dàn cảnh: PXK status=5 + đã có WarehouseReImport(status=2) cho nó (tạo qua Task 3 từ PXK status 4).
    // snapshot tồn, gọi service reExport với data lots khớp lô reimport, status=2.
    // assert: child->parent_warehouse_export_id == parent->id; tồn GIẢM đúng; reimport->status==1; parent->status==6.
}
public function test_reexport_blocked_when_parent_not_status_5() { /* canReExport false → không ghi */ }
public function test_reexport_rejects_over_stock() { /* qty > stock_position_detail.qty → rollback, tồn nguyên */ }
```

- [ ] **Step 3: Run → FAIL.** `php artisan test --filter=ReExportTest`

- [ ] **Step 4: Viết `reExport()`** trong service (bọc transaction):
  - gate `$parent->canReExport()` → ném/`return` lỗi.
  - `new WarehouseExport` copy: `type, contract_id, wr_service_contract_id, service_contract_id, project_contract_id, firm_contract_id, firm_contract_tab_id, warehouse_export_request_id, customer_*, delivery_place, gara_name, contact_*, warehouse_id, import_warehouse_id, company_id` (giữ company để net), `receiver_id=$data['receiver_id']`, `note`, `status=$data['status']`, `step=STEP_DANG_XUAT`, **`parent_warehouse_export_id=$parent->id`**, `created_by=Auth::id()`.
  - dựng lô bằng chính logic `buildOfficialLots` (tái dùng; chặn "xuất quá tồn" theo `stock_position_details`), `syncTabs($data['tabs'])` nếu có (validate tổng qty tab==tổng lô như ERP :1844-1864).
  - `WarehouseReImport::where('warehouse_export_id',$parent->id)->firstOrFail()->update(['status'=>1])`.
  - `$parent->status = 6; $parent->save();`.
  - nếu `status==2` → `$this->exportStock($child)` + `$this->send($child)`.

> Nếu `buildOfficialLots`/`exportStock`/`send` đang `private` và không gọi lại được cho PXK con → refactor nhẹ thành `protected` hoặc tách method dùng chung TRONG CÙNG service (không đổi hành vi); chạy lại test luồng tạo PXK gốc để chắc không vỡ.

- [ ] **Step 5: Viết Controller** `reExport` (validate R2-scoped + gate + gọi service + responseJson) + `reExportData($pxkId)` (gate + trả data PXK gốc prefill). Thêm routes:
```php
// trong group /assign/warehouse-exports (block :825)
Route::get('/{id}/re-export-data', [WarehouseExportController::class, 'reExportData']);
Route::post('/{id}/re-export', [WarehouseExportController::class, 'reExport']);
```

- [ ] **Step 6: Run → PASS** (+ chạy test luồng tạo PXK gốc cũ nếu có, để chắc refactor không vỡ). `php artisan test --filter=ReExportTest` và `php artisan test --filter=WarehouseExport`

- [ ] **Step 7: Commit.**
```bash
git add Modules/Assign/Services/WarehouseExportService.php Modules/Assign/Http/Controllers/Api/V1/WarehouseExportController.php Modules/Assign/Routes/api.php Modules/Assign/Tests/Feature/ReExportTest.php
git commit -m "feat(assign): Xuất lại PXK (tạo PXK con parent_warehouse_export_id + trừ tồn + reimport->1/PXK->6)"
```

---

## Task 6: FE — danh sách Nhập lại + nút Nhập lại/Xuất lại trên PXK + menu

**Files:**
- Create: `hrm-client/pages/finance/warehouse-reimports/index.vue`
- Modify: `hrm-client/pages/finance/warehouse-exports/index.vue` (row-action `re_import`, `re_export`)
- Modify: `hrm-client/pages/finance/warehouse-exports/_id/index.vue` (nút ở `.export-actionbar__btns`)
- Modify: menu (`components/subsystem-menu/*.js` phù hợp — xác định ở Step 1)

**Interfaces:** API `GET /assign/warehouse-reimports`, `GET /assign/warehouse-reimports/{id}`, cờ `is_can_re_import`/`is_can_re_export` trên item PXK.

- [ ] **Step 1: Đọc skill `erp-to-hrm-screen` + mẫu** `pages/finance/warehouse-exports/index.vue` (getRowActions :336), `warehouse-imports/components/row-actions.js` (:38-50 pattern `re_import/re_export`), và xác định file menu đúng phân hệ (grep link `/finance/warehouse-exports`). Ghi màn mẫu bám theo.
- [ ] **Step 2: Dựng `warehouse-reimports/index.vue`** đủ 4 mixin, `V2BaseSmartFilterPanel` (floating) + `V2BaseDataTable`; cột STT/Mã(PNL-, nuxt-link)/Tên/PXK gốc/Người tạo/Ngày tạo/Trạng thái(V2BaseBadge)/Hành động; sort mặc định ngày tạo desc; `localStorageKey`/`columnScreenKey` duy nhất; `layout: 'default-sidebar'`; ColumnCustomizationModal + loadColumnFields.
- [ ] **Step 3: Thêm row-action** `re_import` (visible `item.is_can_re_import`, điều hướng form tạo Nhập lại) + `re_export` (visible `item.is_can_re_export`, điều hướng form Xuất lại) vào `getRowActions` màn PXK; thêm nút tương ứng ở chi tiết PXK `_id/index.vue` gated `detail.is_can_re_import/re_export` (khớp danh sách).
- [ ] **Step 4: Thêm mục menu** "Phiếu nhập lại" ở phân hệ luồng xuất kho (file menu xác định Step 1), khai `isShow` theo quyền "Xem phiếu nhập lại …"; không đổi nhãn mục có sẵn.
- [ ] **Step 5: Verify Playwright** (http://127.0.0.1:3000): mở danh sách Nhập lại (chụp ảnh so màn PXK), bấm lọc chờ ≥3s; mở màn PXK thấy nút Nhập lại/Xuất lại đúng điều kiện. Không báo xong khi chưa bấm thật.
- [ ] **Step 6: Commit** (path tường minh).

---

## Task 7: FE — form tạo Nhập lại (từ PXK) + màn chi tiết Nhập lại

**Files:**
- Create: `hrm-client/pages/finance/warehouse-reimports/add.vue` (hoặc `_pxkId/create.vue` theo điều hướng Task 6)
- Create: `hrm-client/pages/finance/warehouse-reimports/_id/index.vue` (chi tiết, nút "Xuất lại" gated `is_can_re_export`)

**Interfaces:** `GET /assign/warehouse-reimports/re-import-data/{pxkId}` (prefill), `POST /assign/warehouse-reimports` payload `{warehouse_export_id, note}`.

- [ ] **Step 1: Đọc mẫu** `pages/finance/warehouse-imports/_id/re-export.vue` (form chuẩn: V2BaseFormCard disabled + bảng hàng hóa + note + export-actionbar + BaseConfirmModal) và `warehouse-reexports/_id/index.vue` (màn xem).
- [ ] **Step 2: Dựng form tạo** — thông tin chung disabled (mã PXK gốc, kho, khách hàng), bảng hàng hóa nhập lại (readonly, từ prefill), ô ghi chú validate inline; nút "Nhập lại" (BaseConfirmModal) → POST; thành công → toast QLDA + `$router.push` về danh sách.
- [ ] **Step 3: Dựng màn chi tiết** — card thông tin chung + bảng hàng hóa nhập lại (rowspan theo lô/vị trí); `export-actionbar` nút "Xuất lại" gated `detail.is_can_re_export` (điều hướng form Xuất lại của PXK gốc).
- [ ] **Step 4: Verify Playwright** — tạo 1 Nhập lại từ PXK status 4 thật trên dev; kiểm toast, điều hướng, dữ liệu chi tiết.
- [ ] **Step 5: Commit.**

---

## Task 8: FE — form Xuất lại trên PXK

**Files:**
- Create: `hrm-client/pages/finance/warehouse-exports/_id/re-export.vue`

**Interfaces:** `GET /assign/warehouse-exports/{id}/re-export-data` (prefill), `POST /assign/warehouse-exports/{id}/re-export` payload `{status, receiver_id, note, lots:[{...details}], tabs?}` (R2 — không trips/bốc xếp/packages/attachments).

- [ ] **Step 1: Đọc mẫu** form tạo/sửa PXK hiện có của HRM (`warehouse-exports/_id/edit.vue` / `create.vue`) để tái dùng đúng component bảng lô + chọn vị trí/lô nhập, và `warehouse-imports/_id/re-export.vue` cho khung actionbar.
- [ ] **Step 2: Dựng form Xuất lại** — prefill từ `re-export-data` (lô/vị trí của PXK gốc), chọn người nhận (`receiver_id`), ghi chú, chọn "Lưu nháp"(3)/"Gửi"(2); bảng lô cho sửa qty theo tồn; nút "Xuất lại" (BaseConfirmModal) → POST; chặn "xuất quá tồn" hiển thị lỗi từ BE (`need_refresh`/message). Thành công → toast + về chi tiết/danh sách PXK.
- [ ] **Step 3: Verify Playwright** — PXK đã Nhập lại (status 5) → bấm Xuất lại → gửi → kiểm PXK về 6, phiếu Nhập lại về 1 (xem lại chi tiết), tồn giảm (đối chiếu nếu truy cập được).
- [ ] **Step 4: Commit.**

---

## Self-review (đã chạy khi viết plan)

- **Spec coverage**: §2 trạng thái → Task 1 gate + Task 3/5 flip; §3.2 Nhập lại → Task 1-4; §3.3 Xuất lại → Task 5+8 (R2); §3.4 hoàn tồn → Task 2 (Review Focus net-về-0); §4 FE → Task 6-8; §5 quyền → Task 4; §6 Review Focus → test Task 2/3/4/5; §7 xác minh → đã làm (agent §7), kết quả nạp vào R1-R4 + Interfaces. §8 ngoài phạm vi (in/Excel/trips/bốc xếp) KHÔNG có task — đúng chủ ý.
- **Placeholder**: các `/* ... */` trong test là khung dàn cảnh dữ liệu (test phụ thuộc dữ liệu DB thật local → `markTestSkipped` khi thiếu), không phải logic sản phẩm bỏ ngỏ; mọi field copy/ctx đã liệt kê cụ thể.
- **Type consistency**: `STATUS_CHO_XUAT_LAI=2`/`STATUS_DA_XUAT_LAI=1` dùng nhất quán Task 1/3/5; ctx `importLot` thống nhất Task 2; `canReImport`(status4)/`canReExport`(status5) nhất quán.
- **Review Focus**: 5 mục đều có task test tương ứng (net-về-0 Task 2; gate Task 3/5; import_qty Task 2/3; over-stock Task 5; phân quyền Task 4).

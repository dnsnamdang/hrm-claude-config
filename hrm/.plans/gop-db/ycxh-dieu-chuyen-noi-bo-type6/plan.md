# Xuất điều chuyển kho NỘI BỘ (type 6) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để chạy plan task-by-task. Các step dùng checkbox (`- [ ]`).

**Goal:** Nối điểm còn thiếu phía XUẤT của luồng điều chuyển kho nội bộ (type 6): sau khi hạch toán Phiếu xuất hàng (PXH) type 6, YCXH tự về **Chờ duyệt nhập (14)** và **tự sinh YCNH type 6** ở kho đích — bám ERP `ProductExport::updateWarehouse:1876-1946` 1:1, KHÔNG sinh bút toán (D1).

**Architecture:** Phía nhập (YCNH/ĐNNK/PNK/hạch toán nhập + hoàn trả loại 17) + trừ tồn kế toán (`WarehouseExportAccountingService::updateWarehouse`, type-agnostic) + status 14-19 ĐÃ có sẵn và đã commit. Plan này thêm: (1) hằng `XUAT_DIEU_KHO_NOI_BO = 6` phía xuất; (2) cho type 6 đi nhánh **empty-success** của posting-service (không bút toán); (3) method `finalizeInternalTransferExport()` + đấu vào 2 điểm dispatch finalize của `ProductExportService`. Không màn mới (dùng màn YCXH dùng chung), không migration.

**Tech Stack:** PHP 7.4 / Laravel 8, MySQL `erp_hrm_check` (shared gop_db). Model phía xuất ở `Modules/Assign/Entities/Warehouse/`, model YCNH ở `Modules/Finance/Entities/ProductImportRequest/`. Test: PHPUnit Feature + `DatabaseTransactions`.

**Spec:** `.plans/gop-db/ycxh-dieu-chuyen-noi-bo-type6/design.md` (+ survey ở scratchpad: `erp-type6-internal-transfer-survey.md`, `hrm-import-side-coverage-survey.md`).

## Global Constraints

- **Làm GIỐNG ERP 1:1**, dữ liệu lưu đúng như ERP (`ProductExport::updateWarehouse:1876-1946`). Rủi ro/lỗi cũng theo ERP, không "cải tiến".
- Nhánh `develop` (gop_db) cả 2 repo; làm **LOCAL**, KHÔNG push/merge tới khi user yêu cầu.
- KHÔNG đụng WIP đồng đội: hrm-api `Modules/Assign/Http/Controllers/Api/V1/ProductExportController.php` + `Modules/Assign/Services/CustomerManagerService.php`; hrm-client `pages/finance/product-exports/create.vue`.
- KHÔNG `git add -A`/`git add .` — chỉ add path tường minh. KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`.
- KHÔNG sửa ERP (read-only). Sửa hàm dùng chung → hỏi trước (các task dưới chỉ THÊM nhánh type 6, không đổi hành vi loại khác).
- Test/tinker chỉ chạy LOCAL `erp_hrm_check` (xác minh `grep DB_ .env` trước), bọc `DatabaseTransactions`/transaction+rollback. Production READ-ONLY.
- PHP 7.4: không `?->`, named args, union types, enum, constructor promotion.
- Quyền mới (nếu cần) ở `PermissionsTableSeeder` guard `api`, KHÔNG migration. (Plan này KHÔNG thêm quyền — màn YCXH dùng chung đã có quyền sẵn.)

## Review Focus

- **type 6 chưa khai hằng phía xuất → Reflection/so sánh `=== XUAT_DIEU_KHO_NOI_BO` không bao giờ true** → Task 1 pin hằng; Task 3 test khẳng định branch chạy.
- **posting-service trả `[false, …]` cho type 6 (nhánh `else`) → `postAccounting` ném ValidationException, finalize không bao giờ tới** → Task 2 test khẳng định `getDataProductExportAccounting(type 6)` = `[true, [], '']` + 0 account_detail.
- **YCNH tự sinh lấy kho SAI (lấy `warehouse_id` nguồn thay vì `import_warehouse_id` đích)** → Task 3 test assert `warehouse_id === import_warehouse_id`.
- **created_by/cty-phòng-bộ phận YCNH gán nhầm người lập YCXH thay vì người đang hạch toán** (ERP dùng `Auth` = người thao tác, KHÁC YCNH hoàn trả loại 17) → Task 3 test assert YCNH `created_by === auth()->id()`.
- **supplier_price sai (quên × unit_coefficient)** → Task 3 test assert `supplier_price === export_price × unit_coefficient` từng dòng.

---

### Task 1: Khai hằng `XUAT_DIEU_KHO_NOI_BO = 6` phía xuất

**Files:**
- Modify: `Modules/Assign/Entities/Warehouse/ProductExportRequest.php:40` (ngay sau `const XUAT_KHAC = 99;`)

**Interfaces:**
- Produces: hằng `ProductExportRequest::XUAT_DIEU_KHO_NOI_BO` (= 6) cho Task 2 + Task 3 tham chiếu. `TYPE_NAMES[6]` + `STATUS_CHO_DUYET_NHAP (14)` đã có sẵn (dòng 52, 206) — không đụng.

- [ ] **Step 1: Thêm hằng** — chèn sau dòng 40:

```php
    const XUAT_KHAC          = 99; // Xuất khác — ERP KHÔNG hạch toán
    // Loại điều chuyển (bám ERP ExportModel.php:16). Type 5 (cùng thủ kho) đi WarehouseTransfer có màn riêng;
    // type 6 (nội bộ, khác thủ kho cùng công ty) đi chứng từ thường + tự sinh YCNH type 6 sau hạch toán xuất.
    const XUAT_DIEU_KHO_NOI_BO = 6;
```

- [ ] **Step 2: Kiểm cú pháp** — `php -l Modules/Assign/Entities/Warehouse/ProductExportRequest.php` → `No syntax errors detected`.

- [ ] **Step 3: Commit**

```bash
git add Modules/Assign/Entities/Warehouse/ProductExportRequest.php
git commit -m "feat(ycxh): khai hằng XUAT_DIEU_KHO_NOI_BO=6 phía xuất (điều chuyển kho nội bộ)"
```

---

### Task 2: Cho type 6 đi nhánh empty-success của posting-service (D1 — không bút toán)

**Files:**
- Test: `Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php` (tạo — method `test_posting_type6_returns_empty_success`)
- Modify: `Modules/Assign/Services/ProductExportPostingService.php:468`

**Interfaces:**
- Consumes: `ProductExportRequest::XUAT_DIEU_KHO_NOI_BO` (Task 1).
- Produces: `getDataProductExportAccounting($pxh)` trả `[true, [], '']` khi `$pxh->type === 6` → `postAccounting` đi nhánh rỗng, KHÔNG ném, KHÔNG tạo `account_details`.

- [ ] **Step 1: Viết test FAIL trước** — tạo file test với method khẳng định type 6 ra empty-success. Dùng Reflection gọi thẳng `getDataProductExportAccounting` (private) trên 1 PXH type 6 dựng tối thiểu:

```php
<?php

namespace Modules\Assign\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Warehouse\ProductExport;
use Modules\Assign\Entities\Warehouse\ProductExportRequest;
use Modules\Assign\Services\ProductExportPostingService;

/**
 * Type 6 (Xuất điều chuyển kho nội bộ): phía xuất phải (1) KHÔNG sinh bút toán — posting trả empty-success
 * như loại 12/99 (D1), và (2) sau hạch toán đẩy YCXH về Chờ duyệt nhập (14) + tự sinh YCNH type 6 ở kho đích
 * (ERP ProductExport::updateWarehouse:1876-1946). Trước fix, posting trả [false,…] (nhánh else) → ValidationException.
 */
class Type6InternalTransferExportTest extends TestCase
{
    use DatabaseTransactions;

    public function test_posting_type6_returns_empty_success()
    {
        $pxh = new ProductExport();
        $pxh->type = ProductExportRequest::XUAT_DIEU_KHO_NOI_BO; // 6

        $svc = app(ProductExportPostingService::class);
        $ref = new \ReflectionMethod($svc, 'getDataProductExportAccounting');
        $ref->setAccessible(true);
        [$ok, $accounts, $err] = $ref->invoke($svc, $pxh);

        $this->assertTrue($ok, 'Type 6 phải ra thành công (không bút toán), không rơi nhánh else lỗi.');
        $this->assertSame([], $accounts, 'Type 6 KHÔNG sinh account_detail (D1).');
        $this->assertSame('', $err);
    }
}
```

- [ ] **Step 2: Chạy test → FAIL** — `vendor/bin/phpunit Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php --filter test_posting_type6_returns_empty_success`
  Expected: FAIL — `assertTrue` fail vì type 6 rơi nhánh `else` → `[false, [], 'Loại phiếu xuất 6 không hỗ trợ hạch toán!']`.

- [ ] **Step 3: Thêm type 6 vào nhánh empty-success** — sửa dòng 468:

```php
        } elseif (in_array($type, [ProductExportRequest::XUAT_HANG_GUI, ProductExportRequest::XUAT_KHAC, ProductExportRequest::XUAT_DIEU_KHO_NOI_BO], true)) { // 12 (Xuất hàng gửi) + 99 (Xuất khác) + 6 (Xuất điều chuyển kho nội bộ): ERP KHÔNG sinh bút toán → thành công, accounts rỗng (postAccounting đi nhánh empty()).
            return [true, [], ''];
```

- [ ] **Step 4: Chạy test → PASS** — lệnh như Step 2. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add Modules/Assign/Services/ProductExportPostingService.php Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php
git commit -m "feat(posting): type 6 đi nhánh empty-success (không bút toán, D1) + test"
```

---

### Task 3: `finalizeInternalTransferExport()` + đấu vào 2 điểm dispatch finalize

**Files:**
- Modify: `Modules/Assign/Services/ProductExportService.php` — thêm 2 `use` (dòng 22), đấu dispatch path A (sau dòng 453) + path B (sau dòng 753), thêm private method mới.
- Test: `Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php` (thêm method `test_finalize_advances_ycxh_and_creates_import_request`)

**Interfaces:**
- Consumes: `ProductExportRequest::XUAT_DIEU_KHO_NOI_BO` (Task 1); `ProductExportRequest::STATUS_CHO_DUYET_NHAP` (14, có sẵn); `ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_NOI_BO` (6) + `ProductImportRequest::CHO_DUYET` (2) + `generateCode()` + `saveCreateHistory()` (Finance, có sẵn); `ProductImportRequestDetail` (Finance, có sẵn); `ProductExportRequestService::logStatusChanged()` (cùng namespace, gọi qua `app()`).
- Produces: private `finalizeInternalTransferExport(ProductExport $pxh, int $ycxhId): void` — (1) YCXH→14 + is_completed + log; (2) tạo `ProductImportRequest` type 6 ở `import_warehouse_id`, status 2, currency 'VNĐ', `product_export_id`/`product_export_request_id` trỏ PXH/YCXH, created_by/cty-phòng-bộ phận để boot điền theo người thao tác, KHÔNG `receiver_id` (D4); (3) chi tiết từng dòng PXH, `supplier_price = export_price × unit_coefficient`.

- [ ] **Step 1: Viết test FAIL** — thêm vào class `Type6InternalTransferExportTest` (fixtures dùng product/unit/warehouse/employee thật trên LOCAL, `markTestSkipped` nếu thiếu — bám idiom Phase4Type15WritebackTest):

```php
    public function test_finalize_advances_ycxh_and_creates_import_request()
    {
        // Dữ liệu nền thật trên erp_hrm_check (rollback cuối test nhờ DatabaseTransactions).
        $product = DB::table('products')->whereNotNull('model_id')->whereNotNull('brand_id')->first(['id', 'model_id', 'brand_id', 'code', 'name']);
        $unitId  = $product ? (int) DB::table('product_units')->where('product_id', $product->id)->value('unit_id') : 0;
        if (!$unitId) {
            $unitId = (int) DB::table('units')->value('id');
        }
        $warehouses = DB::table('warehouses')->orderBy('id')->limit(2)->pluck('id')->all();
        $employeeId = (int) DB::table('employees')->whereNotNull('employee_info_id')->value('id');
        if (!$product || !$unitId || count($warehouses) < 2 || !$employeeId) {
            $this->markTestSkipped('Thiếu product/unit/warehouse/employee thật trên DB test để dựng kịch bản type 6.');
        }
        [$srcWh, $dstWh] = [(int) $warehouses[0], (int) $warehouses[1]];

        // Đăng nhập = người HẠCH TOÁN xuất (boot YCNH điền created_by/cty/phòng theo người này — khớp ERP Auth).
        $actor = \Modules\Timesheet\Entities\Employee::find($employeeId);
        $this->actingAs($actor);

        // YCXH type 6 ở trạng thái Đang hạch toán (9) để chứng minh method đẩy lên 14.
        $ycxhId = DB::table('product_export_requests')->insertGetId([
            'type' => ProductExportRequest::XUAT_DIEU_KHO_NOI_BO,
            'status' => ProductExportRequest::STATUS_DANG_HACH_TOAN, // 9
            'code' => 'TEST-YCXH6-' . uniqid(),
            'created_by' => $employeeId,
            'department' => 'Test',
            'warehouse_id' => $srcWh,
            'import_warehouse_id' => $dstWh,
            'is_completed' => 0,
            'created_at' => now(), 'updated_at' => now(),
        ]);

        $pxhId = DB::table('product_exports')->insertGetId([
            'type' => ProductExportRequest::XUAT_DIEU_KHO_NOI_BO,
            'status' => 1,
            'code' => 'TEST-PXH6-' . uniqid(),
            'department' => 'Test', 'employee_phone' => '0900000000', 'employee_email' => 't@t.vn',
            'created_by' => $employeeId,
            'product_export_request_id' => $ycxhId,
            'warehouse_id' => $srcWh,
            'import_warehouse_id' => $dstWh,
            'created_at' => now(), 'updated_at' => now(),
        ]);

        DB::table('product_export_details')->insert([
            'parent_id' => $pxhId,
            'product_id' => (int) $product->id,
            'unit_id' => $unitId,
            'base_unit_id' => $unitId,
            'base_unit_name' => 'ĐV',
            'unit_coefficient' => 2,
            'export_from_prepick' => 0,
            'export_from_stock' => 3,
            'qty' => 3,
            'export_price' => 100000,
            'detail_type' => 0,
            'created_at' => now(), 'updated_at' => now(),
        ]);

        $pxh = ProductExport::find($pxhId);

        $svc = app(\Modules\Assign\Services\ProductExportService::class);
        $ref = new \ReflectionMethod($svc, 'finalizeInternalTransferExport');
        $ref->setAccessible(true);
        $ref->invoke($svc, $pxh, $ycxhId);

        // (1) YCXH → Chờ duyệt nhập (14) + is_completed.
        $ycxh = ProductExportRequest::find($ycxhId);
        $this->assertEquals(ProductExportRequest::STATUS_CHO_DUYET_NHAP, (int) $ycxh->status, 'YCXH type 6 phải về 14 Chờ duyệt nhập.');
        $this->assertEquals(1, (int) $ycxh->is_completed);

        // (2) YCNH type 6 ở kho ĐÍCH, status 2, trỏ đúng PXH/YCXH, created_by = người đang hạch toán.
        $ycnh = DB::table('product_import_requests')->where('product_export_id', $pxhId)->first();
        $this->assertNotNull($ycnh, 'Phải tự sinh YCNH sau hạch toán xuất type 6.');
        $this->assertEquals(6, (int) $ycnh->type);
        $this->assertEquals($dstWh, (int) $ycnh->warehouse_id, 'YCNH lấy kho ĐÍCH = import_warehouse_id.');
        $this->assertEquals(2, (int) $ycnh->status);
        $this->assertEquals('VNĐ', $ycnh->currency);
        $this->assertEquals($ycxhId, (int) $ycnh->product_export_request_id);
        $this->assertEquals($employeeId, (int) $ycnh->created_by, 'created_by = người hạch toán (boot điền auth()->id()).');
        $this->assertNull($ycnh->receiver_id ?? null, 'Type 6 KHÔNG gán receiver_id (D4).');

        // (3) Chi tiết YCNH: 1 dòng, supplier_price = export_price × unit_coefficient = 100000 × 2.
        $details = DB::table('product_import_request_details')->where('parent_id', $ycnh->id)->get();
        $this->assertCount(1, $details);
        $this->assertEqualsWithDelta(200000, (float) $details[0]->supplier_price, 0.001, 'supplier_price = export_price × unit_coefficient.');
        $this->assertEquals(3, (float) $details[0]->qty);
        $this->assertEquals((int) $product->id, (int) $details[0]->product_id);
    }
```

- [ ] **Step 2: Chạy test → FAIL** — `vendor/bin/phpunit Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php --filter test_finalize_advances_ycxh_and_creates_import_request`
  Expected: FAIL — `ReflectionException: Method finalizeInternalTransferExport does not exist`.

- [ ] **Step 3: Thêm 2 `use`** — sau dòng 22 (`use Modules\Finance\Entities\CostDebt;`) của `ProductExportService.php`:

```php
use Modules\Finance\Entities\CostDebt;
use Modules\Finance\Entities\ProductImportRequest\ProductImportRequest;
use Modules\Finance\Entities\ProductImportRequest\ProductImportRequestDetail;
```

- [ ] **Step 4: Đấu dispatch path A** — trong `createFromWarehouseExport`, chèn NGAY SAU block loại 14 (sau dòng 453, trước `}` đóng `if ($isFinalize)`):

```php
                if ((int) $pxh->type === ProductExportRequest::XUAT_BAN_HD_HANG) {
                    $this->finalizeFirmContractExport($pxh, ($req && $req->product_export_request_id) ? (int) $req->product_export_request_id : 0);
                }

                // 9) Loại 6 (Xuất điều chuyển kho nội bộ): YCXH → Chờ duyệt nhập (14) + tự sinh YCNH type 6 ở kho đích.
                //    Port ERP ProductExport::updateWarehouse:1876-1946 (nhánh type 6). KHÔNG bút toán (D1).
                if ((int) $pxh->type === ProductExportRequest::XUAT_DIEU_KHO_NOI_BO) {
                    $this->finalizeInternalTransferExport($pxh, ($req && $req->product_export_request_id) ? (int) $req->product_export_request_id : 0);
                }
```

- [ ] **Step 5: Đấu dispatch path B** — trong `createFromProductExportRequest`, chèn NGAY SAU block loại 15 (sau dòng 753, trước `}` đóng `if ($isFinalize)`):

```php
                if ((int) $pxh->type === ProductExportRequest::XUAT_KM_HD_HANG) {
                    $this->finalizeFirmContractPromotionExport($pxh, (int) $per->id);
                }

                // 10) Loại 6 (Xuất điều chuyển kho nội bộ) — xuất thẳng: YCXH → 14 + tự sinh YCNH type 6 ở kho đích.
                if ((int) $pxh->type === ProductExportRequest::XUAT_DIEU_KHO_NOI_BO) {
                    $this->finalizeInternalTransferExport($pxh, (int) $per->id);
                }
```

- [ ] **Step 6: Thêm private method** — đặt ngay SAU `finalizeGenericExport()` (sau dòng 889, trước docblock `finalizeFirmContractExport`). Bám ERP `ProductExport::updateWarehouse:1876-1946` + idiom gold-ref `ProductImportService::createInternalTransferReturnRequest`:

```php
    /**
     * Side-effect finalize PXH loại 6 (Xuất điều chuyển kho nội bộ). Port ERP ProductExport::updateWarehouse:1876-1946.
     *  (1) YCXH → Chờ duyệt nhập (14) + is_completed (KHÁC loại khác về 5) — ERP :1876-1882.
     *  (2) Tự sinh YCNH (ProductImportRequest) loại 6 ở kho ĐÍCH (import_warehouse_id), status Chờ duyệt (2),
     *      currency 'VNĐ' — ERP :1896-1930. created_by + cty/phòng/bộ phận để boot()::creating HRM điền theo
     *      NGƯỜI ĐANG hạch toán (= ERP Auth), KHÁC YCNH hoàn trả loại 17 vốn giữ theo người lập YCXH. KHÔNG gán
     *      receiver_id (D4 — ERP chỉ bắn notification tới người thao tác, không set receiver trên phiếu).
     *  (3) Chi tiết = TỪNG dòng PXH, supplier_price = export_price × unit_coefficient — ERP :1931-1945.
     * KHÔNG bút toán (getDataProductExportAccounting type 6 trả empty-success — D1).
     */
    private function finalizeInternalTransferExport(ProductExport $pxh, int $ycxhId): void
    {
        if ($ycxhId <= 0) {
            return;
        }
        $ycxh = ProductExportRequest::find($ycxhId);
        if (!$ycxh) {
            return;
        }

        // (1) YCXH → Chờ duyệt nhập (14) + hoàn tất (ghi đè 9 mà cascade đã set).
        $before = (int) $ycxh->status;
        $ycxh->status = ProductExportRequest::STATUS_CHO_DUYET_NHAP; // 14
        $ycxh->is_completed = true;
        $ycxh->save();
        app(ProductExportRequestService::class)->logStatusChanged(
            $ycxh,
            $before,
            'Tự động chuyển do Hoàn tất Phiếu xuất hàng ' . ($pxh->code ?? ('#' . $pxh->id))
        );

        // (2) Tự sinh YCNH loại 6 ở kho ĐÍCH. Info theo người đang hạch toán (boot điền created_by + cty/phòng/bộ phận).
        $actor = auth()->id()
            ? DB::table('employees as e')
                ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
                ->leftJoin('departments as d', 'd.id', '=', 'i.department_id')
                ->where('e.id', auth()->id())
                ->first(['i.telephone', 'i.email', 'd.name as department_name'])
            : null;

        $req = new ProductImportRequest();
        $req->code = 'TMP-' . uniqid();
        $req->type = ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_NOI_BO; // 6
        $req->product_export_request_id = $ycxh->id;
        $req->product_export_id = $pxh->id;
        $req->currency = 'VNĐ';
        $req->warehouse_id = $pxh->import_warehouse_id; // kho ĐÍCH
        $req->status = ProductImportRequest::CHO_DUYET; // 2
        $req->department = $actor ? $actor->department_name : null;
        $req->employee_phone = $actor ? $actor->telephone : null;
        $req->employee_email = $actor ? $actor->email : null;
        // KHÔNG gán created_by/receiver_id: boot()::creating HRM điền created_by + cty/phòng/bộ phận theo
        // người ĐANG thao tác (khớp ERP Auth); type 6 KHÔNG đặt receiver_id (D4).
        $req->save();
        $req->saveCreateHistory(); // mốc "Tạo mới" (YCNH loại 6 tự sinh)
        $req->generateCode();

        // (3) Chi tiết YCNH = từng dòng PXH (ERP lặp $this->products, KHÔNG lọc qty).
        foreach ($pxh->products as $p) {
            $product = DB::table('products')
                ->where('id', $p->product_id)
                ->first(['name', 'model_id', 'brand_id', 'code']);

            $detail = new ProductImportRequestDetail();
            $detail->parent_id = $req->id;
            $detail->product_id = $p->product_id;
            $detail->product_name = $product ? ($product->name ?? '') : '';
            $detail->model_id = $product ? ($product->model_id ?? null) : null;
            $detail->model_name = ($product && $product->model_id)
                ? (string) DB::table('product_models')->where('id', $product->model_id)->value('name')
                : '';
            $detail->unit_id = $p->unit_id;
            $detail->unit_name = (string) DB::table('units')->where('id', $p->unit_id)->value('name');
            $detail->brand_id = $product ? ($product->brand_id ?? null) : null;
            $detail->brand_name = ($product && $product->brand_id)
                ? (string) DB::table('brands')->where('id', $product->brand_id)->value('name')
                : '';
            $detail->code = $product ? ($product->code ?? '') : '';
            $detail->qty = $p->qty;
            $detail->unit_coefficient = $p->unit_coefficient;
            $detail->detail_type = $p->detail_type;
            $detail->supplier_price = (float) $p->export_price * (float) $p->unit_coefficient;
            $detail->save();
        }
    }
```

- [ ] **Step 7: Kiểm cú pháp** — `php -l Modules/Assign/Services/ProductExportService.php` → `No syntax errors detected`.

- [ ] **Step 8: Chạy test → PASS** — `vendor/bin/phpunit Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php`
  Expected: cả 2 method PASS (hoặc `test_finalize…` SKIP nếu DB test thiếu nền — khi đó chạy lại trên LOCAL `erp_hrm_check` đủ data, xem Task 4).

- [ ] **Step 9: Commit**

```bash
git add Modules/Assign/Services/ProductExportService.php Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php
git commit -m "feat(ycxh): finalize type 6 — YCXH→14 + tự sinh YCNH type 6 kho đích (port ERP 1:1)"
```

---

### Task 4: Xác minh end-to-end trên LOCAL `erp_hrm_check` (tinker, transaction + rollback)

**Files:**
- (không sửa code) — chạy script kiểm trên DB LOCAL.

**Interfaces:**
- Consumes: toàn bộ Task 1-3.

- [ ] **Step 1: Xác nhận DB LOCAL** — `grep DB_ .env` phải cho `DB_DATABASE=erp_hrm_check`, `DB_HOST=127.0.0.1`. Nếu khác → DỪNG, không chạy ghi.

- [ ] **Step 2: Chạy toàn bộ test class trên DB LOCAL** (đủ product/unit/warehouse/employee thật nên `test_finalize…` KHÔNG skip):

Run: `vendor/bin/phpunit Modules/Assign/Tests/Feature/Type6InternalTransferExportTest.php`
Expected: 2 passed (posting empty-success + finalize). Nếu `test_finalize…` vẫn SKIP → nền DB thiếu, chuyển Step 3.

- [ ] **Step 3 (chỉ khi test SKIP): tinker kiểm thủ công** — bọc `DB::transaction` + `throw` để rollback, khẳng định đúng 5 điểm Review Focus (YCXH→14+is_completed; YCNH type 6 ở `import_warehouse_id` status 2; `created_by === auth()->id()`; `receiver_id` null; `supplier_price === export_price × unit_coefficient`; `account_details` của PXH = 0). Ghi script vào scratchpad, KHÔNG commit.

- [ ] **Step 4: Báo kết quả** — ghi vào checkpoint: lệnh chạy, số test pass, các assert đã xanh. KHÔNG push/merge.

---

### Task 5 (phase FE): dropdown loại 6 + field kho đích + validate kho nguồn≠đích — màn YCXH dùng chung

> Bổ sung sau khi BE/điểm nối (Task 1-4) xong. Phần FE còn thiếu ở design.md mục 6.3. Brainstorm: **bounded** — chỉ thêm 1 rule validate submit-time vào form sẵn có, dùng đúng pattern `errorFields` + `validate()` của form; không component/màn mới. User duyệt "ok".

**Files:**
- Modify: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` — thêm 1 nhánh validate kho nguồn≠đích trong `validate()`.

**Hiện trạng đã có sẵn (không đụng):** dropdown "Loại yêu cầu" đã phát loại 6 "Xuất điều chuyển kho nội bộ" (BE `ProductExportRequest::getDropdownTypes()` có 6); ô "Kho xuất" (`showWarehouse`) + "Kho nhập" (`v-if="needImportWarehouse"`, computed = `Number(this.form.type) === 6`); `import_warehouse_id` có trong form model, payload (:3580), load initialData (:2988); validate đã bắt required "Vui lòng chọn kho nhập." (:3484).

- [x] **Step 1: Thêm nhánh validate kho nguồn≠đích** — chèn NGAY SAU block required `import_warehouse_id` (:3487), bám ERP `different:warehouse_id` message "Cần chọn khác kho xuất" (`ProductExportRequestsController@store:507`):

```js
            // Loại 6 ĐC nội bộ: kho nhập phải KHÁC kho xuất (bám ERP rule different:warehouse_id,
            // message "Cần chọn khác kho xuất" — ProductExportRequestsController@store:507). BE vẫn
            // chặn lại bằng different + "không thuộc Công ty" (warehouseOfCompanyRule).
            if (this.needImportWarehouse && this.form.import_warehouse_id &&
                Number(this.form.import_warehouse_id) === Number(this.form.warehouse_id)) {
                this.errorFields.import_warehouse_id = 'Cần chọn khác kho xuất.'
                return false
            }
```

- [x] **Step 2: Verify Playwright** (`http://127.0.0.1:3000`) — PASS:
  - Loại 6 "Xuất điều chuyển kho nội bộ" hiện trong dropdown "Loại yêu cầu".
  - Chọn loại 6 → hiện "Kho xuất *", "Kho nhập *", "Vận chuyển *" + bảng "Chi tiết hàng hoá".
  - Kho xuất = Kho nhập (cùng "HP - Hải Phòng") → "Lưu và gửi duyệt" → "Xác nhận" → báo đỏ inline **"Cần chọn khác kho xuất."** dưới Kho nhập; form KHÔNG submit (URL giữ /create).
  - Đổi Kho nhập sang "SG - Kho Sài Gòn" (khác) → submit lại → lỗi kho nguồn≠đích biến mất, validate chuyển sang required kế tiếp **"Vui lòng chọn hình thức vận chuyển."** → kiểm tra khác kho đã qua.
  - BE lưu `import_warehouse_id`: đã phủ bởi phpunit Task 2-4 PASS + payload :3580 (xác nhận cấu trúc).

- [x] **Step 3: Commit (LOCAL)** — `git add` path tường minh, KHÔNG push.

---

## Self-Review (đã chạy khi viết plan)

1. **Spec coverage:** design.md mục 6 "CÒN THIẾU" có 3 mục — (1) hằng type 6 phía xuất = Task 1; (2) điểm nối (auto-sinh YCNH + set 14) = Task 3; (3) posting không bút toán = Task 2 (phát hiện thêm). Mục FE (dropdown loại 6 + field kho đích) design.md mục 6.3 — **tách phase sau** (plan này chỉ phần BE/điểm nối; FE cần brainstorm UI riêng, ghi rõ ở checkpoint).
2. **Placeholder scan:** mọi step có code thật / lệnh thật, không TBD.
3. **Type consistency:** `finalizeInternalTransferExport` ký hiệu nhất quán Task 3 (định nghĩa) ↔ test (reflection) ↔ dispatch (gọi). Hằng `XUAT_DIEU_KHO_NOI_BO`/`STATUS_CHO_DUYET_NHAP`/`NHAP_DIEU_CHUYEN_KHO_NOI_BO`/`CHO_DUYET` khớp nguồn đã verify.
4. **Review Focus:** 5 dòng, mỗi dòng có test ở Task 2/Task 3 pin lại.

> **Phạm vi plan này = BE + điểm nối xuất→nhập (Task 1-4).** FE (thêm loại 6 vào dropdown "Loại phiếu" màn YCXH dùng chung + field `import_warehouse_id` khi type=6 + validate kho nguồn≠đích & cùng công ty) là **phase kế tiếp**, cần brainstorm UI trước (SKILL thắng SPEC về trình bày) — KHÔNG gộp vào plan này.

---

## Checkpoint — 2026-10-22 (HOÀN THÀNH plan, LOCAL)

Vừa hoàn thành: Toàn bộ Task 1-4 (SDD) + vá F1 từ final review.
- Task 1 `5b5515ed6` — hằng `XUAT_DIEU_KHO_NOI_BO=6` phía xuất.
- Task 2 `7ad0749f5` — posting type 6 → empty-success (không bút toán, D1) + test.
- Task 3 `be60983f5` — `finalizeInternalTransferExport` (YCXH→14 + tự sinh YCNH type 6 kho đích) + 2 dispatch + test.
- Task 4 — xác minh LOCAL `erp_hrm_check`: `vendor/bin/phpunit …Type6InternalTransferExportTest.php` PASS.
- Final review (opus) CHANGES_REQUESTED → F1 (thiếu ghi ngược exported_qty/base_exported_qty, bám ERP :1856-1874)
  ĐÃ VÁ `9e40d7c6f`; test 2 pass, 19 assertions (thêm 2 assert cộng dồn). F2 notification = lệch có chủ ý
  (nhất quán finalize anh em) ghi design.md mục 8.

HEAD cuối (hrm-api): `9e40d7c6f`. 4 commit, 4 file (+~255/-1). TẤT CẢ LOCAL trên `develop` — CHƯA push/merge.

Đang làm dở: không.
Bước tiếp theo: chờ user chốt tích hợp (khuyến nghị GIỮ LOCAL tới khi yêu cầu) + phase FE type 6 (brainstorm UI riêng).
Blocked: không.

---

## Checkpoint — 2026-10-22 (Task 5 FE, LOCAL)

Vừa hoàn thành: phase FE type 6 (Task 5) — thêm validate kho nguồn≠đích vào màn YCXH dùng chung.
- FE commit `56f5f492f` (hrm-client) — 1 file `ProductExportRequestForm.vue` (+8), rule submit-time
  trong `validate()` báo "Cần chọn khác kho xuất." khi `import_warehouse_id === warehouse_id`
  (bám ERP `different:warehouse_id`, message khớp ERP). Dropdown loại 6 + field kho nhập đã có sẵn
  từ BE/scaffolding (không đụng).
- Verify Playwright (`http://127.0.0.1:3000`) PASS cả 2 chiều: cùng kho → báo đỏ inline + không submit;
  khác kho → lỗi clear, validate sang required kế tiếp. BE lưu `import_warehouse_id` phủ bởi phpunit
  Task 2-4 + payload :3580.

HEAD cuối: hrm-api `9e40d7c6f` (4 commit) · hrm-client `56f5f492f` (1 commit). TẤT CẢ LOCAL trên
`develop` — CHƯA push/merge.

Đang làm dở: không.
Bước tiếp theo: chờ user chốt tích hợp (khuyến nghị GIỮ LOCAL) + các phase còn lại (type 7 chi nhánh,
notification pass chung, FE phần còn lại nếu user yêu cầu).
Blocked: không.

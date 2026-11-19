# Xuất điều chuyển kho CHI NHÁNH (type 7) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development để implement task-by-task. Steps dùng checkbox (`- [ ]`).

**Goal:** Nối trọn luồng điều chuyển kho chi nhánh (type 7) phía XUẤT — khi hạch toán PXK type 7 thì ghi ngược SL về YCXH, đẩy YCXH→Đã hạch toán(5), set phiếu YC chuyển hàng(PYCCH)→7, và tự sinh YCNH type 7 ở công ty đích — GIỐNG HỆT ERP `ProductExport::updateWarehouse` nhánh type 7.

**Architecture:** Bám khuôn type 6 đã làm (commit develop). Mỗi loại xuất có 1 method finalize riêng trong `ProductExportService`; posting trả empty-success (type 7 KHÔNG bút toán hàng — D1). Thêm `finalizeBranchTransferExport()` + 2 điểm dispatch + 1 nhánh posting + 1 hằng.

**Tech Stack:** PHP 7.4, Laravel 8, MySQL (DB gộp `erp_hrm_check`). PHPUnit + DatabaseTransactions.

**Spec:** `.plans/gop-db/ycxh-dieu-chuyen-chi-nhanh-type7/design.md` (mục 4–5, D1–D6, bẫy #1–#7).

**Nhánh:** cả 2 repo `develop`. **LOCAL** — KHÔNG push/merge tới khi user yêu cầu.

## Global Constraints

- **Làm GIỐNG ERP 1:1**; chỉ LỆCH với ERP mới là lỗi. Dữ liệu lưu đúng như ERP (`ProductExport.php:1857-2010`).
- PHP 7.4: không `?->`, named args, union types, enum, constructor promotion.
- KHÔNG `DB_CONNECTION_SECOND`/`mysql2`. KHÔNG sửa code ERP. KHÔNG tạo migration (cột `import_company_id`/`branch_transfer_coefficient`/`kind_of_import` đã có sẵn trong DB gộp từ ERP).
- Atomic increment khi cộng dồn (`increment()` / `DB::raw('col + x')`) — chống lost-update (bám type 6, memory `erp-borrowsell-lost-update-incident`).
- Hằng, tên method, docblock bám đúng phong cách type 6 (`finalizeInternalTransferExport`).
- Test chạy LOCAL trên `erp_hrm_check` (dùng `DatabaseTransactions`, dữ liệu nền thật, `markTestSkipped` nếu thiếu).
- KHÔNG tạo Notification/Redis trong phase này (bẫy #7 — hoãn chung 1 pass thông báo, nhất quán type 6 F2 "lệch cố ý").

## Review Focus

- **YCXH không có SL thực xuất** (mọi dòng PXH `qty=0`): PYCCH VẪN set 7, YCXH VẪN về 5+is_completed, nhưng KHÔNG sinh YCNH (ERP `:1954-1957` return sớm SAU khi set PYCCH=7 và SAU khi `:1876-1882` đã set YCXH=5). → Task 3 test riêng.
- **import_company_id lấy nhầm công ty**: phải = công ty NGƯỜI LẬP YCXH (đích), KHÔNG phải công ty người đang hạch toán, KHÔNG phải công ty nguồn. → Task 3 assert.
- **YCNH type 7 KHÔNG set `warehouse_id`** (khác type 6 set `import_warehouse_id`); phải set `received_time`, `is_import_direct` theo `kind_of_import`. → Task 3 assert.
- **branch_transfer_coefficient NULL/0**: ERP nhân thẳng `× $this->branch_transfer_coefficient`; nếu NULL → supplier_price = 0. Bám ERP (coi NULL như ERP coi: phép nhân với null = 0). → Task 3 dùng hệ số thật >0, ghi chú bẫy.
- **posting type 7 trước fix rơi nhánh else** → `[false,…,'...không hỗ trợ hạch toán!']` → ValidationException chặn hạch toán. → Task 2 test empty-success.

---

### Task 1: Hằng `XUAT_DIEU_CHUYEN_KHO_CHI_NHANH = 7`

**Files:**
- Modify: `Modules/Assign/Entities/Warehouse/ProductExportRequest.php:43` (ngay dưới `const XUAT_DIEU_KHO_NOI_BO = 6;`)

**Interfaces:**
- Produces: `ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` (= 7) — dùng ở Task 2, 3.

> Hiện code type 7 phía xuất dùng literal `7` (survey mục 1). Thêm hằng tên để Task 2/3 tham chiếu, bám ERP `ExportModel.php:17 const XUAT_DIEU_CHUYEN_KHO_CHI_NHANH = 7`. TYPE_NAMES[7] đã có sẵn — KHÔNG đụng.

- [ ] **Step 1: Thêm hằng**

```php
    const XUAT_DIEU_KHO_NOI_BO = 6;
    const XUAT_DIEU_CHUYEN_KHO_CHI_NHANH = 7; // nguồn: phiếu YC chuyển hàng (product_transfer_requests), KHÁC công ty
```

- [ ] **Step 2: Verify** — `php -l Modules/Assign/Entities/Warehouse/ProductExportRequest.php` → `No syntax errors`.

- [ ] **Step 3: Commit**

```bash
git add Modules/Assign/Entities/Warehouse/ProductExportRequest.php
git commit -m "feat(type7): them hang XUAT_DIEU_CHUYEN_KHO_CHI_NHANH=7 phia xuat"
```

---

### Task 2: Posting type 7 → empty-success (KHÔNG bút toán — D1)

**Files:**
- Modify: `Modules/Assign/Services/ProductExportPostingService.php:468` (thêm `XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` vào `in_array`)
- Test: `Modules/Assign/Tests/Feature/Type7BranchTransferExportTest.php` (tạo mới)

**Interfaces:**
- Consumes: `ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` (Task 1).
- Produces: `getDataProductExportAccounting(ProductExport)` trả `[true, [], '']` cho type 7.

> ERP type 7: `getDataCreateDept` không có nhánh → `$accounts=[]` → posting empty-success, giống 6/12/99 (D1). Hiện HRM rơi nhánh `else` → `[false,…]`.

- [ ] **Step 1: Viết test fail (mới tạo file test)**

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
 * Type 7 (Xuất điều chuyển kho CHI NHÁNH): phía xuất (1) KHÔNG sinh bút toán — posting empty-success (D1),
 * (2) finalize đẩy YCXH→5+is_completed, PYCCH→7, tự sinh YCNH type 7 ở cty ĐÍCH (ERP ProductExport:1857-2010).
 */
class Type7BranchTransferExportTest extends TestCase
{
    use DatabaseTransactions;

    public function test_posting_type7_returns_empty_success()
    {
        $pxh = new ProductExport();
        $pxh->type = ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH; // 7

        $svc = app(ProductExportPostingService::class);
        $ref = new \ReflectionMethod($svc, 'getDataProductExportAccounting');
        $ref->setAccessible(true);
        [$ok, $accounts, $err] = $ref->invoke($svc, $pxh);

        $this->assertTrue($ok, 'Type 7 phải thành công (không bút toán), không rơi nhánh else lỗi.');
        $this->assertSame([], $accounts, 'Type 7 KHÔNG sinh account_detail (D1).');
        $this->assertSame('', $err);
    }
}
```

- [ ] **Step 2: Chạy test → FAIL**

Run: `php artisan test --filter=test_posting_type7_returns_empty_success`
Expected: FAIL — `$ok` là false, `$err` = `'Loại phiếu xuất 7 không hỗ trợ hạch toán!'`.

- [ ] **Step 3: Thêm type 7 vào in_array**

Tại `:468` sửa:

```php
        } elseif (in_array($type, [ProductExportRequest::XUAT_HANG_GUI, ProductExportRequest::XUAT_KHAC, ProductExportRequest::XUAT_DIEU_KHO_NOI_BO, ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH], true)) { // 12 + 99 + 6 + 7 (ĐC kho chi nhánh): ERP KHÔNG sinh bút toán → empty-success (D1).
            return [true, [], ''];
```

- [ ] **Step 4: Chạy test → PASS**

Run: `php artisan test --filter=test_posting_type7_returns_empty_success`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add Modules/Assign/Services/ProductExportPostingService.php Modules/Assign/Tests/Feature/Type7BranchTransferExportTest.php
git commit -m "feat(type7): posting type 7 empty-success (khong but toan - D1) + test"
```

---

### Task 3: `finalizeBranchTransferExport()` + 2 điểm dispatch + test

**Files:**
- Modify: `Modules/Assign/Services/ProductExportService.php` — thêm method `finalizeBranchTransferExport()` (sau `finalizeInternalTransferExport`, ~:1018) + 2 nhánh dispatch (sau `:459` và sau `:765`).
- Modify (test): `Modules/Assign/Tests/Feature/Type7BranchTransferExportTest.php` — thêm `test_finalize_advances_ycxh_sets_transfer_requests_and_creates_import_request` và `test_finalize_no_real_export_skips_import_request`.

**Interfaces:**
- Consumes: `ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH`, `::STATUS_DA_HACH_TOAN` (5); `ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH` (7), `::CHO_DUYET` (2); `ProductTransferRequest`.
- Produces: `finalizeBranchTransferExport(ProductExport $pxh, int $ycxhId): void`.

> Port ERP `ProductExport::updateWarehouse`:
> - `:1857-1874` ghi ngược exported_qty/base_exported_qty (vòng chung mọi loại) — type 7 KHÔNG gắn HĐ nên khóa các cột liên kết NULL (bám đúng `finalizeInternalTransferExport`).
> - `:1876-1882` nhánh `else`: YCXH→**5** (Đã hạch toán) + is_completed (type 7 đi nhánh else, KHÁC type 6 =14).
> - `:1948-1952` set MỌI `product_transfer_requests`→7.
> - `:1954-1957` `hasRealExport` = có dòng PXH `qty>0`; nếu KHÔNG → return (PYCCH đã =7, YCXH đã =5, KHÔNG sinh YCNH).
> - `:1959-1998` YCNH type 7: `product_export_id`, `product_export_request_id`, currency VNĐ, `import_company_id` = cty NGƯỜI LẬP YCXH (đích), status 2, `received_time`=now, **KHÔNG** `warehouse_id`, `is_import_direct`=1 nếu `kind_of_import==1`; chi tiết/dòng: `supplier_price = export_price × unit_coefficient × branch_transfer_coefficient`.
> - `:2001-2009` Notification → **HOÃN** (bẫy #7, nhất quán type 6). created_by YCNH do boot điền theo người hạch toán.

- [ ] **Step 1: Viết 2 test fail**

Thêm vào `Type7BranchTransferExportTest.php` (dùng chung khuôn dựng data của `Type6InternalTransferExportTest::test_finalize_...`). Dựng: YCXH type 7 (status 9, `created_by`=NV đích, `kind_of_import`=2), 1 PXH type 7 (`branch_transfer_coefficient`=1.5), 1 dòng PXH (qty=3, export_qty=6, export_price=100000, unit_coefficient=2), 1 PERD (qty=10, exported_qty=5, base_exported_qty=10), 2 bản `product_transfer_requests` (status 1, `product_export_request_id`=YCXH). Đăng nhập = người hạch toán (actingAs TpEmployee guard api).

Test A `test_finalize_advances_ycxh_sets_transfer_requests_and_creates_import_request`:
```php
$ref = new \ReflectionMethod($svc, 'finalizeBranchTransferExport');
$ref->setAccessible(true);
$ref->invoke($svc, $pxh, $ycxhId);

// (0) ghi ngược cộng dồn
$perd = DB::table('product_export_request_details')->where('id', $perdId)->first();
$this->assertEquals(8, (float) $perd->exported_qty);      // 5+3
$this->assertEquals(16, (float) $perd->base_exported_qty); // 10+6

// (1) YCXH → 5 (KHÁC type 6 =14) + is_completed
$ycxh = ProductExportRequest::find($ycxhId);
$this->assertEquals(ProductExportRequest::STATUS_DA_HACH_TOAN, (int) $ycxh->status);
$this->assertEquals(1, (int) $ycxh->is_completed);

// (2) MỌI product_transfer_requests → 7
$statuses = DB::table('product_transfer_requests')->where('product_export_request_id', $ycxhId)->pluck('status');
foreach ($statuses as $s) { $this->assertEquals(7, (int) $s); }
$this->assertCount(2, $statuses);

// (3) YCNH type 7 ở cty ĐÍCH, KHÔNG warehouse_id, có received_time, supplier_price × hệ số chi nhánh
$ycnh = DB::table('product_import_requests')->where('product_export_id', $pxhId)->first();
$this->assertNotNull($ycnh);
$this->assertEquals(7, (int) $ycnh->type);
$this->assertEquals(2, (int) $ycnh->status);
$this->assertEquals('VNĐ', $ycnh->currency);
$this->assertEquals($ycxhId, (int) $ycnh->product_export_request_id);
$this->assertEquals($destCompanyId, (int) $ycnh->import_company_id); // = company_id của NV lập YCXH
$this->assertNull($ycnh->warehouse_id, 'YCNH type 7 KHÔNG set warehouse_id (khác type 6).');
$this->assertNotNull($ycnh->received_time);
$details = DB::table('product_import_request_details')->where('parent_id', $ycnh->id)->get();
$this->assertCount(1, $details);
// supplier_price = export_price × unit_coefficient × branch_transfer_coefficient = 100000 × 2 × 1.5
$this->assertEqualsWithDelta(300000, (float) $details[0]->supplier_price, 0.001);
```

Test B `test_finalize_no_real_export_skips_import_request` — dòng PXH `qty=0`:
```php
// PYCCH vẫn 7, YCXH vẫn 5+is_completed, nhưng KHÔNG sinh YCNH
$ref->invoke($svc, $pxh0, $ycxhId0);
$this->assertEquals(ProductExportRequest::STATUS_DA_HACH_TOAN, (int) ProductExportRequest::find($ycxhId0)->status);
$this->assertEquals(7, (int) DB::table('product_transfer_requests')->where('product_export_request_id', $ycxhId0)->value('status'));
$this->assertNull(DB::table('product_import_requests')->where('product_export_id', $pxhId0)->first());
```

- [ ] **Step 2: Chạy → FAIL** (`finalizeBranchTransferExport` chưa tồn tại → ReflectionException/method not found).

Run: `php artisan test --filter=Type7BranchTransferExportTest`

- [ ] **Step 3: Thêm method `finalizeBranchTransferExport`** (sau `finalizeInternalTransferExport`):

```php
    /**
     * Side-effect finalize PXH loại 7 (Xuất điều chuyển kho CHI NHÁNH). Port ERP ProductExport::updateWarehouse:
     *  (0) Ghi ngược exported_qty/base_exported_qty về chi tiết YCXH — ERP :1857-1874 (vòng chung mọi loại).
     *  (1) YCXH → ĐÃ HẠCH TOÁN (5) + is_completed — ERP :1876-1882 nhánh else (KHÁC type 6 =14).
     *  (2) MỌI product_transfer_requests (PYCCH) → 7 — ERP :1948-1952.
     *  (3) hasRealExport: nếu KHÔNG có dòng PXH qty>0 → return (PYCCH đã =7, YCXH đã =5, KHÔNG sinh YCNH) — ERP :1954-1957.
     *  (4) Tự sinh YCNH loại 7 ở cty ĐÍCH: import_company_id = cty NGƯỜI LẬP YCXH; status 2; VNĐ; received_time=now;
     *      KHÔNG warehouse_id; is_import_direct=1 nếu kind_of_import==1; supplier_price = export_price × unit_coefficient
     *      × branch_transfer_coefficient — ERP :1959-1998. created_by do boot điền theo người hạch toán (ERP Auth).
     * KHÔNG bút toán (posting type 7 empty-success — D1). Notification HOÃN (bẫy #7, nhất quán type 6 F2).
     */
    private function finalizeBranchTransferExport(ProductExport $pxh, int $ycxhId): void
    {
        if ($ycxhId <= 0) {
            return;
        }
        $ycxh = ProductExportRequest::find($ycxhId);
        if (!$ycxh) {
            return;
        }

        // (0) Ghi ngược SL đã xuất về chi tiết YCXH — ERP :1857-1874 (type 7 KHÔNG gắn HĐ → khóa cột liên kết NULL).
        foreach ($pxh->products as $p) {
            $qty  = (float) $p->qty;
            $base = (float) $p->export_qty;
            if ($qty <= 0 && $base <= 0) {
                continue;
            }
            $perdId = DB::table('product_export_request_details')
                ->where('parent_id', $ycxhId)
                ->where('product_id', $p->product_id)
                ->where('unit_id', $p->unit_id)
                ->where('detail_type', $p->detail_type)
                ->whereNull('service_contract_item_product_id')
                ->whereNull('order_import_detail_id')
                ->whereNull('inland_notify_detail_id')
                ->whereNull('rule_inland_notify_detail_id')
                ->whereNull('project_contract_tab_product_id')
                ->whereNull('firm_contract_tab_product_id')
                ->whereNull('wr_service_contract_item_id')
                ->value('id');
            if (!$perdId) {
                continue;
            }
            DB::table('product_export_request_details')->where('id', $perdId)->increment('exported_qty', $qty, [
                'base_exported_qty' => DB::raw('base_exported_qty + ' . $base),
            ]);
        }

        // (1) YCXH → ĐÃ HẠCH TOÁN (5) + is_completed (ERP nhánh else :1878-1882).
        $before = (int) $ycxh->status;
        $ycxh->status = ProductExportRequest::STATUS_DA_HACH_TOAN; // 5
        $ycxh->is_completed = true;
        $ycxh->save();
        app(ProductExportRequestService::class)->logStatusChanged(
            $ycxh,
            $before,
            'Tự động chuyển do Hoàn tất Phiếu xuất hàng ' . ($pxh->code ?? ('#' . $pxh->id))
        );

        // (2) MỌI phiếu YC chuyển hàng (PYCCH) → 7 (ERP :1948-1952).
        DB::table('product_transfer_requests')->where('product_export_request_id', $ycxhId)->update(['status' => 7]);

        // (3) hasRealExport (ERP :1954-1957): không có dòng thực xuất → dừng, KHÔNG sinh YCNH.
        $hasRealExport = false;
        foreach ($pxh->products as $p) {
            if ((float) $p->qty > 0) {
                $hasRealExport = true;
                break;
            }
        }
        if (!$hasRealExport) {
            return;
        }

        // (4) YCNH loại 7 ở cty ĐÍCH. import_company_id = cty NGƯỜI LẬP YCXH (đích).
        $destCompanyId = DB::table('employees as e')
            ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
            ->where('e.id', (int) $ycxh->created_by)
            ->value('i.company_id');

        $actor = auth()->id()
            ? DB::table('employees as e')
                ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
                ->leftJoin('departments as d', 'd.id', '=', 'i.department_id')
                ->where('e.id', auth()->id())
                ->first(['i.telephone', 'i.email', 'd.name as department_name'])
            : null;

        $req = new ProductImportRequest();
        $req->code = 'TMP-' . uniqid();
        $req->type = ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH; // 7
        $req->product_export_request_id = $ycxh->id;
        $req->product_export_id = $pxh->id;
        $req->currency = 'VNĐ';
        $req->import_company_id = $destCompanyId; // cty đích = cty người lập YCXH (KHÔNG warehouse_id)
        $req->status = ProductImportRequest::CHO_DUYET; // 2
        $req->received_time = now();
        $req->department = $actor ? $actor->department_name : null;
        $req->employee_phone = $actor ? $actor->telephone : null;
        $req->employee_email = $actor ? $actor->email : null;
        if ((int) $ycxh->kind_of_import === 1) {
            $req->is_import_direct = 1; // nhập thẳng
        }
        // KHÔNG gán created_by/receiver_id: boot()::creating HRM điền created_by + cty/phòng/bộ phận theo người hạch toán.
        $req->save();
        $req->saveCreateHistory();
        $req->generateCode();

        $coefficient = (float) $pxh->branch_transfer_coefficient; // ERP nhân thẳng; NULL → 0 (bám ERP)
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
            $detail->supplier_price = (float) $p->export_price * (float) $p->unit_coefficient * $coefficient;
            $detail->save();
        }
    }
```

- [ ] **Step 4: Thêm 2 nhánh dispatch** — ngay sau khối type 6 (`:457-459` và `:763-765`), thêm:

```php
                // 10) Loại 7 (Xuất điều chuyển kho CHI NHÁNH): YCXH→5+is_completed, PYCCH→7, tự sinh YCNH type 7 cty đích.
                //     Port ERP ProductExport::updateWarehouse:1948-2010. KHÔNG bút toán (D1).
                if ((int) $pxh->type === ProductExportRequest::XUAT_DIEU_CHUYEN_KHO_CHI_NHANH) {
                    $this->finalizeBranchTransferExport($pxh, ($req && $req->product_export_request_id) ? (int) $req->product_export_request_id : 0);
                }
```

(ở điểm thứ 2 quanh `:765` dùng `(int) $per->id` thay cho `$req->product_export_request_id` — bám đúng mẫu type 6 tại chỗ đó.)

- [ ] **Step 5: Chạy → PASS**

Run: `php artisan test --filter=Type7BranchTransferExportTest`
Expected: 3 test PASS (hoặc skipped nếu DB test thiếu nền — ghi rõ lý do skip).

- [ ] **Step 6: Verify `php -l`** cho `ProductExportService.php`.

- [ ] **Step 7: Commit**

```bash
git add Modules/Assign/Services/ProductExportService.php Modules/Assign/Tests/Feature/Type7BranchTransferExportTest.php
git commit -m "feat(type7): finalizeBranchTransferExport (ghi nguoc + YCXH 5 + PYCCH 7 + sinh YCNH type 7 cty dich) + 2 dispatch + test"
```

---

## PHASE B — NHẬP đóng vòng type 7 (điểm nối NHẬP)

**Mục tiêu:** mở loại 7 ở luồng Phiếu nhập hàng (`ProductImportService` + entity `ProductImport`) để lập/hoàn thành phiếu nhập điều chuyển chi nhánh, đóng PYCCH đúng mốc ERP (→8 duyệt YCNH, →11 lập phiếu nhập hàng) và gỡ mốc →9 lệch; xử lý cả 2 đường non-direct (qua kho) và nhập thẳng. Bám ERP 1:1 (`App\Model\Warehouse\ProductImport::updateWarehouse()` :1795-1806 + `ProductImportRequest::approve()` :1549-1560).

**Base HEAD develop khi bắt đầu Phase B: `ba65bbe44` (LOCAL — sau merge code đồng đội 2026-10-23; trước merge là `7c00ea709`).** Giữ LOCAL trên `develop`, KHÔNG push/merge tới khi user chốt.

**⚠️ Số dòng tái verify post-merge (remote đụng 2/4 file):** ProductImportService.php shift → buildDetailsByType case NOI_BO `:1292`, resolveAccountingService case NOI_BO `:1551`, editableTypes NOI_BO `:290`. WarehouseImportWriteService.php shift → block →9 lệch `:839-841`. ProductImport.php entity + WarehouseImportRequestService.php KHÔNG đổi (số dòng dưới đây đúng nguyên). Anchor thật = ngữ cảnh code (case/method), implementer grep xác nhận trước khi sửa.

**⚠️ HÀM DÙNG CHUNG — ĐÃ FLAG USER:** Task B4 GỠ nhánh type-7 `→9` trong `WarehouseImportWriteService::approveRequest()` (hàm dùng chung cho mọi loại nhập). Chỉ đụng **nhánh `if type===7`** (xoá hẳn), KHÔNG chạm nhánh type 6 / nhánh chung. Trình diff cho user review TRƯỚC khi chạy SDD.

**Hằng dùng xuyên Phase B:**
- `ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH = 7` (entity :74), lặp ở `ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH = 7`.
- `ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO = 6` (mốc tham chiếu — type 7 bám theo nhóm type 6).
- `ProductImport::ERP_IMPORT_DETAIL_TYPE = 'App\\Model\\Warehouse\\ProductImportDetail'` (entity :98).
- PYCCH (`product_transfer_requests`) status: 8 = Đang nhập kho, 11 = Đã nhập hàng.

**Chuỗi quan hệ tới PYCCH từ `ProductImport` (đọc bằng Query Builder — entity KHÔNG có quan hệ trực tiếp):**
`ProductImport.product_import_request_id` → `product_import_requests.product_export_request_id` → `product_export_requests.id` → `product_transfer_requests.product_export_request_id`.

---

### LÁT A — non-direct (qua kho)

### Task B1: Mở `buildDetailsByType` + `resolveAccountingService` + `editableTypes` cho type 7

Gom 3 sửa cùng file (`ProductImportService.php`), cùng shape "thêm type 7 vào nhóm type 6", review 1 lượt.

**Files:**
- Modify: `Modules/Finance/Services/ProductImportService.php` (3 chỗ: ~:1292, ~:1551, ~:290 — post-merge)

**Interfaces:**
- Consumes: entity const `ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH`, `OtherProductImportAccountingService` (đã tồn tại, type 6 đang dùng).
- Produces: `store()`/`handleCompleted()` chấp nhận type 7 (không còn ném 422 ở builder/accounting/update).

- [ ] **Step 1: `buildDetailsByType` — thêm case type 7 vào nhóm `buildDetailsFromSource`**

Tại `case ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO:` (dòng ~:1292, ngay trước `$this->buildDetailsFromSource(...)` :1293), thêm dòng case type 7 ngay trên nó:

```php
            case ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH: // 7 — cùng builder type 6 (lấy từ nguồn YCNH)
            case ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO:
                $this->buildDetailsFromSource($productImport, $parent, $lots, $sourcePir);
                break;
```

> KHÔNG sửa `buildDetailsFromSource()`: type 7 ∉ `ProductImport::KHAC` → rơi nhánh `else` (:2760-2761) lấy `$reqProduct->supplier_price` — giá này đã = `export_price × unit_coef × hệ số chi nhánh` do Phase A ghi vào YCNH detail. Đúng ERP (`ProductImportsController:641-648`: type 7 chung nhánh NOI_BO/MUON_TRA_LAI → `$req_product->supplier_price`).

- [ ] **Step 2: `resolveAccountingService` — thêm case type 7 vào nhóm `OtherProductImportAccountingService`**

Tại nhóm case kết thúc bằng `case ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO:` (dòng ~:1551, ngay trước `return app(\Modules\Finance\Services\OtherProductImportAccountingService::class);` :1552), thêm:

```php
            // #type7 — Nhập điều chuyển kho chi nhánh (7): ERP getDataCreateDept() KHÔNG có case 7 (lẫn 6)
            // → rơi `else` cuối (ProductImport.php:2381-2392) = CHỈ bút toán bốc xếp thuê ngoài (rent_type==2).
            // Phiếu HRM lập tay KHÔNG có tab bốc-hạ → service trả [] (empty-success), y hệt type 6. KHÔNG tạo service rỗng mới.
            case ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH:
            case ProductImport::KHAC:
            case ProductImport::MUON_TRA_LAI:
            case ProductImport::NHAP_GUI:
            case ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO:
                return app(\Modules\Finance\Services\OtherProductImportAccountingService::class);
```

> Chỉ THÊM 1 dòng `case ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH:` vào đầu nhóm hiện có (KHAC/MUON_TRA_LAI/NHAP_GUI/NOI_BO :1548-1551) + cập nhật comment. KHÔNG đổi các case khác.

- [ ] **Step 3: `editableTypes` — thêm type 7 (parity type 6, cho sửa nháp)**

Tại mảng `$editableTypes` (:280-291), thêm sau `ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO,`:

```php
            ProductImport::NHAP_DIEU_CHUYEN_KHO_NOI_BO,
            // #type7 — Nhập điều chuyển kho chi nhánh (loại tự sinh, vào form qua "Chọn phiếu nhập kho"), cho sửa nháp như type 6.
            ProductImport::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH,
```

- [ ] **Step 4: Verify `php -l Modules/Finance/Services/ProductImportService.php`** → No syntax errors.

- [ ] **Step 5: Commit**

```bash
git add Modules/Finance/Services/ProductImportService.php
git commit -m "feat(type7-import): mo loai 7 o buildDetailsByType + resolveAccountingService (Other, empty-success) + editableTypes (parity type 6)"
```

---

### Task B2: PYCCH →8 khi duyệt YCNH (`createFromImportRequest`)

**Files:**
- Modify: `Modules/Finance/Services/WarehouseImportRequestService.php` (:196 vùng `createFromImportRequest`)
- Test: `Modules/Finance/Tests/Feature/Type7BranchTransferImportTest.php` (tạo mới — xem Task B6 cho fixture dùng chung; test PYCCH→8 có thể gộp vào B6)

**Interfaces:**
- Consumes: `ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH`, `$req->product_export_request_id`.
- Produces: khi lập ĐNNK từ YCNH type 7 → mọi `product_transfer_requests` của YCXH gốc chuyển status 8.

- [ ] **Step 1: Thêm block PYCCH→8 ngay sau khi set YCNH→7 (port ERP `ProductImportRequest::approve()` :1555-1559)**

Sau khối set `$req->status` (dòng :194-201, sau cả nhánh `if ($status === STATUS_CHO_DUYET)`), thêm:

```php
            // #type7 — Duyệt YCNH điều chuyển chi nhánh (lập ĐNNK) = ERP ProductImportRequest::approve() :1555-1559:
            // đẩy MỌI product_transfer_requests của YCXH gốc → 8 (Đang nhập kho). ERP KHÔNG đụng PYCCH ở bước duyệt ĐNNK.
            if ((int) $req->type === ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH && $req->product_export_request_id) {
                DB::table('product_transfer_requests')
                    ->where('product_export_request_id', $req->product_export_request_id)
                    ->update(['status' => 8, 'updated_at' => Carbon::now()]);
            }
```

> `DB` và `Carbon` đã import trong file (kiểm đầu file; `createFromImportRequest` đã dùng cả hai). Nếu thiếu → thêm `use`.

- [ ] **Step 2: Verify `php -l`** → No syntax errors.

- [ ] **Step 3: Commit**

```bash
git add Modules/Finance/Services/WarehouseImportRequestService.php
git commit -m "feat(type7-import): PYCCH ->8 khi duyet YCNH type 7 (createFromImportRequest = ERP approve)"
```

---

### Task B3: Entity `ProductImport::updateWarehouse()` — type-7 branch: PYCCH →11 (non-direct)

**Files:**
- Modify: `Modules/Finance/Entities/ProductImport/ProductImport.php` (thêm nhánh type 7 trước khi đóng `updateWarehouse()` tại :932, trước dòng `    }` :933)

**Interfaces:**
- Consumes: `$this->product_import_request_id`, bảng `product_import_requests`/`product_export_requests`/`product_transfer_requests`.
- Produces: khi hoàn thành (status DA_HOAN_THANH) Phiếu nhập hàng type 7 → mọi PYCCH của YCXH gốc → 11. accounting_stocks đã ghi ở block type-agnostic (:618-681) trước đó — nhánh này KHÔNG lặp lại.

- [ ] **Step 1: Thêm nhánh type 7 (PYCCH→11, non-direct) ngay sau block `MUA_HANG_TRONG_NUOC` (:932), trước `}` đóng method (:933)**

```php
        // #type7 — Nhập điều chuyển kho chi nhánh (7): đóng vòng PYCCH. Port ERP
        // `App\Model\Warehouse\ProductImport::updateWarehouse()` :1795-1800: MỌI product_transfer_requests
        // của YCXH gốc → 11 (Đã nhập hàng). Chuỗi quan hệ đọc bằng Query Builder (entity không có quan hệ trực tiếp).
        if ((int) $this->type === self::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH) {
            $perId = $this->product_import_request_id
                ? DB::table('product_import_requests')->where('id', $this->product_import_request_id)->value('product_export_request_id')
                : null;
            if ($perId) {
                DB::table('product_transfer_requests')
                    ->where('product_export_request_id', $perId)
                    ->update(['status' => 11, 'updated_at' => Carbon::now()]);

                // LÁT B — nhập thẳng: xem Task B5 (chèn vào CHÍNH nhánh này).
            }
        }
```

> `DB` và `Carbon` đã import trong entity (các block trên dùng rồi). Đặt đúng trong thân `updateWarehouse()`, SAU block `MUA_HANG_TRONG_NUOC` (:899-932), KHÔNG lồng vào block khác.

- [ ] **Step 2: Verify `php -l Modules/Finance/Entities/ProductImport/ProductImport.php`** → No syntax errors.

- [ ] **Step 3: Commit**

```bash
git add Modules/Finance/Entities/ProductImport/ProductImport.php
git commit -m "feat(type7-import): updateWarehouse type-7 branch PYCCH ->11 (non-direct, = ERP :1795-1800)"
```

---

### Task B4: GỠ mốc PYCCH →9 lệch ở `approveRequest` (⚠️ HÀM DÙNG CHUNG — đã flag user)

**Files:**
- Modify: `Modules/Finance/Services/WarehouseImportWriteService.php` (:839-841 post-merge, chỉ nhánh `if type===7`)

**Interfaces:**
- Consumes: không có gì mới.
- Produces: duyệt ĐNNK (tạo PNK) type 7 KHÔNG còn đụng PYCCH (khớp ERP — ERP chỉ đụng PYCCH ở approve YCNH + lập phiếu nhập hàng).

- [ ] **Step 1: XOÁ hẳn nhánh type-7 →9 (:839-841 post-merge)**

Xoá nguyên block:

```php
        $per = $pir->product_export_request_id ? DB::table('product_export_requests')->where('id', $pir->product_export_request_id)->first() : null;
        if ((int) $wir->type === ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH && $per) {
            DB::table('product_transfer_requests')->where('product_export_request_id', $per->id)->update(['status' => 9, 'updated_at' => Carbon::now()]);
        }
        if ((int) $wir->type === ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_NOI_BO && $per
```

> **CẨN THẬN:** `$per` còn được nhánh type 6 (`NHAP_DIEU_CHUYEN_KHO_NOI_BO`) dùng NGAY SAU. KHÔNG xoá dòng gán `$per`. Chỉ xoá đúng 3 dòng `if (... NHAP_DIEU_CHUYEN_KHO_CHI_NHANH ...) { ...status=9... }`. Kết quả mong muốn — giữ `$per` + giữ nguyên nhánh type 6:

```php
        $per = $pir->product_export_request_id ? DB::table('product_export_requests')->where('id', $pir->product_export_request_id)->first() : null;
        // #type7 — GỠ mốc PYCCH→9 (ERP KHÔNG đụng product_transfer_requests lúc duyệt ĐNNK; mốc đúng là
        // →8 ở duyệt YCNH (createFromImportRequest) và →11 ở lập phiếu nhập hàng (ProductImport::updateWarehouse)).
        if ((int) $wir->type === ProductImportRequest::NHAP_DIEU_CHUYEN_KHO_NOI_BO && $per
            && (int) $per->type === self::PER_TYPE_XUAT_DIEU_KHO_NOI_BO) {
            DB::table('product_export_requests')->where('id', $per->id)
                ->update(['status' => self::PER_STATUS_DANG_NHAP_KHO_NHAP, 'updated_at' => Carbon::now()]);
        }
```

- [ ] **Step 2: Cập nhật docblock method `approveRequest` (docblock :818-822; mệnh đề ở :820)** — bỏ mệnh đề "loại 7: YC điều chuyển → 9" cho khớp hành vi mới (ERP không đụng PYCCH ở bước này).

- [ ] **Step 3: Verify `php -l`** → No syntax errors.

- [ ] **Step 4: Commit**

```bash
git add Modules/Finance/Services/WarehouseImportWriteService.php
git commit -m "fix(type7-import): go moc PYCCH ->9 lech o approveRequest (ERP khong dung PYCCH luc duyet DNNK)"
```

---

### LÁT B — nhập thẳng (is_import_direct)

### Task B5: Entity `updateWarehouse()` type-7 branch — nhánh nhập thẳng (`productImportDirectDetail`)

**Files:**
- Modify: `Modules/Finance/Entities/ProductImport/ProductImport.php` (bên trong nhánh type-7 của Task B3, chỗ comment "LÁT B")

**Interfaces:**
- Consumes: `$this->is_import_direct`, `$this->products` (ProductImportDetail), `productImportDirectDetail($detail, int $employeeId, string $objectableType)` (:1051, đã có), `self::ERP_IMPORT_DETAIL_TYPE`.
- Produces: khi phiếu nhập hàng type 7 **nhập thẳng** hoàn thành → ghi `product_import_direct_details` + log cho từng dòng hàng, employee = người lập PYCCH đầu tiên. ĐNNK/PNK KHÔNG lập ở đường nhập thẳng (block non-direct :602-616 đã guard `!is_import_direct`). accounting_stocks vẫn ghi (block :618-681 chạy mọi đường).

- [ ] **Step 1: Thay dòng comment "// LÁT B — nhập thẳng: xem Task B5" trong nhánh type-7 (Task B3) bằng khối nhập thẳng (port ERP :1801-1805)**

```php
                // LÁT B — nhập thẳng (is_import_direct): ghi product_import_direct_details theo người lập
                // PYCCH đầu tiên (ERP :1801-1805 `$product_export_request->product_transfer_requests[0]->created_by`).
                if ($this->is_import_direct) {
                    $firstPycchCreatedBy = DB::table('product_transfer_requests')
                        ->where('product_export_request_id', $perId)
                        ->orderBy('id')
                        ->value('created_by');
                    if ($firstPycchCreatedBy) {
                        foreach ($this->products as $p) { // ProductImportDetail
                            $this->productImportDirectDetail($p, (int) $firstPycchCreatedBy, self::ERP_IMPORT_DETAIL_TYPE);
                        }
                    }
                }
```

> Khối này nằm TRONG `if ($perId) { ... }` của nhánh type-7 (Task B3), NGAY SAU update PYCCH→11. `productImportDirectDetail` đã tồn tại (:1051), chữ ký `($detail, int $employeeId, string $objectableType)`, tự tính `qty = qty × unit_coefficient` + `department_id` từ `employee_infos`. KHÔNG sửa hàm đó.

- [ ] **Step 2: Verify `php -l`** → No syntax errors.

- [ ] **Step 3: Commit**

```bash
git add Modules/Finance/Entities/ProductImport/ProductImport.php
git commit -m "feat(type7-import): updateWarehouse nhanh nhap thang - productImportDirectDetail theo PYCCH[0].created_by (= ERP :1801-1805)"
```

---

### Task B6: Test đóng vòng nhập type 7 (non-direct + nhập thẳng)

**Files:**
- Create: `Modules/Finance/Tests/Feature/Type7BranchTransferImportTest.php`

**Interfaces:**
- Consumes: toàn bộ B1-B5. Fixture bám khuôn `Modules/Assign/Tests/Feature/Type7BranchTransferExportTest.php` (DatabaseTransactions; chọn product có model_id/brand_id, unit thật, 2 employee khác company).

- [ ] **Step 1: Dựng fixture + 4 test (DatabaseTransactions)**

Bám đúng pattern file export-side. Các test bắt buộc:

1. `test_resolve_accounting_service_type7_returns_other_empty_success` — reflection gọi `resolveAccountingService(7)` trả về instance `OtherProductImportAccountingService` (không ném 422); `->build($productImportType7KhongCoTabBocXep)` trả `[]`.
2. `test_approve_ycnh_type7_sets_transfer_requests_to_8` — dựng YCNH type 7 có `product_export_request_id` + ≥2 PYCCH status 7; gọi `createFromImportRequest` (hoặc trực tiếp path tạo ĐNNK) → mọi PYCCH = 8; `approveRequest` (tạo PNK) sau đó KHÔNG đổi PYCCH (vẫn 8) — chốt mốc →9 đã gỡ.
3. `test_complete_import_type7_non_direct_sets_pycch_11_and_writes_accounting_stock` — Phiếu nhập hàng type 7 `is_import_direct=0`, status DA_HOAN_THANH, có detail_accountings → `updateWarehouse()`: mọi PYCCH → 11; có `accounting_stock_logs` type=1; KHÔNG ghi `product_import_direct_details`.
4. `test_complete_import_type7_direct_writes_direct_detail_by_first_pycch_creator` — `is_import_direct=1` → `updateWarehouse()`: PYCCH → 11; `product_import_direct_details` có dòng với `employee_id` = created_by của PYCCH đầu (orderBy id); `qty` = `detail.qty × unit_coefficient`; KHÔNG lập ĐNNK/PNK.

> Thiếu dữ liệu nền (product/unit/employee) → `markTestSkipped` như file export-side. Gọi method protected/private qua `ReflectionMethod::setAccessible(true)`.

- [ ] **Step 2: Chạy test**

```bash
php artisan test --filter=Type7BranchTransferImportTest
```
Expected: PASS (hoặc SKIP nếu DB test thiếu nền — ghi rõ trong report).

- [ ] **Step 3: Commit**

```bash
git add Modules/Finance/Tests/Feature/Type7BranchTransferImportTest.php
git commit -m "test(type7-import): dong vong nhap type 7 - PYCCH 8/11 + accounting_stock + nhap thang direct_detail"
```

---

### Review Focus — Phase B (5 input/failure dễ cắn, pin test ở task sở hữu)

1. **PYCCH mồ côi / YCNH thiếu `product_export_request_id`** → B2/B3 guard `if ($req->product_export_request_id)` / `if ($perId)`: không có thì bỏ qua, KHÔNG ném. (Test 2/3 có nhánh perId null = no-op.)
2. **Nhập thẳng mà PYCCH rỗng** (không có bản ghi) → B5 guard `if ($firstPycchCreatedBy)`: bỏ qua ghi direct_detail, không fatal. (Test 4 phủ nhánh có; nhánh không = assert không crash.)
3. **`recomputeMoneyServerSide()` với type 7** — chạy sau buildDetailsFromSource như type 6. Type 7 cùng nhóm builder type 6 → hành vi giống; nếu recompute có switch loại trừ type 7 phải phát hiện ở B1 review (grep `recomputeMoneyServerSide` xem có `in_array($this->type, [...])` thiếu 7). Pin: B1 Step 4 kèm 1 lần chạy `store()` type 7 thử (hoặc note review).
4. **Idempotency** — `updateWarehouse()` chỉ chạy ở status DA_HOAN_THANH; đổi status 1 lần → PYCCH→11 chạy 1 lần. Nếu luồng gọi updateWarehouse 2 lần (lưu lại phiếu đã hoàn thành) → PYCCH set 11 lại (vô hại) nhưng direct_detail GHI LẶP. Review B5: xác nhận HRM không re-complete (handleCompleted chỉ chạy khi status===DA_HOAN_THANH lần chuyển, bám type 6). Ghi ruling nếu phát hiện khác.
5. **Hàm dùng chung B4** — sau khi gỡ →9, nhánh type 6 ở `approveRequest` phải NGUYÊN VẸN ($per còn dùng). Pin: B4 review đọc lại cả method, xác nhận type 6 + nhánh chung không đổi hành vi.

---

### Checkpoint — 2026-10-23
Vừa hoàn thành: **Phase B (nhập đóng vòng type 7) XONG — B1→B6 code + test + review hết.** 5 commit LOCAL trên `develop` (hrm-api): `678d6b22c` B1 (ProductImportService: buildDetailsByType + resolveAccountingService=Other + editableTypes) · `9eccacd4f` B2 (WarehouseImportRequestService: PYCCH→8 khi duyệt YCNH) · `08ddb6607` B3+B5 (ProductImport::updateWarehouse: PYCCH→11 + nhập thẳng productImportDirectDetail theo PYCCH[0].created_by) · `a940b0cce` B4 (GỠ mốc PYCCH→9 lệch ở approveRequest — HÀM DÙNG CHUNG, chỉ xoá nhánh type 7, giữ $per + nhánh type 6) · `ef86ae82f` B6 (Type7BranchTransferImportTest 4 test PASS/18 assertion).
  - SDD: mỗi task 1 fresh implementer + task review (SPEC+QUALITY đều ✅). **Final whole-branch review (opus): APPROVED** — data GIỐNG ERP, 0 lệch-ERP làm sai; 8/8 trọng tâm ✅; grep toàn repo chỉ còn 3 điểm ghi product_transfer_requests.status (→7/→8/→11), KHÔNG còn →9.
  - Chạy test: `vendor/bin/phpunit Modules/Finance/Tests/Feature/Type7BranchTransferImportTest.php` → OK (4 tests, 18 assertions). LƯU Ý: `php artisan test --filter` ra "No tests executed" vì phpunit.xml chỉ quét ./tests.
Đang làm dở: không có — Phase B đóng.
Bước tiếp theo: **CHỜ user chốt integration** (push develop vs GIỮ LOCAL — khuyến nghị GIỮ LOCAL như các phase trước). Sau đó: Phase C (PPBHĐC→12 + màn phân bổ), Phase D (DeliveryTrip cost + in %VAT + biên bản), Phase E (FE rà), Phase A-prepick (cần spike).
Blocked: không.

---

# PHASE C — PPBHĐC (Phân bổ hàng điều chuyển chi nhánh, type 7)

> **Spec:** `design-phaseC.md` (đọc trước). Quyết định user: **A/A/A** (nút trên chi tiết Phiếu nhập hàng · gate bằng method entity, không quyền mới · làm trọn FE).
> **Nguồn ERP 1:1** (read-only): `ERP/TanPhatDev/app/Model/Warehouse/TransferProductAllocation.php` + `app/Http/Controllers/Warehouse/TransferProductAllocationsController.php` + `ProductImport.php:578-608,892-898`.
> **Bảng `transfer_product_allocations` + `_details` ĐÃ có trong DB chung → KHÔNG migration.**

## Global Constraints (Phase C)
- LOCAL trên `develop` (hrm-api). KHÔNG push/merge. KHÔNG `git add -A`/`.` — chỉ add file của task.
- KHÔNG đụng WIP đồng đội (`Modules/Assign/Http/Controllers/Api/V1/ProductExportController.php`, `Modules/Assign/Services/CustomerManagerService.php`, client `product-exports/create.vue`).
- KHÔNG sửa ERP. PHP 7.4 (không `?->`/named args/enum). Số định dạng quốc tế. Nhãn "Người tạo/Ngày tạo".
- **KHÔNG thêm quyền mới** — gate bằng method entity (`canCreate`/`canView`/`canEdit`), bám tiền lệ `ProductTransferRequest` (route KHÔNG `checkPermission`, lý do model_type mismatch — docblock controller :22).
- Prepick CHỈ ghi qua `PrepickStockService::addLot(...)` — KHÔNG tự `new PrepickDetail`.
- Notification/Redis: **HOÃN** (gộp pass F2, nhất quán Phase A/B — lệch cố ý, ghi rõ trong code comment).

## Review Focus (Phase C)
1. **company_id prepick = `product_import->company_id` (ĐÍCH)** — KHÔNG lấy từ PTR/PXK (nguồn). Test phải assert company_id của prepick_details = cty phiếu nhập.
2. **status=12 set cho MỌI PTR của PXK** (không chỉ dòng được phân bổ) — test ≥2 PYCCH, 1 không có dòng phân bổ, vẫn →12.
3. **`+= allocate_qty` KHÔNG idempotent** — chặn duyệt lại bằng guard `canEdit` (status==3). Test: phiếu status==1 (đã duyệt) gọi update → bị chặn, allocated_qty KHÔNG cộng lần 2.
4. **validateDetails khớp CHÍNH XÁC** `min(group.qty-group.allocated_qty, lot.qty)` — test under/over đều `false`.
5. **prepick_qty = allocate_qty × `WarehouseImportLot.unit_coefficient`** (lô theo `product_import.warehouse_import_id` + product + unit) — test assert đúng hệ số.

---

### Task C1: Entity TransferProductAllocation + Detail + helper trên ProductImport

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/TransferProductAllocation/TransferProductAllocation.php`
- Create: `hrm-api/Modules/Finance/Entities/TransferProductAllocation/TransferProductAllocationDetail.php`
- Modify: `hrm-api/Modules/Finance/Entities/ProductImport/ProductImport.php` (thêm 2 method: `canCreateTransferProductAllocation()`, `getDataForTransferProductAllocation($id)`)

**Interfaces (dữ kiện ĐÃ khảo sát 2026-10-23 — dùng thẳng, KHÔNG đoán lại):**
- Produces: `TransferProductAllocation` với quan hệ `product_import()` (belongsTo `Modules\Finance\Entities\ProductImport\ProductImport`, `product_import_id`), `details()` (hasMany `TransferProductAllocationDetail`, `parent_id`), `product_export_request()` (belongsTo **`Modules\Finance\Entities\ProductImportRequest\ProductExportRequest`** `product_export_request_id` — CHÍNH là class mà `ProductImportRequest::product_export_request()` :925-928 trỏ tới), `employee_create()` (belongsTo `Modules\Human\Entities\Employee` qua `created_by`, bám `ProductTransferRequest::employee_create`). Const `ERP_TRANSFER_ALLOCATION_DETAIL_TYPE = 'App\\Model\\Warehouse\\TransferProductAllocationDetail'`. Method `generateCode()`, `canView()`, `canEdit()`, `validateDetails($products)`, `syncDetails($products)`, `approve()` (C2).
- `TransferProductAllocationDetail` `$fillable`: `parent_id, product_id, employee_id, allocate_qty, prepick_qty, expire_date, customer_id, request_id, detail_id`.
- Consumes: `ProductImport` (đã có `warehouse_import_id`, `company_id`, `created_by`, `is_import_direct`, `product_import_request_id`, const `NHAP_DIEU_CHUYEN_KHO_CHI_NHANH=7`, const status hoàn thành — xác minh tên, Phase B dùng `DA_HOAN_THANH`); `WarehouseImportLot` (`Modules\Finance\Entities\WarehouseImport\WarehouseImportLot`, `$guarded=['id']`); `ProductTransferRequest/Product/ProductDetail`.

- [ ] **Step 1: 2 entity map bảng sẵn có** (extends `Illuminate\Database\Eloquent\Model` — bám `WarehouseImportLot`/`ProductTransferRequestProduct`, bảng ERP port KHÔNG dùng BaseModel). `$table` đúng tên; quan hệ như trên; `generateCode()`:
```php
public function generateCode(): void {
    // generateCode($len,$value) ĐÃ port — app/Helper/FormatHelper.php:97-105 (zero-pad). Khuôn: ProductImport::generateCode() :372-376.
    $this->code = 'PPBHĐC-' . generateCode(5, $this->id);
    $this->save();
}
public function canView() {
    $uid = optional(auth()->user())->id;
    if ($uid == $this->created_by) return true;
    // ERP mở cho 'Kế toán kho' khi status != 3. Dùng CÙNG cách query pivot của ProductTransferRequest
    // (grep ProductTransferRequest cho check 'Kế toán kho' — query thẳng employee_has_roles/role_has_permissions,
    //  KHÔNG dùng spatie hasPermissionTo vì guard/model_type mismatch). Gate thêm (int)$this->status != 3.
    return (int)$this->status != 3 && $this->currentUserHasWarehouseAccountantRole();
}
public function canEdit() {
    return optional(auth()->user())->id == $this->created_by && (int)$this->status == 3;
}
```
> `generateCode($len,$value)` ĐÃ có (FormatHelper.php:97-105). `currentUserHasWarehouseAccountantRole()` = helper private trong chính entity, COPY nguyên cách `ProductTransferRequest` kiểm quyền 'Kế toán kho' (query builder pivot, không spatie) — grep `Kế toán kho` trong `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php` lấy đúng đoạn.

- [ ] **Step 2: `ProductImport::canCreateTransferProductAllocation()`** (port ERP :892-898, 1:1):
```php
public function canCreateTransferProductAllocation() {
    if ((int)$this->type !== self::NHAP_DIEU_CHUYEN_KHO_CHI_NHANH || (int)$this->status !== self::DA_HOAN_THANH
        || optional(auth()->user())->id != $this->created_by || $this->is_import_direct) return false;
    if (TransferProductAllocation::where('product_import_id', $this->id)->exists()) return false;
    return true;
}
```
> ĐÃ khảo sát: `ProductImport::DA_HOAN_THANH = 1` (:50) = "Đã hoàn thành" (khớp ERP status==1). `NHAP_DIEU_CHUYEN_KHO_CHI_NHANH = 7` (:79). Fields `warehouse_import_id/company_id/is_import_direct(bool cast)/product_import_request_id/created_by` đều fillable. Nhớ `use` entity `TransferProductAllocation`.

- [ ] **Step 3: `ProductImport::getDataForTransferProductAllocation($id)`** (port ERP :578-608): ERP `warehouse_import.products` = lô đã nhập → HRM dùng **`$this->warehouse_import->lots`** (`WarehouseImport::lots()` :139-142 hasMany `WarehouseImportLot` theo `parent_id`; KHÔNG có `products()`). Kèm `requests` (ProductTransferRequestProduct của mọi PYCCH của PXK — PYCCH = `ProductTransferRequest` where `product_export_request_id` = PXK; mỗi PTR `->products` + `allocated_qty` + `customers` + `employee_create`) + `product_export_request` (quan hệ mới ở C1) + `product_import` ($this). Mảng thuần như ERP.

- [ ] **Step 4: chạy thử load** — `php artisan tinker` (hoặc 1 unit nhỏ) nạp entity + gọi `canCreateTransferProductAllocation` trên 1 ProductImport type 7 để chắc không lỗi cú pháp/quan hệ. (Nếu không có data nền → chỉ `php -l` + `composer dump-autoload` xác nhận class load.)

- [ ] **Step 5: Commit**
```bash
git add Modules/Finance/Entities/TransferProductAllocation/ Modules/Finance/Entities/ProductImport/ProductImport.php
git commit -m "feat(type7-ppbhdc): entity TransferProductAllocation(+Detail) + ProductImport canCreate/getDataForAllocation

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task C2: validateDetails + syncDetails + approve (ghi allocated_qty + prepick đích + PYCCH→12)

**Files:**
- Modify: `hrm-api/Modules/Finance/Entities/TransferProductAllocation/TransferProductAllocation.php`

**Interfaces:**
- Consumes: `PrepickStockService::addLot(int $productId, int $employeeId, ?int $customerId, ?int $companyId, ?string $expireDate, float $qty, int $documentId, int $detailId, ?string $objectableType=null, ?int $objectableId=null): int`; `WarehouseImportLot`; `ProductTransferRequest/Product/ProductDetail`.
- Produces: `approve()` dùng bởi Service (C3) khi status==1.

- [ ] **Step 1: `validateDetails($products)`** — port ERP :118-156 1:1 (vòng theo product → requests → customers; từng dòng `allocate_qty <= detail.qty - detail.allocated_qty`; tổng SP phải == `min(group.qty-group.allocated_qty, lot.qty)`: `if ($qty > $max || $qty > $lot->qty || ($qty < $max && $qty < $lot->qty)) return false`). `$lot = WarehouseImportLot::where('parent_id',$this->product_import->warehouse_import_id)->where('product_id',$p['product_id'])->where('unit_id',$p['unit_id'])->first();`.

- [ ] **Step 2: `syncDetails($products)`** — port ERP :158-177 1:1 (xóa hết detail cũ, tạo lại, BỎ QUA `allocate_qty == 0`).

- [ ] **Step 3: `approve()`** — port ERP :179-263, THAY khối ghi prepick thủ công bằng `addLot`:
```php
public function approve() {
    foreach ($this->details as $d) {
        if ($d->allocate_qty <= 0) continue;
        $detail = ProductTransferRequestProductDetail::findOrFail($d->detail_id);
        $product = ProductTransferRequestProduct::where('id', $detail->parent_id)
            ->where('product_id', $d->product_id)->firstOrFail();
        $detail->allocated_qty += $d->allocate_qty; $detail->save();
        $product->allocated_qty += $d->allocate_qty; $product->save();

        $lot = WarehouseImportLot::where('parent_id', $this->product_import->warehouse_import_id)
            ->where('product_id', $d->product_id)->where('unit_id', $product->unit_id)->first();
        $prepickQty = (float)$d->allocate_qty * (float)$lot->unit_coefficient;
        $d->prepick_qty = $prepickQty; $d->save();

        // Giữ hàng tại CÔNG TY ĐÍCH (product_import->company_id). Ghi qua service dùng chung.
        app(\Modules\Finance\Services\PrepickStockService::class)->addLot(
            (int)$d->product_id,
            (int)$d->employee_id,                              // người giữ = người lập PYCCH
            $d->customer_id !== null ? (int)$d->customer_id : null,
            $this->product_import->company_id !== null ? (int)$this->product_import->company_id : null,
            $d->expire_date,
            $prepickQty,                                       // ĐV cơ bản (đã × unit_coefficient)
            (int)$d->id,                                       // documentId → prepick_details.objectable_id
            (int)$d->id,                                       // detailId   → prepick_logs.objectable_id
            self::ERP_TRANSFER_ALLOCATION_DETAIL_TYPE,         // FQN ERP cho cả 3 vị trí (mirror ERP root_objectable)
            (int)$d->id
        );
    }
    // status=12 cho TẤT CẢ PYCCH của PXK (ERP :246-249)
    ProductTransferRequest::where('product_export_request_id', $this->product_export_request_id)
        ->update(['status' => 12]);
    // Notification/Redis: HOÃN pass F2 (nhất quán Phase A/B — lệch cố ý).
}
```
> ⚠️ ERP cũng `array_push($change,...)` chỉ để notify — bỏ cùng khối notification. Giữ thứ tự: cộng allocated_qty → ghi prepick → set 12.

- [ ] **Step 4: `php -l`** trên entity. (Test hành vi ở C5.)

- [ ] **Step 5: Commit**
```bash
git add Modules/Finance/Entities/TransferProductAllocation/TransferProductAllocation.php
git commit -m "feat(type7-ppbhdc): approve/validateDetails/syncDetails - allocated_qty + prepick dich (addLot) + PYCCH->12

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task C3: Service + Controller + Routes + FormRequest + cờ is_can_allocate

**Files:**
- Create: `hrm-api/Modules/Finance/Services/TransferProductAllocationService.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/TransferProductAllocationController.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/TransferProductAllocation/StoreTransferProductAllocationRequest.php` (+ Update nếu rule khác — ERP y hệt, có thể dùng chung)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (group `/transfer-product-allocations`)
- Modify: `hrm-api/Modules/Finance/Transformers/ProductImportResource/ProductImportDetailResource.php` (resource trả bởi `ProductImportController::show` :111→:122, route `GET /v1/finance/product-imports/{id}` api.php:526) — thêm cờ `is_can_allocate` = `$this->canCreateTransferProductAllocation()` NGAY SAU `is_can_edit` (dòng 494).

**Interfaces:**
- Consumes: entity C1/C2. Bám khuôn `ProductTransferRequestService` (store/update trong `DB::transaction`) + `ProductTransferRequestController` (mỏng, uỷ thác) + route group `Routes/api.php:287` (khai route tĩnh TRƯỚC `/{id}`; action KHÔNG `checkPermission`).
- Produces: endpoint `GET /transfer-product-allocations/create-data?import_id=` (→ `getDataForTransferProductAllocation`, guard `canCreateTransferProductAllocation`), `POST /transfer-product-allocations` (store), `GET /transfer-product-allocations/{id}` (show, guard canView), `PUT /transfer-product-allocations/{id}` (update, guard canEdit), optionally `GET /transfer-product-allocations` (index theo `created_by`).

- [ ] **Step 1: FormRequest** — rule port ERP controller :83-98 (product_import_id exists; products[]; product_id/unit_id exists; requests[].employee_id/request_id exists; customers[].customer_id exists; allocate_qty numeric 0..999999999; expire_date date `after_or_equal:tomorrow`; detail_id exists; status in:1,3) + message tiếng Việt như ERP :100-110.

- [ ] **Step 2: Service `store($data)` / `update($id,$data)`** trong `DB::transaction` — port ERP controller :136-174 / :247-272:
  - store: tạo entity (`product_import_id`; `product_export_request_id` = `ProductImport::find(pid)->product_import_request` → `product_export_request_id`; `note`; `status`; `code=randomString(16)` rồi `generateCode()`); `validateDetails` (false → ném ValidationException/trả lỗi "Dữ liệu không hợp lệ"); `syncDetails`; nếu `status==1` → `approve()`.
  - guard `canCreateTransferProductAllocation` (store) / `canEdit` (update) — ném 403/validation nếu false.
- [ ] **Step 3: Controller** mỏng (index/show/store/update/createData), uỷ thác service; `show`/`createData` gọi entity getData/getDataForTransferProductAllocation; trả `ResponseTrait` chuẩn HRM.
- [ ] **Step 4: Routes** — group `['prefix'=>'transfer-product-allocations']`, KHÔNG `checkPermission`; khai `/create-data` TRƯỚC `/{id}`.
- [ ] **Step 5: cờ `is_can_allocate`** — mở `Modules/Finance/Transformers/ProductImportResource/ProductImportDetailResource.php`, thêm `'is_can_allocate' => $this->canCreateTransferProductAllocation(),` NGAY SAU `'is_can_edit'` (dòng 494). Đây là nơi FE nút "Phân bổ hàng" (C4) đọc qua `GET /v1/finance/product-imports/{id}`.
- [ ] **Step 6: `php -l` + chạy route list** `php artisan route:list --path=transfer-product-allocations`.
- [ ] **Step 7: Commit**
```bash
git add Modules/Finance/Services/TransferProductAllocationService.php Modules/Finance/Http/Controllers/V1/TransferProductAllocationController.php Modules/Finance/Http/Requests/TransferProductAllocation/ Modules/Finance/Routes/api.php Modules/Finance/Transformers/ProductImportResource/ProductImportDetailResource.php
git commit -m "feat(type7-ppbhdc): service + controller + routes + is_can_allocate (gate bang method, khong checkPermission)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task C4: FE — nút "Phân bổ hàng" + màn lập/sửa/chi tiết phân bổ

**Files (hrm-client):**
- Modify: trang **chi tiết Phiếu nhập hàng** type 7 (**xác minh path**: grep `pages/finance/` cho màn ProductImport/Phiếu nhập hàng — ví dụ `warehouse-imports/_id` hoặc `product-imports/_id`) — thêm nút "Phân bổ hàng" ở slot `#custom-actions` của `V2Footer`, `v-if="data.is_can_allocate"`.
- Create: màn lập/sửa phân bổ + chi tiết (theo `erp-to-hrm-screen` khuôn màn mẫu; dùng `V2BaseModal`/trang riêng — chọn theo khối lượng bảng phân bổ; bám `product-transfer-requests/_id/index.vue` cho nút + popup + `apiPostMethod`).

**Interfaces:**
- Consumes: endpoint C3. `GET create-data?import_id=` → dựng bảng SP × người YC × dòng customer (allocate_qty input + expire_date). Submit `POST` với `status` (1 duyệt / 3 lưu nháp). Chi tiết phiếu đã duyệt → hiển thị allocate_qty/prepick_qty; `canEdit` (nháp) → mở sửa.

- [ ] **Step 1: locate** trang chi tiết Phiếu nhập hàng + xác nhận component footer (`V2Footer` + `#custom-actions`) + cách gọi API (`this.$store.dispatch('apiPostMethod'/'apiGetMethod')`).
- [ ] **Step 2: nút "Phân bổ hàng"** — `V2BaseButton primary size="sm" v-if="data.is_can_allocate" @click="openAllocation"` → điều hướng/ mở màn lập (truyền `import_id`).
- [ ] **Step 3: màn lập/sửa** — form bảng phân bổ (nhãn "Người tạo/Ngày tạo"; số định dạng quốc tế; validate inline). Nút "Lưu" (status 3) + "Phân bổ" (status 1). Toast chuẩn QLDA.
- [ ] **Step 4: màn chi tiết** — hiển thị dòng phân bổ + trạng thái; nút Sửa khi `canEdit`.
- [ ] **Step 5: verify Playwright** — mở chi tiết PNK type 7 non-direct đã hoàn thành → bấm "Phân bổ hàng" → nhập → Phân bổ → kiểm PYCCH về "Đã phân bổ" (status 12) + cột "Được nhận" hiện. (Nếu môi trường dev thiếu data → ghi rõ, verify tối thiểu cú pháp/định tuyến.)
- [ ] **Step 6: Commit** (hrm-client, chỉ file của task; KHÔNG đụng `product-exports/create.vue`)
```bash
git add <cac-file-FE-cua-task>
git commit -m "feat(type7-ppbhdc): FE nut Phan bo hang tren chi tiet Phieu nhap hang + man lap/sua/chi tiet phan bo

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task C5: Feature test PPBHĐC

**Files:**
- Create: `hrm-api/Modules/Finance/Tests/Feature/Type7BranchTransferAllocationTest.php`

**Interfaces:** bám khuôn `Type7BranchTransferImportTest.php` (`use DatabaseTransactions;`, chọn product/unit thật, 2 employee khác company, `markTestSkipped` khi thiếu nền; gọi method qua `ReflectionMethod` nếu cần).

- [ ] **Step 1: 5 test (DatabaseTransactions)** phủ Review Focus:
  1. `test_approve_writes_allocated_qty_on_ptr_product_and_detail` — approve cộng đúng `allocate_qty` lên cả `ProductTransferRequestProduct.allocated_qty` và `...Detail.allocated_qty`.
  2. `test_approve_writes_prepick_at_destination_company` — prepick_details có dòng `company_id = product_import.company_id` (ĐÍCH), `employee_id = detail.employee_id`, `qty = allocate_qty × lot.unit_coefficient`; có prepick_logs.
  3. `test_approve_sets_all_ptr_of_pxk_to_12` — ≥2 PYCCH (1 không có dòng phân bổ) → tất cả `status==12`.
  4. `test_validate_details_rejects_under_and_over` — tổng allocate ≠ `min(group remain, lot.qty)` → `validateDetails` false (cả thiếu lẫn thừa).
  5. `test_can_create_guard` — `canCreateTransferProductAllocation` false khi: type≠7 / status≠hoàn thành / khác created_by / is_import_direct / đã có allocation.

- [ ] **Step 2: chạy** `vendor/bin/phpunit Modules/Finance/Tests/Feature/Type7BranchTransferAllocationTest.php` (KHÔNG dùng `artisan test --filter`).
- [ ] **Step 3: Commit**
```bash
git add Modules/Finance/Tests/Feature/Type7BranchTransferAllocationTest.php
git commit -m "test(type7-ppbhdc): allocated_qty + prepick dich + PYCCH 12 + validateDetails + canCreate guard

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Checkpoint — 2026-10-23 (Phase C khởi động)
Vừa hoàn thành: design `design-phaseC.md` (A/A/A) + plan Phase C (C1-C5) với code thật từ khảo sát ERP+HRM. Xác minh then chốt: `WarehouseImportLot` HRM map bảng ERP 1:1 (đã populate ở bước PNK) → lot lookup port thẳng; prepick ghi qua `PrepickStockService::addLot`; bảng allocation đã có sẵn (không migration).
Đang làm dở: chưa code — chờ chạy SDD C1→C5.
Bước tiếp theo: dispatch implementer C1 (SDD), task review mỗi task, final opus review. GIỮ LOCAL.
Blocked: không.

---

## GHI CHÚ PHẠM VI (ngoài Phase A — các phase sau, KHÔNG làm trong plan này)

- **Prepick phía xuất** (ERP :1396-1440 trừ prepick theo NGƯỜI YÊU CẦU chuyển hàng, bỏ lọc customer; :1257 xuất thẳng `employee_id` từ `product_transfer_requests[0]`): nằm ở luồng trừ tồn/giữ lúc lập–duyệt PXK, KHÔNG ở finalize → **cần spike riêng** luồng prepick-on-export của HRM trước khi code. Tách Phase A-prepick.
- Phase B (nhập đóng vòng type 7), C (PPBHĐC), D (DeliveryTrip + in %VAT + biên bản), E (FE rà) — xem design.md mục 6.

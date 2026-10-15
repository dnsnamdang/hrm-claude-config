# Popup chọn hàng hoá dùng chung — Implementation Plan (A7 Phase 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Một popup chọn hàng hoá (cây catalog kinh doanh bên trái + bộ lọc phân loại mới phía trên bảng) dùng chung ERP + HRM, đọc
1 bộ API của HRM.

**Architecture:** HRM MasterData có thêm `ProductPickerService` (lọc + phạm vi + chế độ dịch vụ theo máy), `SellableStockReader` (port
công thức "SL tồn có thể bán" của ERP) và `ProductPickerController` (`search` / `tree-counts` / `items`). HRM dùng component Vue
`V2ProductPickerModal`; ERP gọi cùng API qua route trung gian mang `jwt_token`, rồi thay ruột 2 partial chính.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), Laravel 6 + AngularJS 1.3 + Blade (ERP), MySQL `hrm_erp_giacty`.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-13-popup-chon-hang-hoa-dung-chung-design.md` · Mockup: `mockup-popup-tim-hang.html`.

## Cách chia plan

Spec có 5 bước trên 3 repo, mỗi bước hỏi "Làm" riêng. File này gồm **Phần A (bản đồ chung)** và **Phần B (task chi tiết bước 4.1 + 4.2)**.
Bước 4.3 / 4.4 / 4.5 phụ thuộc khuôn dữ liệu chốt ở 4.2, nên sẽ viết task chi tiết vào file này khi bắt đầu bước đó (Phần A đã chốt
phạm vi + giao diện để không lệch).

## Global Constraints

- Không merge vào `gop_db` (cả 3 repo). HRM: nhánh con `feat/cdhh-p4-popup-chon-hang` từ `feat/chuyen-doi-hang-hoa` (worktree
  `wt-chuyen-doi-hang-hoa`), xong merge `--no-ff` về nhánh chung. ERP: nhánh con từ `feat/2d1-erp-khong-loi` (worktree `wt-erp-2d1`).
- Mỗi bước 4.x chỉ bắt đầu sau khi user nói **"Làm"** cho bước đó (kèm phạm vi repo · nhánh · file · DB). Chạy migration vào DB nào cũng phải nêu.
- Không git stash; dừng tiến trình theo PID; không chạy cả bộ e2e trừ khi user yêu cầu (vẫn viết/cập nhật spec e2e).
- FE phải kiểm bằng Playwright MCP, đo số từ DOM, so với mockup.
- PHP: `/opt/homebrew/opt/php@7.4/bin/php`. Test hrm-api chạy trên MySQL `hrm_erp_giacty` trong `DatabaseTransactions`, chạy theo đường dẫn file
  (module test không nằm trong testsuite mặc định). Luôn `artisan config:clear` trước.
- Không truyền hàm built-in (`'intval'`, `'is_numeric'`) vào `Collection::map/filter` — dùng closure.
- Mọi chỗ đọc giá đi qua `ProductPriceReader` (không chạm bảng giá trực tiếp) để `PriceReaderWhitelistTest` xanh.
- Quyền: không bypass super admin; giá vốn = quyền `Xem giá vốn hàng hoá` (id 1092) đọc qua `isCurrentEmployeeHasPermission`.
- Văn bản UI tiếng Việt; số định dạng 1,234,567; tiêu đề cột 1 dòng.

## Review Focus

1. **Hàng không có `product_type_id` (100% hàng hiện tại)** — lọc "ẩn hàng làm dịch vụ" bằng `whereNotIn(product_type_id …)` sẽ loại sạch
   hàng NULL (SQL `NULL NOT IN` = NULL). Phải dùng `whereNotExists`. Test: hàng `product_type_id = NULL` vẫn ra (Task 4).
2. **Công ty chứng từ ≠ công ty đang làm việc** — người dùng làm ở cty A mở chứng từ của cty B mà họ cũng được làm: phải trả giá/tồn của B;
   công ty không thuộc danh sách được làm ⇒ 403, không âm thầm lùi về công ty hiện tại. Test (Task 6).
3. **Không có quyền giá vốn** — `columns[]=cost_price` vẫn phải ra `null`, kể cả khi FE gửi. Test (Task 6).
4. **Từ khoá có `đ` / gõ không dấu** — collation `utf8mb4_unicode_ci` coi `ầ = a` nhưng `đ ≠ d`. Gõ "dau nhot" phải ra "Dầu nhớt"; "đ" chưa
   khớp "d" thì ghi rõ giới hạn (không làm cột không dấu ở đợt này). Test khẳng định ca không dấu (Task 4).
5. **Hàng xếp ở nhiều Tiểu mục** — `search` phải trả 1 dòng/hàng (không nhân dòng do join `product_business_catalogs`); tổng "Tất cả" đếm
   hàng phân biệt. Test (Task 4, Task 7).

---

## Phần A — Bản đồ chung

### A1. Điều chỉnh so với spec sau khảo sát code (13/10)
| Spec | Thực tế | Plan làm |
|---|---|---|
| `GET/PUT product-picker/column-config` mới | HRM đã có bảng `user_column_settings` + `GET /human/column-customizations/detail?table=` / `POST /human/column-customizations` + mixin `columnCustomizationMixin` | **Dùng lại**, `screen_key = product_picker`. ERP gọi qua route trung gian. Không tạo endpoint mới. |
| `GET product-picker/options` mới | Đã có `products/form-options` (Loại SP kèm `path` Tính chất/Nhóm CN/Nhóm SP), `products/vehicle-options`, `products/catalog-options`, `products/option-search?type=product_models|order_codes`, `<slug>/getAll` | **Dùng lại**, không tạo endpoint mới. |
| Adapter ERP đổi khuôn hàng sang 2 định dạng dòng cũ | Hầu hết màn ERP chỉ đọc `product.id` rồi tự gọi `/admin/products/{id}/getData`; popup báo giá lấy danh sách id rồi `chooseProducts()` | Adapter ERP chủ yếu **trả id** cho hàm cũ (`addProduct({id})`, `chooseProducts` với mảng id). `items` chỉ HRM dùng. |
| "Hàng hoá làm dịch vụ" | Hôm nay là enum ERP `products.product_type = 'service_product'` (30 hàng) | Cờ mới trên Tính chất thay thế; quy đổi 30 hàng nằm trong việc quy đổi phân loại (chặn go-live). |
| Từ khoá không dấu | Không có cột/helper không dấu; collation `unicode_ci` đã bỏ dấu trừ `đ` | Dựa vào collation; `đ ≠ d` ghi là giới hạn (Review Focus 4). |

### A2. Bản đồ file
**hrm-api (`Modules/MasterData` = MD)**
| File | Việc |
|---|---|
| `MD/Database/Migrations/2026_10_13_000001_add_service_flags_to_product_natures_table.php` (mới) | 2 cột `is_service_product`, `is_service_quotation` |
| `MD/Entities/ProductClassification/ProductNature.php` | fillable + cast 2 cờ |
| `MD/Http/Requests/ProductClassification/ProductNatureRequest.php` | validate 2 cờ |
| `MD/Services/ProductClassification/ProductNatureService.php` | ghi + lịch sử 2 cờ |
| `MD/Transformers/ProductClassification/ProductNatureResource.php` | trả 2 cờ |
| `MD/Services/Product/SellableStockReader.php` (mới) | Tồn bán được theo công ty (port ERP `Product::stockCompanies`) |
| `MD/Services/Product/ProductPickerService.php` (mới) | Phạm vi + bộ lọc + chế độ máy; `query()`, `treeCounts()`, `rows()`, `items()` |
| `MD/Http/Requests/Product/ProductPickerRequest.php` (mới) | validate tham số + kiểm công ty được làm việc |
| `MD/Http/Controllers/V1/Product/ProductPickerController.php` (mới) | 3 endpoint |
| `MD/Routes/api.php` | 3 route `product-picker/*` trong nhóm `products` (trước `/{product}`) |
| `hrm-api/database/migrations/2026_10_13_000002_add_picker_indexes.php` (mới, chỉ nếu đo thấy cần) | index cho picker (gồm N84) |
| `MD/Tests/Feature/ProductNatureServiceFlagsTest.php`, `SellableStockReaderTest.php`, `ProductPickerSearchTest.php`, `ProductPickerTreeCountsTest.php`, `ProductPickerItemsTest.php` (mới) | test |

**hrm-client**
| File | Việc |
|---|---|
| `pages/master-data/product-natures/AddProductNatureModal.vue`, `index.vue` | 2 checkbox + 2 cột (4.1) |
| `components/product/picker/V2ProductPickerModal.vue` + con `PickerFilterBar.vue`, `PickerAdvancedFilters.vue`, `PickerResultTable.vue` (mới, 4.3) | popup |
| Thay popup ở: `QuotationProductSearchModal`, `BomBuilderAddProductModal`, `PriceAskingProductPickerModal`, `ProductItemPickerModal` (4.3) | |

**ERP (`wt-erp-2d1`)** (4.4–4.5)
| File | Việc |
|---|---|
| `app/Services/Hrm/HrmProductPickerProxy.php` (mới) | Guzzle gọi HRM với `Authorization: Bearer <jwt_token>` (khuôn `HrmApiService`) |
| `app/Http/Controllers/Hrm/ProductPickerProxyController.php` (mới) + route trong nhóm `admin` `['sso.check','userLogin']` (`routes/web.php:34-56`, không có `PreventDuplicateSubmission`) | `/admin/hrm/product-picker/{search,tree-counts,items}` + `/admin/hrm/column-customizations` |
| `resources/views/partials/modals/searchProduct.blade.php` + `js/searchProductJs.blade.php`; `searchProductQuotation.blade.php` + `js/searchProductQuotationJs.blade.php` | thay ruột, giữ hàm `searchProduct(options, disabled)` / `searchProduct(quotation, options)` và đường trả về |

### A3. Giao diện giữa các bước (chốt ở 4.2, 4.3/4.4 dùng)
`GET /api/v1/master-data/products/product-picker/search` — tham số:
```
company_id (bắt buộc) · price_type_id · keyword · page · per_page (≤100, mặc định 20)
business_scope_id | chapter_id | job_group_id | job_cluster_id | uncatalogued=1   (nhánh cây)
include_uncataloged=1 · in_stock=1 · exclude_ids[]
product_nature_id · product_function_group_id · product_family_id · product_type_id · product_characteristic_id
brand_ids[] · manufacture_ids[] · origin_ids[] · model_id · used_for_machine_id
vehicle_manufact_id · vehicle_brand_id · vehicle_model_id · vehicle_life_id
machine_id + include_service_shared=1                                              (chế độ báo giá DV)
columns[] ⊂ {manufacturer, origin, barcode, order_code, product_type_path, catalog_path, characteristic, negotiation_limit, note, cost_price}
```
Trả về (`apiGetList`-like): `{ data: Row[], meta: { current_page, per_page, total, last_page } }` với
```
Row = { id, code, name, avatar, model_name, brand_name, unit_name, product_type_name, price: float|null, sellable_qty: float,
        + các khoá trong columns[] (cost_price: float|null — null khi không có quyền) }
```
`GET .../product-picker/tree-counts` — cùng tham số trừ nhánh cây ⇒ `{ data: { clusters: {id: n}, groups: {id: n}, chapters: {id: n}, scopes: {id: n}, total: n, uncatalogued: n|null } }` — **đếm phân biệt từng cấp, FE dùng thẳng, KHÔNG cộng dồn** (sửa sau review 13/10).
`GET .../product-picker/items?company_id=&price_type_id=&ids[]=` ⇒ `{ data: Item[] }` với `Item = Row + { units: [{unit_id, unit_name, is_base: bool, unit_coefficient, price (+ cost_price khi có quyền)}], vat_percent, guarantee, guarantee_type, min_stock_qty }`. Quyền giá vốn xét theo **công ty chứng từ** (`company_id`), không theo công ty đang làm việc.

### A4. Phạm vi bước sau (task chi tiết viết khi tới lượt)
- **4.3 HRM FE:** `V2ProductPickerModal` theo mockup (props `companyId`, `priceTypeId`, `multiple`, `lockedFilters`, `existingIds`, `mode`,
  `machineId`; emit `select(items)` gọi `items` khi bấm Thêm); cây tái dùng `ProductCatalogTree` (truyền counts từ `tree-counts`);
  cấu hình cột qua `columnCustomizationMixin` (`columnScreenKey = 'product_picker'`); thay 4 popup cũ; spec e2e
  `e2e/tests/product-picker.spec.ts` (có/không quyền giá vốn).
- **4.4 ERP:** proxy + thay ruột 2 partial. **Rủi ro đã thấy:** các màn truyền ~20 tuỳ chọn riêng cho `searchProduct`
  (`firm_contract_id`, `buy_contract2_id`, `inland_buy_contract_id`, `service_contract_id`, `contract_id`, `request_type`, `warehouse_id`,
  `warehouses`, `is_self_inventory`, `is_liquidation_product`, `type=include_deleted|has_prepick|has_stock|position_transfers…`, `group_ids`,
  `recipe`, `promotion`, `supplier`…). Task đầu của 4.4 là **kiểm kê từng tuỳ chọn → quyết định port sang API HRM hay giữ popup cũ cho
  màn đó**, rồi hỏi user các tuỳ chọn thuộc nghiệp vụ trước khi code.
- **4.5 ERP:** 3 partial phụ + `searchProduct2`, gỡ partial/endpoint cũ khi hết chỗ dùng.

---

## Phần B — Task chi tiết

Chuẩn bị (1 lần, trước Task 1):
```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa
git status --short            # phải sạch
git checkout -b feat/cdhh-p4-popup-chon-hang feat/chuyen-doi-hang-hoa
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear
```

### Task 1 (4.1 BE): 2 cờ dịch vụ trên Tính chất hàng hoá

**Files:**
- Create: `hrm-api/Modules/MasterData/Database/Migrations/2026_10_13_000001_add_service_flags_to_product_natures_table.php`
- Modify: `MD/Entities/ProductClassification/ProductNature.php` (fillable ~L30, casts ~L40)
- Modify: `MD/Http/Requests/ProductClassification/ProductNatureRequest.php` (rules ~L32, attributes ~L48)
- Modify: `MD/Services/ProductClassification/ProductNatureService.php` (`fillableFrom`, `catalogColumns`, `catalogDisplay`)
- Modify: `MD/Transformers/ProductClassification/ProductNatureResource.php` (~L13)
- Test: `MD/Tests/Feature/ProductNatureServiceFlagsTest.php`

**Interfaces:**
- Produces: cột `product_natures.is_service_product` (1 = Hàng hoá làm dịch vụ — ẩn khỏi popup), `product_natures.is_service_quotation`
  (1 = Dùng cho báo giá dịch vụ); resource trả 2 khoá boolean cùng tên. Task 4 đọc 2 cột này.

- [ ] **Step 1: Viết test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

/** A7 Phase 4 — 2 cờ dịch vụ trên Tính chất hàng hoá (spec §4.3) */
class ProductNatureServiceFlagsTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private function create(array $flags): int
    {
        $code = 'TCHH.' . substr(uniqid(), -4);

        return $this->postJson('/api/v1/master-data/product-natures', [
            'code' => $code, 'name' => 'P4 test ' . $code, 'status' => 1, 'barcode_template_type' => 4,
        ] + $flags)->assertSuccessful()->json('data.id');
    }

    /** @test */
    public function luu_va_doc_lai_2_co_dich_vu()
    {
        $this->actAs(1, ['Quản lý danh mục tính chất hàng hóa', 'Xem danh mục tính chất hàng hóa']);
        $id = $this->create(['is_service_product' => 1, 'is_service_quotation' => 0]);

        $row = DB::table('product_natures')->where('id', $id)->first();
        $this->assertSame([1, 0], [(int) $row->is_service_product, (int) $row->is_service_quotation]);
        $this->getJson('/api/v1/master-data/product-natures/' . $id)->assertOk()
            ->assertJsonPath('data.is_service_product', true)
            ->assertJsonPath('data.is_service_quotation', false);
    }

    /** @test */
    public function bo_trong_thi_mac_dinh_0()
    {
        $this->actAs(1, ['Quản lý danh mục tính chất hàng hóa', 'Xem danh mục tính chất hàng hóa']);
        $id = $this->create([]);
        $row = DB::table('product_natures')->where('id', $id)->first();
        $this->assertSame([0, 0], [(int) $row->is_service_product, (int) $row->is_service_quotation]);
    }

    /** @test */
    public function sai_kieu_bao_loi_ca_2_o_cung_luc()
    {
        $this->actAs(1, ['Quản lý danh mục tính chất hàng hóa', 'Xem danh mục tính chất hàng hóa']);
        $this->postJson('/api/v1/master-data/product-natures', [
            'code' => 'TCHH.' . substr(uniqid(), -4), 'name' => 'x', 'status' => 1, 'barcode_template_type' => 4,
            'is_service_product' => 'abc', 'is_service_quotation' => 'xyz',
        ])->assertStatus(422)->assertJsonValidationErrors(['is_service_product', 'is_service_quotation']);
    }
}
```

- [ ] **Step 2: Chạy, xác nhận fail**

Run: `cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductNatureServiceFlagsTest.php`
Expected: FAIL — `Unknown column 'is_service_product'` (chưa migrate).

- [ ] **Step 3: Migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * A7 Phase 4 (chốt 13/10/2026): 2 cờ dịch vụ đặt ở Tính chất hàng hoá — popup chọn hàng dùng chung đọc:
 * - is_service_product: "Hàng hoá làm dịch vụ" ⇒ ẩn khỏi popup (thay enum ERP product_type = service_product);
 * - is_service_quotation: "Dùng cho báo giá dịch vụ" ⇒ công tắc "Gồm cả hàng dùng chung cho dịch vụ" (thay accessories/lubricant).
 */
class AddServiceFlagsToProductNaturesTable extends Migration
{
    public function up()
    {
        Schema::table('product_natures', function (Blueprint $table) {
            if (!Schema::hasColumn('product_natures', 'is_service_product')) {
                $table->unsignedTinyInteger('is_service_product')->default(0)->after('is_auto_parts')
                    ->comment('1 = Hàng hoá làm dịch vụ: ẩn khỏi popup chọn hàng (A7 P4)');
            }
            if (!Schema::hasColumn('product_natures', 'is_service_quotation')) {
                $table->unsignedTinyInteger('is_service_quotation')->default(0)->after('is_service_product')
                    ->comment('1 = Dùng cho báo giá dịch vụ: hàng dùng chung khi báo giá sửa máy (A7 P4)');
            }
        });
    }

    public function down()
    {
        Schema::table('product_natures', function (Blueprint $table) {
            foreach (['is_service_quotation', 'is_service_product'] as $column) {
                if (Schema::hasColumn('product_natures', $column)) {
                    $table->dropColumn($column);
                }
            }
        });
    }
}
```

**Hỏi user trước khi chạy** (phạm vi "Làm" 4.1 phải nêu DB): `php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_10_13_000001_add_service_flags_to_product_natures_table.php`
vào `hrm_erp_giacty`.

- [ ] **Step 4: Model + Request + Service + Resource**

`ProductNature.php` — thêm vào `$fillable` sau `'is_auto_parts',`:
```php
        'is_service_product',
        'is_service_quotation',
```
và `$casts`:
```php
    protected $casts = [
        'is_auto_parts' => 'boolean',
        'is_service_product' => 'boolean',
        'is_service_quotation' => 'boolean',
    ];
```
`ProductNatureRequest.php` — rules thêm cạnh `is_auto_parts`:
```php
            'is_service_product' => 'nullable|boolean',
            'is_service_quotation' => 'nullable|boolean',
```
attributes:
```php
            'is_service_product' => 'Hàng hoá làm dịch vụ',
            'is_service_quotation' => 'Dùng cho báo giá dịch vụ',
```
`ProductNatureService.php`:
```php
    protected function fillableFrom(Request $request): array
    {
        return parent::fillableFrom($request) + [
            'barcode_template_type' => (int) $request->barcode_template_type,
            'is_auto_parts' => $request->boolean('is_auto_parts') ? 1 : 0,
            'is_service_product' => $request->boolean('is_service_product') ? 1 : 0,
            'is_service_quotation' => $request->boolean('is_service_quotation') ? 1 : 0,
        ];
    }

    protected function catalogColumns(): array
    {
        return array_merge(parent::catalogColumns(), [
            'barcode_template_type', 'is_auto_parts', 'is_service_product', 'is_service_quotation',
        ]);
    }
```
trong `catalogDisplay` đổi nhánh cờ thành:
```php
        if (in_array($column, ['is_auto_parts', 'is_service_product', 'is_service_quotation'], true)) {
            return (int) $value === 1 ? 'Có' : 'Không';
        }
```
`ProductNatureResource.php` cạnh `is_auto_parts`:
```php
            'is_service_product' => (bool) $this->is_service_product,
            'is_service_quotation' => (bool) $this->is_service_quotation,
```

- [ ] **Step 5: Chạy test xanh + test cũ cùng màn**

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductNatureServiceFlagsTest.php && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductNatureAutoPartsTest.php`
Expected: OK (3 tests) và OK (2 tests).

- [ ] **Step 6: Commit**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api
git add Modules/MasterData/Database/Migrations/2026_10_13_000001_add_service_flags_to_product_natures_table.php \
  Modules/MasterData/Entities/ProductClassification/ProductNature.php \
  Modules/MasterData/Http/Requests/ProductClassification/ProductNatureRequest.php \
  Modules/MasterData/Services/ProductClassification/ProductNatureService.php \
  Modules/MasterData/Transformers/ProductClassification/ProductNatureResource.php \
  Modules/MasterData/Tests/Feature/ProductNatureServiceFlagsTest.php
git commit -m "feat(master-data): 2 cờ dịch vụ trên Tính chất hàng hoá cho popup chọn hàng (A7 P4-4.1)"
```

### Task 2 (4.1 FE): tick 2 cờ trên màn Tính chất

**Files:**
- Modify: `hrm-client/pages/master-data/product-natures/AddProductNatureModal.vue` (template ~L65-72, data ~L147, map ~L208, payload ~L268)
- Modify: `hrm-client/pages/master-data/product-natures/index.vue` (slot ~L104, fields ~L385)

**Interfaces:** Consumes Task 1 (khoá `is_service_product`, `is_service_quotation`).

- [ ] **Step 1: Thêm hàng checkbox mới ngay dưới hàng "Mẫu in barcode / Phụ tùng ô tô"** (2 ô col-md-6 — đủ 12 cột, không để ô lẻ)

```vue
        <div class="form-row">
            <div class="col-md-6 mb-2">
                <V2BaseLabel hint="Tick: hàng thuộc tính chất này là hàng làm dịch vụ, không hiện trong popup chọn hàng.">
                    Hàng hoá làm dịch vụ
                </V2BaseLabel>
                <V2BaseCheckbox v-model="data.is_service_product" label="Là hàng hoá làm dịch vụ" :disabled="isShow" />
            </div>
            <div class="col-md-6 mb-2">
                <V2BaseLabel hint="Tick: khi báo giá dịch vụ sửa máy, bật &quot;Gồm cả hàng dùng chung cho dịch vụ&quot; sẽ hiện hàng thuộc tính chất này.">
                    Dùng cho báo giá dịch vụ
                </V2BaseLabel>
                <V2BaseCheckbox v-model="data.is_service_quotation" label="Dùng chung cho báo giá dịch vụ" :disabled="isShow" />
            </div>
        </div>
```
data mặc định (cạnh `is_auto_parts: false,`): `is_service_product: false, is_service_quotation: false,`
map khi mở sửa/xem (cạnh `is_auto_parts: !!data.is_auto_parts,`): `is_service_product: !!data.is_service_product, is_service_quotation: !!data.is_service_quotation,`
payload (cạnh `is_auto_parts: this.data.is_auto_parts ? 1 : 0,`): `is_service_product: this.data.is_service_product ? 1 : 0, is_service_quotation: this.data.is_service_quotation ? 1 : 0,`

- [ ] **Step 2: 2 cột ở danh sách** — `index.vue`, chép khuôn cột `is_auto_parts` (slot `#cell-is_auto_parts` + field):

```vue
                <template #cell-is_service_product="{ item }">
                    <div class="field-line text-dark font-weight-normal">{{ item.is_service_product ? 'Có' : '' }}</div>
                </template>
                <template #cell-is_service_quotation="{ item }">
                    <div class="field-line text-dark font-weight-normal">{{ item.is_service_quotation ? 'Có' : '' }}</div>
                </template>
```
fields (sau field `is_auto_parts`, cùng thuộc tính width/minWidth với nó):
```js
                { key: 'is_service_product', label: 'Làm dịch vụ', sortable: false, width: 110, minWidth: 110 },
                { key: 'is_service_quotation', label: 'Báo giá DV', sortable: false, width: 110, minWidth: 110 },
```
(nếu field `is_auto_parts` khai thêm khoá khác — vd `class`, `thClass` — chép đủ y hệt.)

- [ ] **Step 3: Kiểm bằng Playwright MCP** (Nuxt 3031, API 8031)
  - Mở `/master-data/product-natures`, đo: tiêu đề 2 cột mới 1 dòng (`th.getBoundingClientRect().height` ≤ hàng tiêu đề cũ).
  - Thêm mới → tick 2 ô → Lưu → mở lại xem: 2 ô còn tick (đọc `input.checked`), danh sách hiện "Có".
  - Đo 2 checkbox mới cùng `top` với nhau và lệch ≤ 1px so với khuôn checkbox "Phụ tùng ô tô" (`getBoundingClientRect().left`).
  - Tài khoản không có quyền Quản lý: nút Lưu không hiện / modal xem chỉ đọc (2 ô `disabled`).

- [ ] **Step 4: Commit**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-client
git add pages/master-data/product-natures/AddProductNatureModal.vue pages/master-data/product-natures/index.vue
git commit -m "feat(master-data): tick Hàng làm dịch vụ / Dùng cho báo giá DV trên màn Tính chất (A7 P4-4.1)"
```

### Task 3 (4.2): `SellableStockReader` — Tồn bán được theo công ty

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/SellableStockReader.php`
- Test: `MD/Tests/Feature/SellableStockReaderTest.php`

**Interfaces:**
- Produces:
  - `SellableStockReader::subquery(int $companyId): \Illuminate\Database\Query\Builder` — cột `product_id`, `sellable_qty` (1 dòng/hàng có tồn kế toán ở công ty).
  - `SellableStockReader::forProducts(array $productIds, int $companyId): array` — `[product_id => float]`, hàng không có dòng = 0.
- Công thức (port nguyên `App\Product::stockCompanies()` của ERP `app/Product.php:5998-6079`, cắt 1 công ty):
  `sellable = Σ accounting_stocks.qty (kho không thuộc promo_warehouse_ids của mọi công ty; stock_id NOT NULL; aw.company_id = C)
   − Σ prepick_details.qty (company C) − Σ hold_details.qty (company C)
   − Σ (werd.export_total_qty − export_prepick_qty − export_hold_qty) của phiếu YC xuất (company C, is_complete = 0, status ∉ {3,5}, need_export = 1, type ≠ 15)`.

- [ ] **Step 1: Viết test fail** (dữ liệu giả trong transaction; dùng 1 hàng có sẵn và 2 kho mới của công ty test)

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Services\Product\SellableStockReader;
use Tests\TestCase;

/** A7 P4 — Tồn bán được = công thức ERP Product::stockCompanies() cắt theo 1 công ty */
class SellableStockReaderTest extends TestCase
{
    use DatabaseTransactions;

    private $productId;
    private $company = 6; // UPSERVICE — công ty sạch (không có hàng) như ProductReadApiTest

    protected function setUp(): void
    {
        parent::setUp();
        $this->productId = (int) DB::table('products')->value('id');
        foreach (['accounting_stocks', 'prepick_details', 'hold_details', 'warehouse_export_request_details'] as $t) {
            DB::table($t)->where('product_id', $this->productId)->delete(); // trong transaction, rollback cuối ca
        }
    }

    private function warehouse(bool $promo = false): int
    {
        $id = DB::table('accounting_warehouses')->insertGetId(['name' => 'P4 kho ' . uniqid(), 'company_id' => $this->company]);
        if ($promo) {
            $ids = json_decode((string) DB::table('companies')->where('id', $this->company)->value('promo_warehouse_ids'), true) ?: [];
            $ids[] = $id;
            DB::table('companies')->where('id', $this->company)->update(['promo_warehouse_ids' => json_encode($ids)]);
        }

        return $id;
    }

    private function stock(int $warehouseId, float $qty): void
    {
        DB::table('accounting_stocks')->insert([
            'product_id' => $this->productId, 'accounting_warehouse_id' => $warehouseId, 'qty' => $qty, 'stock_id' => 1,
        ]);
    }

    /** @test */
    public function tru_giu_hang_tam_giu_va_yeu_cau_xuat_chua_xong_bo_kho_khuyen_mai()
    {
        $this->stock($this->warehouse(), 100);
        $this->stock($this->warehouse(true), 40);            // kho khuyến mãi — không tính
        DB::table('prepick_details')->insert(['product_id' => $this->productId, 'company_id' => $this->company, 'qty' => 10]);
        DB::table('hold_details')->insert(['product_id' => $this->productId, 'company_id' => $this->company, 'qty' => 5]);
        $open = DB::table('warehouse_export_requests')->insertGetId(['company_id' => $this->company, 'is_complete' => 0, 'status' => 1, 'type' => 1]);
        $done = DB::table('warehouse_export_requests')->insertGetId(['company_id' => $this->company, 'is_complete' => 1, 'status' => 1, 'type' => 1]);
        $promo = DB::table('warehouse_export_requests')->insertGetId(['company_id' => $this->company, 'is_complete' => 0, 'status' => 1, 'type' => 15]);
        foreach ([$open, $done, $promo] as $parent) {
            DB::table('warehouse_export_request_details')->insert([
                'parent_id' => $parent, 'product_id' => $this->productId, 'need_export' => 1,
                'export_total_qty' => 8, 'export_prepick_qty' => 2, 'export_hold_qty' => 1,
            ]);
        }

        // 100 − 10 − 5 − (8−2−1) = 80 ; phiếu đã xong + phiếu KM (type 15) không trừ
        $this->assertSame([$this->productId => 80.0], (new SellableStockReader())->forProducts([$this->productId], $this->company));
    }

    /** @test */
    public function cong_ty_khac_khong_lan_vao_va_hang_khong_ton_ra_0()
    {
        $other = (int) DB::table('companies')->where('id', '<>', $this->company)->value('id');
        $wh = DB::table('accounting_warehouses')->insertGetId(['name' => 'P4 kho khác ' . uniqid(), 'company_id' => $other]);
        $this->stock($wh, 50);
        $this->assertSame([$this->productId => 0.0], (new SellableStockReader())->forProducts([$this->productId], $this->company));
    }
}
```

> Nếu insert báo thiếu cột NOT NULL không có default (đo bằng `SHOW CREATE TABLE`), bổ sung giá trị tối thiểu vào mảng insert của
> test — không đổi công thức.

- [ ] **Step 2: Chạy, xác nhận fail** — Run: `vendor/bin/phpunit Modules/MasterData/Tests/Feature/SellableStockReaderTest.php` · Expected: FAIL `Class ... SellableStockReader not found`.

- [ ] **Step 3: Cài đặt**

```php
<?php

namespace Modules\MasterData\Services\Product;

use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

/**
 * "Tồn bán được" của 1 công ty — port NGUYÊN công thức ERP `App\Product::stockCompanies()` (app/Product.php:5998-6079),
 * cắt theo công ty: tồn kế toán (bỏ kho khuyến mãi của MỌI công ty) − giữ hàng (prepick) − tạm giữ (hold) − YC xuất chưa xong
 * (trừ phiếu khuyến mãi type 15). Đổi công thức ở ERP thì phải đổi cả ở đây (test đối chiếu Task 8).
 */
class SellableStockReader
{
    public function subquery(int $companyId): Builder
    {
        $promo = $this->promoWarehouseIds();

        $stock = DB::table('accounting_stocks as ast')
            ->join('product_units as pu', function ($j) {
                $j->on('pu.product_id', '=', 'ast.product_id')->where('pu.is_base', 1);
            })
            ->join('accounting_warehouses as aw', 'aw.id', '=', 'ast.accounting_warehouse_id')
            ->whereNotNull('ast.stock_id')
            ->where('aw.company_id', $companyId)
            ->when($promo, function ($q) use ($promo) {
                $q->whereNotIn('ast.accounting_warehouse_id', $promo);
            })
            ->groupBy('ast.product_id')
            ->select('ast.product_id', DB::raw('SUM(ast.qty) as qty'));

        $prepick = DB::table('prepick_details')->where('company_id', $companyId)
            ->groupBy('product_id')->select('product_id', DB::raw('SUM(qty) as qty'));
        $hold = DB::table('hold_details')->where('company_id', $companyId)
            ->groupBy('product_id')->select('product_id', DB::raw('SUM(qty) as qty'));
        $export = DB::table('warehouse_export_request_details as werd')
            ->join('warehouse_export_requests as wer', 'wer.id', '=', 'werd.parent_id')
            ->where('wer.company_id', $companyId)
            ->where('wer.is_complete', 0)
            ->whereNotIn('wer.status', [3, 5])
            ->where('wer.type', '<>', 15)
            ->where('werd.need_export', 1)
            ->groupBy('werd.product_id')
            ->select('werd.product_id', DB::raw(
                'SUM(werd.export_total_qty - werd.export_prepick_qty - werd.export_hold_qty) as qty'
            ));

        return DB::query()->fromSub($stock, 's')
            ->leftJoinSub($prepick, 'pre', 'pre.product_id', '=', 's.product_id')
            ->leftJoinSub($hold, 'hld', 'hld.product_id', '=', 's.product_id')
            ->leftJoinSub($export, 'ex', 'ex.product_id', '=', 's.product_id')
            ->select('s.product_id', DB::raw(
                'COALESCE(s.qty,0) - COALESCE(pre.qty,0) - COALESCE(hld.qty,0) - COALESCE(ex.qty,0) as sellable_qty'
            ));
    }

    /** @return array<int,float> [product_id => tồn bán được]; hàng không có tồn = 0 */
    public function forProducts(array $productIds, int $companyId): array
    {
        $ids = array_values(array_unique(array_map(function ($id) {
            return (int) $id;
        }, $productIds)));
        if (!$ids) {
            return [];
        }

        $rows = DB::query()->fromSub($this->subquery($companyId), 'st')
            ->whereIn('st.product_id', $ids)
            ->pluck('st.sellable_qty', 'st.product_id');

        $result = [];
        foreach ($ids as $id) {
            $result[$id] = (float) ($rows[$id] ?? 0);
        }

        return $result;
    }

    /** Kho khuyến mãi của MỌI công ty (ERP gộp hết) — `companies.promo_warehouse_ids` là mảng JSON */
    private function promoWarehouseIds(): array
    {
        $ids = [];
        foreach (DB::table('companies')->whereNotNull('promo_warehouse_ids')->pluck('promo_warehouse_ids') as $json) {
            foreach ((array) json_decode((string) $json, true) as $id) {
                $ids[] = (int) $id;
            }
        }

        return array_values(array_unique($ids));
    }
}
```

> Lưu ý khác ERP có chủ đích: ERP `leftJoin product_units … where pu.is_base` (thực chất là inner) và join prepick/hold/werd theo cặp
> (hàng, công ty) rồi mới cộng các công ty — cắt 1 công ty thì 2 cách cho cùng số. Test Task 8 đối chiếu trực tiếp trên dữ liệu thật.

- [ ] **Step 4: Chạy xanh** — Expected: OK (2 tests).
- [ ] **Step 5: Commit** — `git add Modules/MasterData/Services/Product/SellableStockReader.php Modules/MasterData/Tests/Feature/SellableStockReaderTest.php && git commit -m "feat(master-data): SellableStockReader — tồn bán được theo công ty, port công thức ERP (A7 P4-4.2)"`

### Task 4 (4.2): `ProductPickerService::query()` — phạm vi + bộ lọc + chế độ máy

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductPickerService.php`
- Test: `MD/Tests/Feature/ProductPickerSearchTest.php` (phần lọc — gọi service trực tiếp; phần HTTP thêm ở Task 6)

**Interfaces:**
- Consumes: `SellableStockReader::subquery(int)` (Task 3); cột cờ Task 1; `ProductCompany::STATUS_TRADING`; `Productable::TYPE_*`.
- Produces: `ProductPickerService::query(array $params, int $companyId, bool $withNode = true): \Illuminate\Database\Query\Builder` —
  trả builder `DB::table('products')` đã áp mọi điều kiện, **chưa select cột** (Task 5/7 tự select). `$params` = mảng tham số A3.

- [ ] **Step 1: Viết test fail** — dựng fixture trong transaction, mỗi ca 1 hàng dương + 1 hàng âm.

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\Productable;
use Modules\MasterData\Services\Product\ProductPickerService;
use Tests\TestCase;

/** A7 P4 — phạm vi + bộ lọc popup chọn hàng (spec §4) */
class ProductPickerSearchTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    const C = 6; // công ty sạch

    private function product(string $name, int $status = 3, array $extra = []): int
    {
        $id = DB::table('products')->insertGetId($extra + [
            'code' => 'P4' . strtoupper(substr(uniqid(), -8)), 'name' => $name, 'status' => 1, 'company_id' => self::C,
            'created_at' => now(), 'updated_at' => now(),
        ]);
        DB::table('product_company_coefficients')->insert([
            'product_id' => $id, 'company_id' => self::C, 'coefficient' => 1, 'status' => $status,
        ]);

        return $id;
    }

    private function catalog(int $productId, int $clusterId): void
    {
        DB::table('product_business_catalogs')->insert([
            'product_id' => $productId, 'company_id' => self::C, 'job_cluster_id' => $clusterId, 'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function ids(array $params, bool $withNode = true): array
    {
        return (new ProductPickerService())->query($params, self::C, $withNode)->orderBy('products.id')->pluck('products.id')
            ->map(function ($id) {
                return (int) $id;
            })->all();
    }

    /** @test */
    public function mac_dinh_chi_hang_dang_kinh_doanh_da_xep_catalog_bat_cong_tac_thi_them_hang_ngoai_catalog()
    {
        $branch = $this->catalogBranch();
        $in = $this->product('P4 trong catalog');
        $this->catalog($in, $branch['cluster']);
        $out = $this->product('P4 ngoài catalog');
        $stopped = $this->product('P4 ngừng KD', 4);
        $this->catalog($stopped, $branch['cluster']);
        $temp = $this->product('P4 hàng tạm', 6);
        $this->catalog($temp, $branch['cluster']);

        $this->assertSame([$in], array_values(array_intersect($this->ids([]), [$in, $out, $stopped, $temp])));
        $this->assertSame([$in, $out], array_values(array_intersect($this->ids(['include_uncataloged' => 1]), [$in, $out, $stopped, $temp])));
        $this->assertSame([$out], array_values(array_intersect($this->ids(['include_uncataloged' => 1, 'uncatalogued' => 1]), [$in, $out])));
    }

    /** @test */
    public function loc_theo_nhanh_cay_va_khong_nhan_dong_khi_hang_o_2_tieu_muc()
    {
        $a = $this->catalogBranch();
        $b = $this->catalogBranch();
        $p = $this->product('P4 hai tiểu mục');
        $this->catalog($p, $a['cluster']);
        $this->catalog($p, $b['cluster']);
        $other = $this->product('P4 chỉ nhánh B');
        $this->catalog($other, $b['cluster']);

        $this->assertSame([$p], array_values(array_intersect($this->ids(['job_cluster_id' => $a['cluster']]), [$p, $other])));
        $this->assertSame([$p], array_values(array_intersect($this->ids(['chapter_id' => $a['chapter']]), [$p, $other])));
        $this->assertSame(1, count(array_keys($this->ids([]), $p)), 'không nhân dòng');
        $this->assertContains($other, $this->ids(['job_cluster_id' => $a['cluster']], false), 'withNode=false bỏ lọc nhánh');
    }

    /** @test */
    public function an_hang_thuoc_tinh_chat_lam_dich_vu_nhung_giu_hang_chua_co_loai_sp()
    {
        $branch = $this->catalogBranch();
        $service = $this->productTypeFixture();
        DB::table('product_natures')->where('id', $service['nature'])->update(['is_service_product' => 1]);
        $hidden = $this->product('P4 làm dịch vụ', 3, ['product_type_id' => $service['type']]);
        $noType = $this->product('P4 chưa có loại SP');
        foreach ([$hidden, $noType] as $id) {
            $this->catalog($id, $branch['cluster']);
        }

        $this->assertSame([$noType], array_values(array_intersect($this->ids([]), [$hidden, $noType])));
    }

    /** @test */
    public function loc_phan_loai_4_cap_va_danh_muc_lien_quan()
    {
        $branch = $this->catalogBranch();
        $t = $this->productTypeFixture();
        $brand = (int) DB::table('brands')->value('id');
        $match = $this->product('P4 khớp', 3, ['product_type_id' => $t['type'], 'brand_id' => $brand]);
        $miss = $this->product('P4 lệch');
        foreach ([$match, $miss] as $id) {
            $this->catalog($id, $branch['cluster']);
        }

        foreach (['product_nature_id' => $t['nature'], 'product_function_group_id' => $t['group'], 'product_family_id' => $t['family'], 'product_type_id' => $t['type']] as $key => $value) {
            $this->assertSame([$match], array_values(array_intersect($this->ids([$key => $value]), [$match, $miss])), $key);
        }
        $this->assertSame([$match], array_values(array_intersect($this->ids(['brand_ids' => [$brand]]), [$match, $miss])));
    }

    /** @test */
    public function tu_khoa_khong_dau_khop_ten_co_dau_va_ma_dat_hang()
    {
        $branch = $this->catalogBranch();
        $p = $this->product('P4 Dầu nhớt động cơ');
        $this->catalog($p, $branch['cluster']);

        $this->assertContains($p, $this->ids(['keyword' => 'dau nhot']));
        $this->assertNotContains($p, $this->ids(['keyword' => 'nhot xyz']));
    }

    /** @test */
    public function che_do_bao_gia_dich_vu_phu_tung_cua_may_va_nhom_may_cong_tac_them_hang_dung_chung()
    {
        $machineGroup = (int) DB::table('groups')->value('id');
        $machine = $this->product('P4 Máy nén', 3, ['group_id' => $machineGroup]);
        $forMachine = $this->product('P4 lọc gió của máy');
        $forGroup = $this->product('P4 lọc dầu của nhóm máy');
        $sharedType = $this->productTypeFixture();
        DB::table('product_natures')->where('id', $sharedType['nature'])->update(['is_service_quotation' => 1]);
        $shared = $this->product('P4 dầu nhớt dùng chung', 3, ['product_type_id' => $sharedType['type']]);
        $unrelated = $this->product('P4 không liên quan');
        DB::table('productables')->insert([
            ['product_id' => $forMachine, 'productable_id' => $machine, 'productable_type' => Productable::TYPE_PRODUCT],
            ['product_id' => $forGroup, 'productable_id' => $machineGroup, 'productable_type' => Productable::TYPE_GROUP],
        ]);
        $all = [$forMachine, $forGroup, $shared, $unrelated];

        // chế độ máy bỏ qua catalog (cây mờ) — không xếp catalog vẫn ra
        $this->assertSame([$forMachine, $forGroup], array_values(array_intersect($this->ids(['machine_id' => $machine]), $all)));
        $this->assertSame([$forMachine, $forGroup, $shared], array_values(array_intersect(
            $this->ids(['machine_id' => $machine, 'include_service_shared' => 1]), $all
        )));
    }

    /** @test */
    public function con_ton_va_loai_tru_id()
    {
        $branch = $this->catalogBranch();
        $a = $this->product('P4 có tồn');
        $b = $this->product('P4 không tồn');
        foreach ([$a, $b] as $id) {
            $this->catalog($id, $branch['cluster']);
        }
        $wh = DB::table('accounting_warehouses')->insertGetId(['name' => 'P4 kho ' . uniqid(), 'company_id' => self::C]);
        DB::table('product_units')->insert([
            ['product_id' => $a, 'unit_id' => (int) DB::table('units')->value('id'), 'is_base' => 1],
        ]);
        DB::table('accounting_stocks')->insert(['product_id' => $a, 'accounting_warehouse_id' => $wh, 'qty' => 3, 'stock_id' => 1]);

        $this->assertSame([$a], array_values(array_intersect($this->ids(['in_stock' => 1]), [$a, $b])));
        $this->assertSame([$b], array_values(array_intersect($this->ids(['exclude_ids' => [$a]]), [$a, $b])));
    }
}
```

> Trước khi chạy Step 1: xác nhận hướng `productables` bằng SQL đọc (không ghi):
> `SELECT p.name, m.name FROM productables x JOIN products p ON p.id=x.product_id JOIN products m ON m.id=x.productable_id WHERE x.productable_type='App\\\\Product' LIMIT 5;`
> — `product_id` phải là phụ tùng, `productable_id` là máy (khớp ERP `SearchController:944-958`). Ngược thì đổi chiều trong test + code.

- [ ] **Step 2: Chạy, xác nhận fail** — Expected: FAIL `Class ... ProductPickerService not found`.

- [ ] **Step 3: Cài đặt**

```php
<?php

namespace Modules\MasterData\Services\Product;

use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\ProductCompany;
use Modules\MasterData\Entities\Product\Productable;

/**
 * Popup chọn hàng hoá dùng chung ERP + HRM (A7 Phase 4, spec 2026-10-13 §4).
 * Phạm vi: hàng Đang kinh doanh tại công ty chứng từ (pcc.status = 3 ⇒ tự loại hàng tạm), bỏ hàng thuộc Tính chất "Hàng hoá làm dịch vụ".
 * Mặc định chỉ hàng ĐÃ XẾP CATALOG của công ty; `include_uncataloged` mở rộng. Chế độ máy (`machine_id`) bỏ qua catalog.
 */
class ProductPickerService
{
    const CATALOG_LEVELS = [
        'job_cluster_id' => 'pbc.job_cluster_id',
        'job_group_id' => 'jc.group_id',
        'chapter_id' => 'jg.chapter_id',
        'business_scope_id' => 'ch.internal_business_scope_id',
    ];

    /** @var SellableStockReader */
    private $stock;

    public function __construct(SellableStockReader $stock = null)
    {
        $this->stock = $stock ?: new SellableStockReader();
    }

    public function query(array $p, int $companyId, bool $withNode = true): Builder
    {
        $q = DB::table('products')
            ->join('product_company_coefficients as pcs', function ($j) use ($companyId) {
                $j->on('pcs.product_id', '=', 'products.id')->where('pcs.company_id', '=', $companyId);
            })
            ->where('pcs.status', ProductCompany::STATUS_TRADING)
            ->where('products.status', '<>', 0)
            ->whereNotExists($this->natureFlag('is_service_product'));

        if (!empty($p['machine_id'])) {
            $this->applyMachine($q, (int) $p['machine_id'], !empty($p['include_service_shared']));
        } else {
            $this->applyCatalog($q, $p, $companyId, $withNode);
        }

        $this->applyClassification($q, $p);
        $this->applyRelated($q, $p);
        $this->applyKeyword($q, $p['keyword'] ?? null);

        if (!empty($p['exclude_ids'])) {
            $q->whereNotIn('products.id', $this->intList($p['exclude_ids']));
        }
        if (!empty($p['in_stock'])) {
            $q->whereExists(function ($sub) use ($companyId) {
                $sub->select(DB::raw(1))->fromSub($this->stock->subquery($companyId), 'st')
                    ->whereColumn('st.product_id', 'products.id')->where('st.sellable_qty', '>', 0);
            });
        }

        return $q;
    }

    /** Hàng có Loại SP thuộc Tính chất bật `$flag` — dùng whereNotExists/whereExists (product_type_id NULL không bị loại nhầm) */
    private function natureFlag(string $flag): \Closure
    {
        return function ($sub) use ($flag) {
            $sub->select(DB::raw(1))->from('product_types as nt')
                ->join('product_families as nf', 'nf.id', '=', 'nt.product_family_id')
                ->join('product_function_groups as ng', 'ng.id', '=', 'nf.product_function_group_id')
                ->join('product_natures as nn', 'nn.id', '=', 'ng.product_nature_id')
                ->whereColumn('nt.id', 'products.product_type_id')
                ->where('nn.' . $flag, 1);
        };
    }

    private function applyCatalog(Builder $q, array $p, int $companyId, bool $withNode): void
    {
        $inCatalog = function ($sub) use ($companyId) {
            $sub->select(DB::raw(1))->from('product_business_catalogs as pbc0')
                ->whereColumn('pbc0.product_id', 'products.id')->where('pbc0.company_id', $companyId);
        };

        if ($withNode && !empty($p['uncatalogued'])) {
            $q->whereNotExists($inCatalog);
            return;
        }
        if (empty($p['include_uncataloged'])) {
            $q->whereExists($inCatalog);
        }
        if (!$withNode) {
            return;
        }

        $chosen = array_filter(self::CATALOG_LEVELS, function ($key) use ($p) {
            return !empty($p[$key]);
        }, ARRAY_FILTER_USE_KEY);
        if (!$chosen) {
            return;
        }

        $q->whereExists(function ($sub) use ($companyId, $chosen, $p) {
            $sub->select(DB::raw(1))->from('product_business_catalogs as pbc')
                ->join('job_clusters as jc', 'jc.id', '=', 'pbc.job_cluster_id')
                ->join('job_groups as jg', 'jg.id', '=', 'jc.group_id')
                ->join('chapters as ch', 'ch.id', '=', 'jg.chapter_id')
                ->whereColumn('pbc.product_id', 'products.id')
                ->where('pbc.company_id', $companyId);
            foreach ($chosen as $key => $column) {
                $sub->where($column, (int) $p[$key]);
            }
        });
    }

    /** Báo giá DV đã chọn máy: phụ tùng khai "Dùng cho" máy / nhóm máy; công tắc thêm hàng thuộc Tính chất "Dùng cho báo giá DV" */
    private function applyMachine(Builder $q, int $machineId, bool $includeShared): void
    {
        $groupId = (int) DB::table('products')->where('id', $machineId)->value('group_id');

        $q->where(function ($w) use ($machineId, $groupId, $includeShared) {
            $w->whereExists(function ($sub) use ($machineId, $groupId) {
                $sub->select(DB::raw(1))->from('productables as mp')
                    ->whereColumn('mp.product_id', 'products.id')
                    ->where(function ($or) use ($machineId, $groupId) {
                        $or->where(function ($m) use ($machineId) {
                            $m->where('mp.productable_type', Productable::TYPE_PRODUCT)->where('mp.productable_id', $machineId);
                        });
                        if ($groupId) {
                            $or->orWhere(function ($g) use ($groupId) {
                                $g->where('mp.productable_type', Productable::TYPE_GROUP)->where('mp.productable_id', $groupId);
                            });
                        }
                    });
            });
            if ($includeShared) {
                $w->orWhereExists($this->natureFlag('is_service_quotation'));
            }
        });
    }

    private function applyClassification(Builder $q, array $p): void
    {
        if (!empty($p['product_type_id'])) {
            $q->where('products.product_type_id', (int) $p['product_type_id']);
        }
        $paths = [
            'product_family_id' => 'nf.id',
            'product_function_group_id' => 'ng.id',
            'product_nature_id' => 'ng.product_nature_id',
        ];
        foreach ($paths as $key => $column) {
            if (empty($p[$key])) {
                continue;
            }
            $value = (int) $p[$key];
            $q->whereIn('products.product_type_id', function ($sub) use ($column, $value) {
                $sub->select('nt.id')->from('product_types as nt')
                    ->join('product_families as nf', 'nf.id', '=', 'nt.product_family_id')
                    ->join('product_function_groups as ng', 'ng.id', '=', 'nf.product_function_group_id')
                    ->where($column, $value);
            });
        }
        if (!empty($p['product_characteristic_id'])) {
            $q->where('products.product_characteristic_id', (int) $p['product_characteristic_id']);
        }
    }

    private function applyRelated(Builder $q, array $p): void
    {
        foreach (['brand_ids' => 'products.brand_id', 'manufacture_ids' => 'products.manufacture_id', 'origin_ids' => 'products.origin_id'] as $key => $column) {
            if (!empty($p[$key])) {
                $q->whereIn($column, $this->intList($p[$key]));
            }
        }
        if (!empty($p['model_id'])) {
            $q->where('products.model_id', (int) $p['model_id']);
        }
        if (!empty($p['used_for_machine_id'])) {
            $this->whereProductable($q, Productable::TYPE_PRODUCT, (int) $p['used_for_machine_id']);
        }
        foreach ([
            'vehicle_manufact_id' => Productable::TYPE_VEHICLE_MANUFACT,
            'vehicle_brand_id' => Productable::TYPE_VEHICLE_BRAND,
            'vehicle_model_id' => Productable::TYPE_VEHICLE_MODEL,
        ] as $key => $type) {
            if (!empty($p[$key])) {
                $this->whereProductable($q, $type, (int) $p[$key]);
            }
        }
        if (!empty($p['vehicle_life_id'])) {
            $life = (int) $p['vehicle_life_id'];
            $q->whereExists(function ($sub) use ($life) {
                $sub->select(DB::raw(1))->from('product_vehicle_model_has_life as vl')
                    ->whereColumn('vl.product_id', 'products.id')->where('vl.life_id', $life);
            });
        }
    }

    private function whereProductable(Builder $q, string $type, int $id): void
    {
        $q->whereExists(function ($sub) use ($type, $id) {
            $sub->select(DB::raw(1))->from('productables as px')
                ->whereColumn('px.product_id', 'products.id')
                ->where('px.productable_type', $type)->where('px.productable_id', $id);
        });
    }

    /** Mã · tên · barcode · model · mã đặt hàng; collation unicode_ci bỏ dấu (trừ đ) */
    private function applyKeyword(Builder $q, $keyword): void
    {
        $k = escapeLikeKeyword((string) $keyword);
        if (mb_strlen(trim($k)) < 2) {
            return;
        }
        $like = '%' . trim($k) . '%';
        $q->where(function ($w) use ($like) {
            $w->where('products.code', 'like', $like)
                ->orWhere('products.name', 'like', $like)
                ->orWhere('products.barcode', 'like', $like)
                ->orWhereExists(function ($sub) use ($like) {
                    $sub->select(DB::raw(1))->from('product_models as km')
                        ->whereColumn('km.id', 'products.model_id')->where('km.name', 'like', $like);
                })
                ->orWhereExists(function ($sub) use ($like) {
                    $sub->select(DB::raw(1))->from('barcodes as kb')
                        ->whereColumn('kb.id', 'products.barcode_id')->where('kb.name', 'like', $like);
                });
        });
    }

    private function intList($values): array
    {
        return array_values(array_filter(array_map(function ($v) {
            return (int) $v;
        }, (array) $values)));
    }
}
```

- [ ] **Step 4: Chạy xanh** — Run: `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductPickerSearchTest.php` · Expected: OK (7 tests).
- [ ] **Step 5: Commit** — `git add Modules/MasterData/Services/Product/ProductPickerService.php Modules/MasterData/Tests/Feature/ProductPickerSearchTest.php && git commit -m "feat(master-data): ProductPickerService — phạm vi, bộ lọc phân loại mới, chế độ máy (A7 P4-4.2)"`

### Task 5 (4.2): `rows()` — dòng nhẹ kèm giá, tồn, cột tuỳ chọn, giá vốn theo quyền

**Files:**
- Modify: `MD/Services/Product/ProductPickerService.php` (thêm `rows`, `OPTIONAL_COLUMNS`)
- Test: thêm ca vào `MD/Tests/Feature/ProductPickerSearchTest.php`

**Interfaces:**
- Consumes: `ProductPriceReader::retailPrices(array $productIds, int $priceTypeId, int $companyId): array`,
  `ProductPriceReader::costPrices(array $productIds, int $companyId): array`, `SellableStockReader::forProducts`.
- Produces: `ProductPickerService::rows(Builder $query, int $companyId, ?int $priceTypeId, array $columns, bool $canSeeCost, int $page, int $perPage): array`
  → `['data' => Row[], 'meta' => ['current_page','per_page','total','last_page']]` (khuôn Row ở A3).

- [ ] **Step 1: Viết test fail**

```php
    /** @test */
    public function rows_tra_khuon_dong_nhe_gia_ton_va_cot_tuy_chon_gia_von_null_khi_khong_quyen()
    {
        $branch = $this->catalogBranch();
        $p = $this->product('P4 dòng nhẹ');
        $this->catalog($p, $branch['cluster']);
        $service = new ProductPickerService();
        $query = $service->query(['keyword' => 'P4 dòng nhẹ'], self::C);

        $page = $service->rows($query, self::C, 1, ['origin', 'cost_price'], false, 1, 20);
        $row = collect($page['data'])->firstWhere('id', $p);
        $this->assertSame(
            ['id', 'code', 'name', 'avatar', 'model_name', 'brand_name', 'unit_name', 'product_type_name', 'price', 'sellable_qty', 'origin', 'cost_price'],
            array_keys($row)
        );
        $this->assertNull($row['cost_price'], 'không quyền giá vốn ⇒ null');
        $this->assertSame(0.0, $row['sellable_qty']);
        $this->assertSame(['current_page' => 1, 'per_page' => 20, 'total' => 1, 'last_page' => 1], $page['meta']);
    }
```

- [ ] **Step 2: Chạy, xác nhận fail** — Expected: FAIL `Call to undefined method ... rows()`.

- [ ] **Step 3: Cài đặt** (thêm vào `ProductPickerService`; `use Modules\MasterData\Services\ProductPrice\ProductPriceReader;`)

```php
    /** Cột tuỳ chọn → biểu thức SQL (cost_price đọc riêng qua ProductPriceReader theo quyền) */
    const OPTIONAL_COLUMNS = [
        'manufacturer' => '(select m.name from manufactures m where m.id = products.manufacture_id)',
        'origin' => '(select o.name from origins o where o.id = products.origin_id)',
        'barcode' => 'products.barcode',
        'order_code' => '(select b.name from barcodes b where b.id = products.barcode_id)',
        'product_type_path' => "(select concat_ws(' › ', nn.name, ng.name, nf.name, nt.name) from product_types nt"
            . ' join product_families nf on nf.id = nt.product_family_id'
            . ' join product_function_groups ng on ng.id = nf.product_function_group_id'
            . ' join product_natures nn on nn.id = ng.product_nature_id where nt.id = products.product_type_id)',
        'characteristic' => '(select c.name from product_characteristics c where c.id = products.product_characteristic_id)',
        'negotiation_limit' => 'products.sale_max_percent',
        'note' => 'products.note',
        'catalog_path' => null,   // gắn sau từ product_business_catalogs (nhiều nhánh ⇒ nối bằng "; ")
        'cost_price' => null,     // gắn sau, theo quyền
    ];

    public function rows(Builder $query, int $companyId, ?int $priceTypeId, array $columns, bool $canSeeCost, int $page, int $perPage): array
    {
        $columns = array_values(array_intersect(array_keys(self::OPTIONAL_COLUMNS), $columns));
        $total = (clone $query)->distinct()->count('products.id');

        $select = [
            'products.id', 'products.code', 'products.name', 'products.avatar',
            DB::raw('(select pm.name from product_models pm where pm.id = products.model_id) as model_name'),
            DB::raw('(select br.name from brands br where br.id = products.brand_id) as brand_name'),
            DB::raw('(select u.name from product_units pu join units u on u.id = pu.unit_id where pu.product_id = products.id and pu.is_base = 1 limit 1) as unit_name'),
            DB::raw('(select t.name from product_types t where t.id = products.product_type_id) as product_type_name'),
        ];
        foreach ($columns as $key) {
            if (self::OPTIONAL_COLUMNS[$key] !== null) {
                $select[] = DB::raw(self::OPTIONAL_COLUMNS[$key] . ' as ' . $key);
            }
        }

        $items = $query->select($select)->orderBy('products.code')->orderBy('products.id')
            ->forPage($page, $perPage)->get();
        $ids = $items->pluck('id')->map(function ($id) {
            return (int) $id;
        })->all();

        $reader = app(ProductPriceReader::class);
        $prices = $priceTypeId ? $reader->retailPrices($ids, $priceTypeId, $companyId) : [];
        $costs = in_array('cost_price', $columns, true) && $canSeeCost ? $reader->costPrices($ids, $companyId) : [];
        $stock = $this->stock->forProducts($ids, $companyId);
        $catalogs = in_array('catalog_path', $columns, true) ? $this->catalogPaths($ids, $companyId) : [];

        $data = $items->map(function ($r) use ($columns, $prices, $costs, $stock, $catalogs, $priceTypeId) {
            $row = [
                'id' => (int) $r->id, 'code' => $r->code, 'name' => $r->name, 'avatar' => $r->avatar,
                'model_name' => $r->model_name, 'brand_name' => $r->brand_name, 'unit_name' => $r->unit_name,
                'product_type_name' => $r->product_type_name,
                'price' => $priceTypeId && isset($prices[$r->id]) ? (float) $prices[$r->id] : null,
                'sellable_qty' => (float) ($stock[$r->id] ?? 0),
            ];
            foreach ($columns as $key) {
                if ($key === 'cost_price') {
                    $row[$key] = isset($costs[$r->id]) ? (float) $costs[$r->id] : null;
                } elseif ($key === 'catalog_path') {
                    $row[$key] = $catalogs[$r->id] ?? null;
                } else {
                    $row[$key] = $r->{$key};
                }
            }

            return $row;
        })->all();

        return ['data' => $data, 'meta' => [
            'current_page' => $page, 'per_page' => $perPage, 'total' => $total, 'last_page' => max(1, (int) ceil($total / $perPage)),
        ]];
    }

    /** [product_id => "Chương › Mục › Tiểu mục; …"] của công ty — 1 query cho cả trang */
    private function catalogPaths(array $ids, int $companyId): array
    {
        if (!$ids) {
            return [];
        }
        $rows = DB::table('product_business_catalogs as pbc')
            ->join('job_clusters as jc', 'jc.id', '=', 'pbc.job_cluster_id')
            ->join('job_groups as jg', 'jg.id', '=', 'jc.group_id')
            ->join('chapters as ch', 'ch.id', '=', 'jg.chapter_id')
            ->where('pbc.company_id', $companyId)->whereIn('pbc.product_id', $ids)
            ->get(['pbc.product_id', 'ch.name as chapter', 'jg.name as grp', 'jc.name as cluster']);
        $paths = [];
        foreach ($rows as $r) {
            $paths[$r->product_id][] = $r->chapter . ' › ' . $r->grp . ' › ' . $r->cluster;
        }

        return array_map(function ($list) {
            return implode('; ', $list);
        }, $paths);
    }
```

> Trước khi chạy: xác nhận `products.sale_max_percent` và `products.note` có thật (`SHOW COLUMNS FROM products LIKE 'sale_max%'` / `'note'`).
> Không có thì đọc nguồn "Định mức đàm phán giá" / "Lưu ý" mà màn chi tiết hàng hoá HRM đang dùng (`ProductDetailResource`) và thay biểu thức.
> `costPrices` / `retailPrices` gọi qua `ProductPriceReader` ⇒ file mới không chạm bảng giá ⇒ `PriceReaderWhitelistTest` vẫn xanh (Step 4 chạy kiểm).

- [ ] **Step 4: Chạy xanh + whitelist** — `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductPickerSearchTest.php && vendor/bin/phpunit Modules/MasterData/Tests/Feature/PriceReaderWhitelistTest.php` · Expected: OK.
- [ ] **Step 5: Commit** — `git commit -am "feat(master-data): ProductPickerService::rows — giá, tồn bán được, cột tuỳ chọn, giá vốn theo quyền (A7 P4-4.2)"`

### Task 6 (4.2): endpoint `search` + quyền công ty + giá vốn

**Files:**
- Create: `MD/Http/Requests/Product/ProductPickerRequest.php`, `MD/Http/Controllers/V1/Product/ProductPickerController.php`
- Modify: `MD/Routes/api.php` (nhóm `products`, ngay sau dòng `Route::get('/item-search', …)`)
- Test: `MD/Tests/Feature/ProductPickerApiTest.php`

**Interfaces:**
- Consumes: `ProductPickerService::query`, `::rows`; `listManageCompanyIdsForCurrentEmployee()`; `isCurrentEmployeeHasPermission(string)`.
- Produces: `GET /api/v1/master-data/products/product-picker/search` (A3). `ProductPickerRequest::companyId(): int`, `::params(): array`.

- [ ] **Step 1: Viết test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

/** A7 P4 — API popup chọn hàng: quyền công ty, giá vốn, phân trang */
class ProductPickerApiTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    const URL = '/api/v1/master-data/products/product-picker/search';

    private function allowCompanies(array $companyIds): void
    {
        // actAs gán role tạm cho công ty đầu; thêm company_roles cho các công ty còn lại của role đó
        $roleId = (int) DB::table('employee_has_roles')->where('employee_id', auth()->id())->value('role_id');
        foreach ($companyIds as $id) {
            DB::table('company_roles')->insertOrIgnore(['role_id' => $roleId, 'company_id' => $id]);
        }
    }

    /** @test */
    public function cong_ty_khong_duoc_lam_viec_tra_403_thieu_cong_ty_tra_422()
    {
        $this->actAs(1, ['Xem dữ liệu hàng hoá công ty']);
        $this->getJson(self::URL)->assertStatus(422)->assertJsonValidationErrors(['company_id']);
        $foreign = (int) DB::table('companies')->whereNotIn('id', listManageCompanyIdsForCurrentEmployee())->value('id');
        $this->getJson(self::URL . '?company_id=' . $foreign)->assertStatus(403);
    }

    /** @test */
    public function cong_ty_chung_tu_khac_cong_ty_dang_lam_van_doc_dung_cong_ty_chung_tu()
    {
        $this->actAs(1, ['Xem dữ liệu hàng hoá công ty']);
        $this->allowCompanies([1, 6]);
        $res = $this->getJson(self::URL . '?company_id=6&include_uncataloged=1&per_page=5')->assertOk();
        $this->assertSame(5, $res->json('meta.per_page'));
    }

    /** @test */
    public function gia_von_null_khi_khong_quyen_co_so_khi_co_quyen()
    {
        $this->actAs(1, ['Xem dữ liệu hàng hoá công ty']); // actAs chỉ tạo role khi có ≥ 1 quyền
        $this->allowCompanies([1]);
        $rows = $this->getJson(self::URL . '?company_id=1&include_uncataloged=1&columns[]=cost_price&per_page=20')->assertOk()->json('data');
        $this->assertNotEmpty($rows);
        $this->assertSame([null], array_values(array_unique(array_column($rows, 'cost_price'))));

        $this->actAs(1, ['Xem giá vốn hàng hoá']);
        $this->allowCompanies([1]);
        $rows = $this->getJson(self::URL . '?company_id=1&include_uncataloged=1&columns[]=cost_price&per_page=100')->assertOk()->json('data');
        $this->assertNotEmpty(array_filter(array_column($rows, 'cost_price'), function ($v) {
            return $v !== null;
        }), 'có quyền ⇒ ít nhất 1 dòng có giá vốn');
    }

    /** @test */
    public function per_page_toi_da_100()
    {
        $this->actAs(1, ['Xem dữ liệu hàng hoá công ty']);
        $this->allowCompanies([1]);
        $this->getJson(self::URL . '?company_id=1&per_page=500')->assertStatus(422)->assertJsonValidationErrors(['per_page']);
    }
}
```

> `actAs` (trait `ActsAsProductUser`) chỉ tạo role tạm khi có ≥ 1 quyền và gắn qua `employee_has_roles(role_id, employee_id, company_id)`;
> `listManageCompanyIdsForCurrentEmployee` (`app/Helper/PermissionHelper.php:218-240`) đọc `company_roles` (model
> `Modules\Timesheet\Entities\CompanyRole`) theo `role_id`. Trước khi chạy: `SHOW COLUMNS FROM company_roles` — có cột NOT NULL khác
> (vd `created_at`) thì thêm vào mảng `insertOrIgnore`.

- [ ] **Step 2: Chạy, xác nhận fail** — Expected: 404 (route chưa có).

- [ ] **Step 3: Request**

```php
<?php

namespace Modules\MasterData\Http\Requests\Product;

use Illuminate\Foundation\Http\FormRequest;
use Modules\MasterData\Services\Product\ProductPickerService;

/** A7 P4 — tham số popup chọn hàng (spec plan A3). Công ty chứng từ phải là công ty người dùng được làm việc. */
class ProductPickerRequest extends FormRequest
{
    const PARAMS = [
        'keyword', 'business_scope_id', 'chapter_id', 'job_group_id', 'job_cluster_id', 'uncatalogued', 'include_uncataloged',
        'in_stock', 'exclude_ids', 'product_nature_id', 'product_function_group_id', 'product_family_id', 'product_type_id',
        'product_characteristic_id', 'brand_ids', 'manufacture_ids', 'origin_ids', 'model_id', 'used_for_machine_id',
        'vehicle_manufact_id', 'vehicle_brand_id', 'vehicle_model_id', 'vehicle_life_id', 'machine_id', 'include_service_shared',
    ];

    public function authorize()
    {
        if (!$this->filled('company_id')) {
            return true; // để rules() báo 422
        }
        $allowed = array_map(function ($id) {
            return (int) $id;
        }, listManageCompanyIdsForCurrentEmployee());

        return in_array((int) $this->company_id, $allowed, true);
    }

    public function rules()
    {
        return [
            'company_id' => 'required|integer',
            'price_type_id' => 'nullable|integer',
            'keyword' => 'nullable|string|max:191',
            'page' => 'nullable|integer|min:1',
            'per_page' => 'nullable|integer|min:1|max:100',
            'columns' => 'nullable|array',
            'columns.*' => 'string|in:' . implode(',', array_keys(ProductPickerService::OPTIONAL_COLUMNS)),
            'exclude_ids' => 'nullable|array', 'exclude_ids.*' => 'integer',
            'brand_ids' => 'nullable|array', 'brand_ids.*' => 'integer',
            'manufacture_ids' => 'nullable|array', 'manufacture_ids.*' => 'integer',
            'origin_ids' => 'nullable|array', 'origin_ids.*' => 'integer',
            'ids' => 'nullable|array|max:200', 'ids.*' => 'integer',
        ];
    }

    public function attributes()
    {
        return ['company_id' => 'Công ty', 'per_page' => 'Số dòng/trang', 'columns' => 'Cột hiển thị'];
    }

    public function companyId(): int
    {
        return (int) $this->company_id;
    }

    public function params(): array
    {
        return $this->only(self::PARAMS);
    }
}
```

> `authorize()` trả false ⇒ Laravel ném 403 "This action is unauthorized." — đúng ý spec. Nếu `ApiController` của dự án đã đổi
> thông điệp 403 sang tiếng Việt qua Handler thì giữ nguyên; không thì thêm `failedAuthorization()` ném
> `AuthorizationException('Bạn không được làm việc tại công ty này')`.

- [ ] **Step 4: Controller + route**

```php
<?php

namespace Modules\MasterData\Http\Controllers\V1\Product;

use App\Http\Controllers\ApiController;
use Modules\MasterData\Http\Requests\Product\ProductPickerRequest;
use Modules\MasterData\Services\Product\ProductPickerService;

/** A7 P4 — API popup chọn hàng hoá dùng chung ERP + HRM. Thông tin hàng hoá không bảo mật; chỉ giá vốn theo quyền. */
class ProductPickerController extends ApiController
{
    const PERMISSION_COST = 'Xem giá vốn hàng hoá';

    /** @var ProductPickerService */
    private $service;

    public function __construct(ProductPickerService $service)
    {
        $this->service = $service;
    }

    public function search(ProductPickerRequest $request)
    {
        $query = $this->service->query($request->params(), $request->companyId());

        return response()->json($this->service->rows(
            $query,
            $request->companyId(),
            $request->filled('price_type_id') ? (int) $request->price_type_id : null,
            (array) $request->get('columns', []),
            isCurrentEmployeeHasPermission(self::PERMISSION_COST),
            (int) $request->get('page', 1),
            (int) $request->get('per_page', 20)
        ));
    }
}
```
`MD/Routes/api.php` — sau `Route::get('/item-search', $option . '@itemSearch');`:
```php
        // A7 P4 — popup chọn hàng hoá dùng chung ERP + HRM (không gate quyền xem; giá vốn gate trong service)
        $picker = 'V1\\Product\\ProductPickerController';
        Route::get('/product-picker/search', $picker . '@search');
        Route::get('/product-picker/tree-counts', $picker . '@treeCounts');
        Route::get('/product-picker/items', $picker . '@items');
```
(route `tree-counts` / `items` trỏ method thêm ở Task 7/8 — commit Task 6 chỉ thêm dòng `search`, 2 dòng kia thêm ở task tương ứng.)

- [ ] **Step 5: Chạy xanh** — `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductPickerApiTest.php` · Expected: OK (4 tests).
- [ ] **Step 6: Commit** — `git add Modules/MasterData/Http/Requests/Product/ProductPickerRequest.php Modules/MasterData/Http/Controllers/V1/Product/ProductPickerController.php Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductPickerApiTest.php && git commit -m "feat(master-data): API product-picker/search — 403 công ty, giá vốn theo quyền (A7 P4-4.2)"`

### Task 7 (4.2): endpoint `tree-counts`

**Files:**
- Modify: `ProductPickerService.php` (`treeCounts`), `ProductPickerController.php` (`treeCounts`), `MD/Routes/api.php`
- Test: `MD/Tests/Feature/ProductPickerTreeCountsTest.php`

**Interfaces:**
- Produces: `ProductPickerService::treeCounts(array $p, int $companyId): array` → `['clusters' => [cluster_id => int], 'total' => int, 'uncatalogued' => int|null]`.
  `total` = số hàng phân biệt (đã xếp catalog; khi `include_uncataloged` thì gồm cả ngoài catalog). FE cộng dồn `clusters` lên các cấp
  như `ProductCatalogTree` đang làm.

- [ ] **Step 1: Viết test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Services\Product\ProductPickerService;
use Tests\TestCase;

class ProductPickerTreeCountsTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    const C = 6;

    private function product(string $name, ?int $cluster): int
    {
        $id = DB::table('products')->insertGetId([
            'code' => 'P4T' . strtoupper(substr(uniqid(), -8)), 'name' => $name, 'status' => 1, 'company_id' => self::C,
            'created_at' => now(), 'updated_at' => now(),
        ]);
        DB::table('product_company_coefficients')->insert(['product_id' => $id, 'company_id' => self::C, 'coefficient' => 1, 'status' => 3]);
        if ($cluster) {
            DB::table('product_business_catalogs')->insert([
                'product_id' => $id, 'company_id' => self::C, 'job_cluster_id' => $cluster, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }

        return $id;
    }

    /** @test */
    public function dem_theo_tieu_muc_tong_phan_biet_va_chua_xep_catalog_theo_cung_bo_loc()
    {
        $a = $this->catalogBranch();
        $b = $this->catalogBranch();
        $two = $this->product('P4T Bơm hai nhánh', $a['cluster']);
        DB::table('product_business_catalogs')->insert([
            'product_id' => $two, 'company_id' => self::C, 'job_cluster_id' => $b['cluster'], 'created_at' => now(), 'updated_at' => now(),
        ]);
        $this->product('P4T Bơm nhánh A', $a['cluster']);
        $this->product('P4T Van nhánh B', $b['cluster']);
        $this->product('P4T Bơm ngoài catalog', null);

        $service = new ProductPickerService();
        $counts = $service->treeCounts(['keyword' => 'P4T Bơm'], self::C);
        $this->assertSame(2, $counts['clusters'][$a['cluster']]);
        $this->assertSame(1, $counts['clusters'][$b['cluster']]);
        $this->assertSame(2, $counts['total'], 'hàng 2 nhánh đếm 1 lần');
        $this->assertNull($counts['uncatalogued']);

        $wide = $service->treeCounts(['keyword' => 'P4T Bơm', 'include_uncataloged' => 1, 'job_cluster_id' => $a['cluster']], self::C);
        $this->assertSame(3, $wide['total'], 'bỏ qua nhánh đang chọn; gồm hàng ngoài catalog');
        $this->assertSame(1, $wide['uncatalogued']);
    }
}
```

- [ ] **Step 2: Chạy, xác nhận fail.**
- [ ] **Step 3: Cài đặt**

```php
    public function treeCounts(array $p, int $companyId): array
    {
        $base = $this->query($p, $companyId, false);

        $clusters = (clone $base)
            ->join('product_business_catalogs as cnt', function ($j) use ($companyId) {
                $j->on('cnt.product_id', '=', 'products.id')->where('cnt.company_id', '=', $companyId);
            })
            ->groupBy('cnt.job_cluster_id')
            ->select('cnt.job_cluster_id', DB::raw('COUNT(DISTINCT products.id) as n'))
            ->pluck('n', 'cnt.job_cluster_id');

        $uncatalogued = null;
        if (!empty($p['include_uncataloged']) && empty($p['machine_id'])) {
            $uncatalogued = (clone $base)->whereNotExists(function ($sub) use ($companyId) {
                $sub->select(DB::raw(1))->from('product_business_catalogs as u')
                    ->whereColumn('u.product_id', 'products.id')->where('u.company_id', $companyId);
            })->count(DB::raw('DISTINCT products.id'));
        }

        return [
            'clusters' => $clusters->map(function ($n) {
                return (int) $n;
            })->all(),
            'total' => (int) (clone $base)->count(DB::raw('DISTINCT products.id')),
            'uncatalogued' => $uncatalogued === null ? null : (int) $uncatalogued,
        ];
    }
```
Controller:
```php
    public function treeCounts(ProductPickerRequest $request)
    {
        return response()->json(['data' => $this->service->treeCounts($request->params(), $request->companyId())]);
    }
```
Route: `Route::get('/product-picker/tree-counts', $picker . '@treeCounts');`

- [ ] **Step 4: Chạy xanh** + thêm 1 ca HTTP vào `ProductPickerApiTest`: `tree-counts` với công ty ngoài danh sách ⇒ 403.
- [ ] **Step 5: Commit** — `git commit -am "feat(master-data): API product-picker/tree-counts (A7 P4-4.2)"` (thêm file test mới bằng `git add` trước).

### Task 8 (4.2): endpoint `items`, đối chiếu tồn với ERP, đo tốc độ + index

**Files:**
- Modify: `ProductPickerService.php` (`items`), `ProductPickerController.php` (`items`), `MD/Routes/api.php`
- Create (chỉ khi đo cần): `hrm-api/database/migrations/2026_10_13_000002_add_product_picker_indexes.php`
- Test: `MD/Tests/Feature/ProductPickerItemsTest.php`; script đối chiếu `HRM/.plans/gop-db/quan-ly-hang-hoa/popup-tim-kiem-hang-hoa/doi-chieu-ton.md` (ghi kết quả)

**Interfaces:**
- Consumes: `ProductPriceReader::unitOptions(array $productIds, int $priceTypeId, int $companyId): array`; `AdminData::source(Product, int)`.
- Produces: `ProductPickerService::items(array $ids, int $companyId, ?int $priceTypeId, bool $canSeeCost): array` — Item[] (A3), giữ đúng thứ tự `$ids`,
  bỏ id ngoài phạm vi (không đang KD tại công ty).

- [ ] **Step 1: Test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class ProductPickerItemsTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    /** @test */
    public function items_giu_thu_tu_bo_hang_ngoai_pham_vi_va_tra_don_vi_tinh()
    {
        $this->actAs(1, ['Xem dữ liệu hàng hoá công ty']);
        $roleId = (int) DB::table('employee_has_roles')->where('employee_id', auth()->id())->value('role_id');
        DB::table('company_roles')->insertOrIgnore(['role_id' => $roleId, 'company_id' => 1]);

        $trading = DB::table('product_company_coefficients')->where('company_id', 1)->where('status', 3)->limit(2)->pluck('product_id')->all();
        $stopped = (int) DB::table('product_company_coefficients')->where('company_id', 1)->where('status', 4)->value('product_id');
        $ids = [$trading[1], $stopped, $trading[0]];

        $items = $this->getJson('/api/v1/master-data/products/product-picker/items?company_id=1&price_type_id=1&'
            . http_build_query(['ids' => $ids]))->assertOk()->json('data');

        $this->assertSame([(int) $trading[1], (int) $trading[0]], array_column($items, 'id'));
        $this->assertArrayHasKey('units', $items[0]);
        $this->assertNotEmpty(array_filter($items[0]['units'], function ($u) {
            return $u['is_base'];
        }));
        foreach (['vat_percent', 'guarantee', 'guarantee_type', 'min_stock_qty', 'sellable_qty'] as $key) {
            $this->assertArrayHasKey($key, $items[0]);
        }
    }
}
```

- [ ] **Step 2: Chạy, xác nhận fail.**
- [ ] **Step 3: Cài đặt** — trong service:

```php
    public function items(array $ids, int $companyId, ?int $priceTypeId, bool $canSeeCost): array
    {
        $ids = $this->intList($ids);
        if (!$ids) {
            return [];
        }
        $query = $this->query(['include_uncataloged' => 1], $companyId, false)->whereIn('products.id', $ids);
        $page = $this->rows($query, $companyId, $priceTypeId, $canSeeCost ? ['cost_price'] : [], $canSeeCost, 1, count($ids));
        $rows = collect($page['data'])->keyBy('id');

        $products = \Modules\MasterData\Entities\Product\Product::query()->whereIn('id', $rows->keys()->all())
            ->with('companies')->get()->keyBy('id');
        $units = $priceTypeId ? app(ProductPriceReader::class)->unitOptions($rows->keys()->all(), $priceTypeId, $companyId) : [];

        $result = [];
        foreach ($ids as $id) {
            if (!$rows->has($id)) {
                continue;
            }
            $admin = \Modules\MasterData\Transformers\Product\AdminData::source($products[$id], $companyId);
            $result[] = $rows[$id] + [
                'units' => array_values($units[$id] ?? []),
                'vat_percent' => $products[$id]->vat_percent === null ? null : (float) $products[$id]->vat_percent,
                'guarantee' => $admin->guarantee,
                'guarantee_type' => $admin->guarantee_type,
                'min_stock_qty' => $admin->min_stock_qty === null ? null : (float) $admin->min_stock_qty,
            ];
        }

        return $result;
    }
```

> Trước khi viết: đọc `ProductPriceReader::unitOptions` (L119) để biết khuôn phần tử trả về; nếu khác
> `{product_unit_id, unit_id, unit_name, is_base, price}` thì map lại trong `items()` cho đúng khuôn A3 (test khẳng định `is_base`).

Controller + route:
```php
    public function items(ProductPickerRequest $request)
    {
        return response()->json(['data' => $this->service->items(
            (array) $request->get('ids', []),
            $request->companyId(),
            $request->filled('price_type_id') ? (int) $request->price_type_id : null,
            isCurrentEmployeeHasPermission(self::PERMISSION_COST)
        )]);
    }
```
`Route::get('/product-picker/items', $picker . '@items');`

- [ ] **Step 4: Chạy xanh** — `ProductPickerItemsTest` + chạy lại cả 5 file test picker + `PriceReaderWhitelistTest`.

- [ ] **Step 5: Đối chiếu Tồn bán được với ERP trên dữ liệu thật (chỉ đọc)**
  1. ERP (`wt-erp-2d1`, `php artisan config:clear` trước — cache config trỏ prod!): lấy 200 hàng có tồn của công ty 1:
     `php artisan tinker --execute="echo json_encode(DB::query()->fromSub(App\Product::stockCompanies(), 's')->whereRaw('s.in_stock <> 0')->limit(200)->get(['product_id','company_codes','in_stocks']));" > /private/tmp/.../erp-stock.json`
  2. HRM: `SellableStockReader::forProducts(ids, 1)` qua tinker cùng 200 id ⇒ `hrm-stock.json`.
  3. So bằng 1 script PHP/Python nhỏ: lấy phần `in_stocks` ứng với mã công ty 1 trong `company_codes`; số dòng lệch phải = 0.
     Ghi kết quả (số dòng so, số lệch, ví dụ lệch nếu có) vào `doi-chieu-ton.md`. Lệch ⇒ dừng, báo user, không sửa công thức mò.

- [ ] **Step 6: Đo tốc độ** (API 8031, token test lấy như e2e `.auth`): đo `curl -w '%{time_total}'` 5 lần mỗi ca trên `hrm_erp_giacty`:
  (a) mặc định công ty 1; (b) `include_uncataloged=1`; (c) `keyword=bom`; (d) `in_stock=1&include_uncataloged=1`; (e) `tree-counts` (b);
  (f) `machine_id=<máy có nhiều phụ tùng>&include_service_shared=1`. Mục tiêu < 1s. Ca nào ≥ 1s ⇒ `EXPLAIN` tìm bảng quét toàn bộ,
  thêm index vào migration `2026_10_13_000002_add_product_picker_indexes.php` (ứng viên đã biết: `product_vehicle_model_has_life(product_id)`
  — N84; `productables(product_id, productable_type, productable_id)`; `accounting_stocks(product_id)`; `prepick_details(company_id, product_id)`;
  `hold_details(company_id, product_id)`), mỗi index bọc kiểm tồn tại như các migration có sẵn. **Hỏi user trước khi chạy migration index
  vào DB.** Ghi bảng số đo trước/sau vào `doi-chieu-ton.md`.

- [ ] **Step 7: Commit + merge về nhánh chung (không push, không gop_db)**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api
git add Modules/MasterData/Services/Product/ProductPickerService.php Modules/MasterData/Http/Controllers/V1/Product/ProductPickerController.php \
  Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductPickerItemsTest.php
# + database/migrations/2026_10_13_000002_add_product_picker_indexes.php nếu có
git commit -m "feat(master-data): API product-picker/items + index tìm hàng (A7 P4-4.2)"
git status --short   # phải sạch trước khi merge
cd .. && git checkout feat/chuyen-doi-hang-hoa && git merge --no-ff feat/cdhh-p4-popup-chon-hang -m "Merge A7 P4 bước 4.1-4.2: cờ dịch vụ Tính chất + API popup chọn hàng"
```
Push chỉ khi user cho phép; sau push kiểm `git merge-base --is-ancestor <commit> origin/gop_db` ⇒ phải "không chứa".

---

## Tự rà (đối chiếu spec)
- Spec §3 giao diện ⇒ 4.3 (Phần A4); §4.1 phạm vi ⇒ Task 4 (`pcs.status = 3`, bỏ hàng tạm, cờ làm dịch vụ); §4.2 catalog mặc định + công tắc ⇒ Task 4/7;
  §4.3 cờ ⇒ Task 1/2; §4.4 chế độ máy ⇒ Task 4; §4.5 không lùi `product_type` ⇒ Task 4 không đọc `products.product_type`;
  §4.6 giá/giá vốn ⇒ Task 5/6; §4.7 tồn ⇒ Task 3 + đối chiếu Task 8; §5.1 quyền 403 ⇒ Task 6; tốc độ ⇒ Task 8;
  §5.2/§5.3 ⇒ 4.3/4.4 (A4, viết chi tiết khi tới lượt); §7 kiểm thử ⇒ test từng task + Playwright Task 2.
- Điều chỉnh so với spec (column-config, options, adapter trả id, giới hạn `đ`) ghi ở A1 — báo user khi trình plan.

---

## Phần C — Bước 4.3 (FE HRM) — task chi tiết (viết 13/10 sau khảo sát hrm-client)

### C0. Chốt của user 13/10 (6 câu tồn)
| # | Câu | Chốt |
|---|---|---|
| 1 | Công ty khi màn gọi không truyền công ty chứng từ | **Công ty đang làm việc** (`$auth.user.current_company_role`); màn nào có công ty riêng truyền prop sau |
| 2 | Mức thay `QuotationProductSearchModal` (2.773 dòng, 10 màn gọi) | **Chỉ thay phần tìm hàng hoá** của tab "Hàng hoá"; giữ tab dịch vụ, hàng tạm YCHG, tạo tay, dùng lại BOM, hàng con, kiểm trùng, đường `apply(items, parentRowId, groupId)` |
| 3 | `PriceAskingProductPickerModal` (cần hàng Đang nhập thông tin + hàng tạm) | **Giữ popup cũ**, ngoài phạm vi |
| 4 | `ProductItemPickerModal` (form hàng hoá, toàn bộ hàng) | **Giữ popup cũ**, ngoài phạm vi |
| 5 | Popup CSKH (chế độ máy, 5 màn) | **Đợt sau — bước 4.3b** |
| 6 | `BomBuilderAddProductModal` (0 chỗ gọi) | **Xoá trong 4.3** |

### C1. Tự chốt (khuôn, không phải nghiệp vụ)
- Thân popup tách thành `ProductPickerPanel.vue` (cây + hàng lọc + nâng cao + bảng + chọn) để **nhúng vào tab "Hàng hoá"** của
  `QuotationProductSearchModal` (popup đó đã có khung, tiêu đề, chân riêng). `V2ProductPickerModal` (vỏ modal theo mockup) làm ở 4.3b khi
  có màn đầu tiên gọi trực tiếp — YAGNI.
- Hàng "đã có trong BOM" (ngữ cảnh BOM, trang 1) hiện thành khối riêng "Hàng đã có trong BOM" phía trên bảng picker (trước đây trộn vào bảng ERP).
- Giá trong bảng = `price_type_id` màn truyền (mặc định 1 như popup cũ).
- Bấm tên hàng = thêm ngay 1 hàng (giữ hành vi cũ của popup báo giá: popup KHÔNG đóng sau khi thêm — yêu cầu cũ của user ở màn này).

### C2. Bản đồ file
| Repo | File | Việc |
|---|---|---|
| hrm-api | `MD/Services/Product/ProductPickerService.php` (`items`) + test `ProductPickerItemsTest` | Item thêm `model_id`, `brand_id`, `origin_id`, `origin_name`, `manufacture_id`, `internal_note` (`products.note`), `product_attributes` (chuỗi thông số — cùng nguồn chuỗi `specification` HRM đang dùng ở chi tiết hàng hoá) |
| hrm-client | `components/product/catalog/ProductCatalogTree.vue` | prop mới `levelCounts` (dùng thẳng số từng cấp, không cộng dồn) + `selectAnyLevel` (bấm tên Lĩnh vực/Chương/Mục cũng chọn) + nút giả "Chưa xếp catalog"; mặc định giữ nguyên hành vi cũ (popup Xây dựng catalog không đổi) |
| hrm-client | `components/modal/column-customization-modal.vue` + `utils/mixins/columnCustomizationMixin.js` | cho đổi `modalId` (mặc định giữ id cũ) — tránh mở trùng khi trang chủ cũng dùng mixin |
| hrm-client | `components/product/picker/ProductPickerPanel.vue` (mới) | thân popup theo mockup A/B |
| hrm-client | `components/product/picker/ProductPickerAdvancedFilters.vue` (mới) | khối Tìm kiếm nâng cao (phân loại 4 cấp + đặc tính, danh mục liên quan, phụ tùng xe) |
| hrm-client | `components/product/picker/productPickerApi.js` (mới) | gọi `search` / `tree-counts` / `items`, dựng query, chống race (latest-wins) |
| hrm-client | `pages/assign/quotations/components/QuotationProductSearchModal.vue` | tab "Hàng hoá": thay `V2BaseSmartFilterPanel` + bảng ERP bằng `ProductPickerPanel`; map Item → khuôn item cũ của `applySelection` |
| hrm-client | `pages/assign/bom-list/components/BomBuilderAddProductModal.vue` | xoá |
| e2e (ngoài git) | `e2e/tests/assign/product-picker-ui.spec.ts` (mới) | viết spec; chỉ chạy khi user yêu cầu |

### C3. Giao diện component
`ProductPickerPanel` props: `companyId` (Number, bắt buộc — màn gọi truyền công ty đang làm việc), `priceTypeId` (Number, mặc định 1),
`multiple` (Boolean, mặc định true), `existingIds` (Array<Number> — nhãn "Đã có"), `lockedFilters` (Object — khoá ô lọc màn truyền),
`mode` ('default' | 'service-machine'), `machineId`, `maxBodyHeight`.
Emits: `selection-change(rows[])` (dòng nhẹ đang tick, giữ qua trang), `quick-pick(row)` (bấm tên hàng).
Method public: `fetchItems(ids): Promise<Item[]>` (gọi `items`), `clearSelection()`, `reload()`.
Map Item → item cũ (trong QuotationProductSearchModal): `erp_product_id=id, code, name, model_id, model_name, brand_id, brand_name,
origin_id, origin_name, unit_id = units.is_base.unit_id, unit_name, product_attributes, internal_note, estimated_price = cost_price (null khi không
quyền), quoted_price = price, vat_percent, source='ERP'`.

### C4. Task
- **T9 (BE) items thêm trường** — test trước: `items` trả 7 khoá mới, `origin_name` khớp bảng `origins`; chạy lại cả 5 file test picker + whitelist.
- **T10 ProductCatalogTree** — thêm 2 prop + nút "Chưa xếp catalog"; Playwright: popup Xây dựng catalog (màn Hàng hoá công ty) vẫn hiện số
  cộng dồn như cũ (đo `.pct-row` count trước/sau giống nhau); spec cũ `products-catalog-popup-ui.spec.ts` phải còn đúng giả định.
- **T11 column-customization modalId** — prop `modalId` + mixin đọc `this.columnModalId || 'column-customization-modal'`; Playwright: 1 màn
  danh sách cũ bấm ⚙ vẫn mở đúng 1 modal.
- **T12 ProductPickerPanel + AdvancedFilters + api** — theo mockup đã duyệt (style đo ở đầu file mockup). Playwright đo: cột trái 330px;
  hàng lọc 1 dòng 32px; tiêu đề cột 1 dòng; số đếm cây = `tree-counts` (đo text badge so JSON); chọn Mục ⇒ "Đang xem" đúng đường dẫn và
  `meta.total` = badge; tick giữ qua trang 2; "Đã có" hiện đúng id; công tắc "Gồm cả hàng chưa xếp catalog" thêm nút "Chưa xếp catalog";
  cấu hình cột ⚙ lưu rồi mở lại còn; ⓘ tooltip hiện; không quyền giá vốn ⇒ cột Giá vốn không có trong danh sách cấu hình (tài khoản
  `user-nocost`); 1440 + 1280 không cuộn ngang trang.
- **T13 nhúng vào QuotationProductSearchModal** — tab "Hàng hoá" dùng panel; Thêm (N) gọi `fetchItems` rồi `applySelection(mapped)`; bấm tên
  ⇒ thêm ngay 1; kiểm trùng / cộng dồn / chặn trùng (`duplicateMode=block`) giữ nguyên; khối "Hàng đã có trong BOM". Playwright trên
  **báo giá** (thêm 2 hàng ⇒ 2 dòng vào lưới đúng ĐVT/giá/VAT), **BOM** (khối BOM + thêm hàng), **1 form kho** (phiếu chuyển kho,
  `duplicateMode=block`); tài khoản không quyền giá vốn ⇒ đơn giá dự kiến trống.
- **T14 xoá BomBuilderAddProductModal** — `grep -r BomBuilderAddProductModal` = 0 trước khi xoá; build Nuxt không lỗi.
- **T15 spec e2e** `e2e/tests/assign/product-picker-ui.spec.ts` (có quyền + không quyền giá vốn); không chạy cả bộ.

Không có migration, không ghi DB (trừ dữ liệu test trong transaction / bản ghi test Playwright tự xoá).

---

## Phần D — Bước 4.4 (ERP thay ruột 2 partial chính) — task chi tiết (viết 14/10 sau khảo sát `khao-sat-4.4.md`)

### D0. Chốt của user 14/10 (Q1–Q5, chi tiết `khao-sat-4.4.md` §6)
Q1 hàng chưa có giá ⇒ **hiện, giá "—"** · Q2 báo cáo ⇒ **toàn bộ hàng** · Q3 phụ lục HĐ ⇒ **popup mới khoá theo HĐ** ·
Q4 kho / kiểm kê / giữ hàng ⇒ **khoá danh sách + cột tồn theo kho** · Q5 thanh lý ⇒ **ngừng báo giá thanh lý (N93, việc riêng)**, 4.4 không làm chế độ thanh lý.

### D1. Tự chốt (kỹ thuật / UI)
- **Giữ nguyên 2 endpoint cũ** `searchProduct` / `searchProductStockBuyer` (còn ~15 chỗ gọi thẳng ngoài partial + `searchProductStockBuyerApi` cho HRM). 4.4 chỉ thay popup.
- **Danh sách khoá do ERP tính** (Q3/Q4): port nguyên văn các nhánh `*_contract_id` + `request_type=annex`, `has_stock`, `is_self_inventory` + `warehouses`,
  `position_transfers`, `has_prepick` từ `SearchController` sang 1 lớp `LegacyPickerScope` ⇒ ra `{ids[], stock_label?, stock_map?}`. HRM chỉ nhận 1 tham số
  chung `only_ids[]` — nghiệp vụ hợp đồng / kho của ERP không lan sang HRM.
- Danh sách khoá có thể hàng nghìn id ⇒ HRM `search` + `tree-counts` nhận thêm **POST** (cùng action); proxy ERP luôn gọi POST.
- **Token**: phiên SSO có `jwt_token` ⇒ dùng; `!config('app.is_use_sso')` (local) ⇒ tự ký JWT cho nhân viên đang đăng nhập (chung `JWT_SECRET`);
  SSO bật mà HRM trả 401 ⇒ JSON 401 + popup báo "Phiên đăng nhập HRM hết hạn, vui lòng đăng nhập lại".
- **Công ty chứng từ** = `Auth::user()->info->company_id` (như popup cũ).
- **Popup AngularJS 1 bản dùng chung**: partial mới `partials/modals/productPicker.blade.php` + `js/productPickerJs.blade.php`; 2 partial cũ chỉ còn
  include partial mới + **adapter** giữ đúng chữ ký `searchProduct(options, disabled)` / `searchProduct(quotation, options)` và đường trả về
  (`addProduct(row)` với `row = {id, code, code_raw, name, brand_id}`; 3 nhánh `type_add_product` của CSKH giữ nguyên trong adapter báo giá).
- **Chọn nhiều** (`has_checkbox_all`): tick ⇒ "Thêm (N)" gọi `addProduct` từng hàng; bỏ tick trong popup không xoá dòng đã thêm.
- Ô bị khoá (`disabled`) ⇒ hiện giá trị + khoá; tham số lạ không còn chép thẳng vào request (adapter chỉ dịch các khoá đã kiểm kê).
- Ánh xạ tuỳ chọn cũ ⇒ tham số mới:

| Cũ | Mới |
|---|---|
| `brand_id`, `manufacture_id` (+ disabled) | `brand_ids[]`, `manufacture_ids[]` khoá |
| `name` | `keyword` |
| `type=include_deleted` (cả 18 màn quotation-partial) | `scope=all` + bật sẵn "Gồm cả hàng chưa xếp catalog" |
| `*_contract_id` (+annex), `contract_id` (PL HĐ bán — nay mới lọc thật, theo `ContractProduct`) | `only_ids[]` + thanh "Hàng thuộc HĐ <số>" |
| `has_stock` / `is_self_inventory`+`warehouses` / `position_transfers` / `has_prepick` | `only_ids[]` + cột tồn "Tồn tại kho" / "Tồn bán được" / "SL đang giữ" do ERP điền |
| `has_product_id` (máy) | `machine_id` + công tắc `include_service_shared` |
| `is_service_quotation:true` (không máy) | `service_quotation_only=1` (hàng thuộc Tính chất có cờ "Dùng cho báo giá dịch vụ") |
| `is_liquidation` / `is_liquidation_product` | bỏ qua (Q5) |
| `price_type` của chứng từ / mặc định 1 | `price_type_id`; báo cáo không truyền ⇒ không có cột Giá |

### D2. Bản đồ file
| Repo | File | Việc |
|---|---|---|
| hrm-api | `MD/Http/Requests/Product/ProductPickerRequest.php` | + `scope` (`trading`\|`all`), `only_ids` (array ≤ 20.000), `service_quotation_only` |
| hrm-api | `MD/Services/Product/ProductPickerService.php` | `query()`: `scope=all` bỏ điều kiện Đang KD + `status<>0`, chỉ loại hàng tạm (pcc 6/7/8) + hàng làm dịch vụ; `only_ids` ⇒ `whereIn` và bỏ lọc Đang KD / catalog; `service_quotation_only` |
| hrm-api | `MD/Routes/api.php` | + `Route::post` cho `search`, `tree-counts` |
| hrm-api | `MD/Tests/Feature/ProductPickerSearchTest.php`, `ProductPickerTreeCountsTest.php` | ca mới |
| ERP | `app/Services/Hrm/HrmProductPickerProxy.php` (mới) | Guzzle + token + 401 |
| ERP | `app/Services/Product/LegacyPickerScope.php` (mới) | port nhánh danh sách khoá từ `SearchController` |
| ERP | `app/Http/Controllers/Hrm/ProductPickerProxyController.php` (mới) + `routes/web.php` nhóm admin | `/admin/hrm/product-picker/{search,tree-counts,items,options}` + `/admin/hrm/column-customizations` (whitelist: `catalog-options`, `form-options`, `vehicle-options`, `option-search`) |
| ERP | `resources/views/partials/modals/productPicker.blade.php` + `js/productPickerJs.blade.php` (mới) | popup theo mockup |
| ERP | `partials/modals/searchProduct.blade.php` + `js/searchProductJs.blade.php`; `searchProductQuotation.blade.php` + `js/searchProductQuotationJs.blade.php` | thay ruột ⇒ adapter |
| ERP | `tests/Feature/Hrm/ProductPickerProxyTest.php`, `tests/Unit/LegacyPickerScopeTest.php` (mới) | test |

### D3. Task
- **D-T1 (hrm-api) `scope=all` + `only_ids` + `service_quotation_only` + POST** — test trước: (a) `scope=all` ra hàng ngừng KD / không có dòng công ty, KHÔNG ra hàng tạm, KHÔNG ra hàng làm dịch vụ;
  (b) `only_ids` ra đúng tập id kể cả hàng ngừng KD / chưa xếp catalog, vẫn áp từ khoá + bộ lọc; (c) `tree-counts` khớp `search` ở cả 2 chế độ;
  (d) POST cho kết quả = GET; (e) `service_quotation_only` chỉ ra hàng thuộc Tính chất có cờ. Chạy lại cả 5 file test picker + whitelist G3.
- **D-T2 (ERP) `LegacyPickerScope`** — test so tập id với endpoint cũ trên `hrm_erp_giacty` (đọc, không ghi): 1 HĐ hãng, 1 PL HĐ mua NK annex, 1 HĐ DV annex,
  1 kho tự kiểm kê, 1 NV có hàng giữ. Ca PL HĐ bán (`ContractProduct`) là hành vi MỚI ⇒ test riêng.
- **D-T3 (ERP) proxy + route** — test: chuyển token đúng; local SSO tắt ⇒ tự ký; HRM 401 ⇒ JSON 401 + thông báo; HRM 403 công ty ⇒ chuyển nguyên;
  danh sách khoá ⇒ proxy gọi POST kèm `only_ids` + ghép cột tồn theo kho vào `data[]`; endpoint ngoài whitelist ⇒ 404.
- **D-T4 (ERP) popup AngularJS `productPicker`** — theo mockup đã duyệt (cây catalog, hàng lọc 1 dòng, nâng cao, bảng, cấu hình cột lưu server, chọn nhiều, "Đã có",
  thanh khoá HĐ / kho / máy / báo cáo). Playwright ERP (8090) đo: cột trái 330px, hàng lọc 1 dòng, tiêu đề cột 1 dòng, số đếm cây = `tree-counts`, tick giữ qua trang,
  cấu hình cột còn sau khi mở lại, số dạng 1,234,567; không quyền giá vốn ⇒ không có cột Giá vốn.
- **D-T5 (ERP) adapter `searchProduct`** — Playwright từng nhóm (mỗi nhóm 1 màn, đo dòng đổ vào chứng từ = id đã chọn, ĐVT / giá như popup cũ):
  YC xuất kho (`()`, chọn nhiều) · HĐ mua TN (khoá thương hiệu) · BH hãng (khoá thương hiệu + hãng, từ chối hàng khác thương hiệu) · PL HĐ hãng (khoá HĐ) ·
  PL HĐ mua TN v2 (khoá HĐ + popup KM) · Kiểm kê (cột Tồn tại kho) · Chuyển giữ hàng v2 (SL đang giữ) · Thẻ kho (báo cáo, chọn được hàng ngừng KD) ·
  CT khuyến mại (`()`) · `sale/services` (dòng cần `group` — kiểm adapter đủ trường hoặc màn tự gọi `getData`).
- **D-T6 (ERP) adapter `searchProductQuotation`** — Playwright: báo giá hãng (tab, hàng con) · báo giá dự án · báo giá thường · báo giá DV bán ("Trang thiết bị" ⇒ `service_quotation_only`) ·
  báo giá DV CSKH (3 nhánh `wr_product` / `extend_product` / `merchandise`, chế độ máy + công tắc) · 1 báo cáo kho (toàn bộ hàng).
- **D-T7 dọn** — `grep` 0 chỗ còn đọc `vehicleLifes`, HTML lọc cũ trong 2 partial; 21 view include `searchProductQuotationJs` mà không có modal: để nguyên (ghi N94), 4.5 gỡ.

Phạm vi ghi: không migration, không seeder, không chạy gì vào DB (test ERP chỉ đọc giacty; test HRM trong transaction). ERP nhánh con từ `feat/2d1-erp-khong-loi`,
HRM nhánh con từ `feat/chuyen-doi-hang-hoa`. Không merge gop_db.

---

## Phần E — Bước 4.5 (ERP: popup còn lại + gỡ code cũ) — task (viết 14/10 sau `khao-sat-4.5.md`)

### E0. Chốt / tự chốt: `khao-sat-4.5.md` §4–§5.

### E1. Task
- **E-T1 (hrm-api)** `out_of_stock=1` (tồn bán được ≤ 0; loại trừ với `in_stock`) — test search + tree-counts khớp; chạy lại bộ picker.
- **E-T2 (ERP BE)** (a) chế độ **xem tồn không giới hạn**: body `stock_view = {warehouse_id | warehouse_group_id}` ⇒ proxy gọi HRM bình thường rồi gắn `stock_qty` cho ĐÚNG các dòng trang trả về (1 truy vấn SUM `stocks` theo kho / nhóm kho của công ty) + `meta.stock_label = 'Tồn tại kho'`; (b) `LegacyPickerScope` nhánh `supplier` ⇒ ids từ `ProductSupplier` (giới hạn); (c) danh sách kho / nhóm kho của công ty cho ô chọn (endpoint options ERP). Test proxy + LegacyPickerScope.
- **E-T3 (ERP popup)** `productPicker`: config `stockView: {warehouses, groups, value}` (ô chọn kho / nhóm kho trên hàng lọc, đổi ⇒ tải lại), `stockFilter` 3 trạng thái (Tất cả / Còn tồn / Hết tồn) khi `stockView` bật, `showSupplierFilter` (ô NCC trong nâng cao). Playwright đo hàng lọc vẫn 1 dòng.
- **E-T4 (ERP)** popup Hàng tương đương (CSKH Chi tiết KH `customermanager/show_`, Báo giá DV CSKH) + Thiết bị (Báo giá DV CSKH) + Hàng KM (PL HĐ mua TN v2 tạo **và sửa**) ⇒ popup mới; callback đóng `#searchProduct`; modal lồng trên popup thiết bị (z-index). Playwright từng màn.
- **E-T5 (ERP)** YC đặt hàng gốc + NK 2 + TN mới + TN + YC hỏi chi phí VC ⇒ popup mới: bỏ modal `#searchProduct` tự viết + `submitSearch`; khoá thương hiệu / hãng; Xem tồn theo kho (gốc); NCC (TN); bấm dòng thêm, popup mở; cảnh báo trùng / khác thương hiệu giữ nguyên. Playwright từng màn.
- **E-T6 (ERP)** Lỗi thiết bị (`device_errors` ×2 + `CreateDeviceErrorModal` ×2 trong Báo giá DV CSKH) ⇒ popup mới; "Thiết bị" chọn nhiều; "Vật tư thay thế" ⇒ `serviceQuotationOnly`. Playwright.
- **E-T7 (ERP) gỡ code chết (N94)**: 19 include báo cáo + `products_approve/list` include; file `searchProductRepairJs`, `searchProductWarrtyJs`, `searchProductPromotion` (số ít), `searchProductPromotionJs` + 5 include, `searchProductForUpdate` + include ở 2 view chết, `searchProductEquivalent`, `searchServiceProduct` + JS, `searchProductPromotions`, markup `searchProductWarranty` ở Phiếu CSKH; catalog `@json` / `$scope.search` / `availableGroup` / nhánh KM trong 2 adapter (giữ `manufactures`, `cates` cho popup tạo barcode/model — chuyển sang chỗ đó). GIỮ: `searchProductWarrantyNew`, 4 method SearchController, 3 màn 0 phiếu. `git grep` 0 tham chiếu trước khi xoá từng file; Playwright hồi quy 1 màn mỗi partial chính + popup barcode/model.

Phạm vi: hrm-api (E-T1) nhánh con từ `feat/chuyen-doi-hang-hoa`; ERP nhánh con từ `feat/2d1-erp-khong-loi`. Không migration / seeder / ghi DB (trừ role tạm + dữ liệu thử gỡ khi xong). Không merge gop_db.

---

## Phần F — Bước 4.3b (HRM: popup chọn hàng CSKH còn lại) — task (viết 14/10 sau `khao-sat-4.3b.md`)

### F0. Chốt / tự chốt: `khao-sat-4.3b.md` §4–§5.

### F1. Task
- **F-T1 (hrm-client)** `ProductPickerPanel` thêm prop `serviceQuotationOnly`, `scope`; vỏ `components/product/picker/V2ProductPickerModal.vue` (khung `V2BaseModal` theo mockup: header icon + tiêu đề + dòng "Công ty … · Bảng giá …" ⓘ, thân = panel, footer "Đã chọn N" · Bỏ chọn tất cả · Thêm (N) · Đóng; props `companyId`, `priceTypeId`, `multiple`, `existingIds`, `lockedFilters`, `mode`, `machineId`, `machineName`, `serviceQuotationOnly`, `scope`; emit `select(items)` (gọi `fetchItems`) + `quick-pick`; popup lồng trên modal khác đúng lớp). Playwright đo khuôn như T12 (cột trái 330, hàng lọc 1 dòng, footer ghim đáy).
- **F-T2** YC thông tin BH-SC + Báo giá DV SC-BD-BT (`WrInformationRequestForm`, `WrQuotationForm`): vật tư theo thiết bị ⇒ chế độ máy (máy của dòng; dòng không có máy ⇒ thường); vật tư gói bảo dưỡng ⇒ `serviceQuotationOnly`; Loại hàng hoá ⇒ thường, không chặn; giữ `line-info`. Gỡ nhánh chết `mode:'device'`.
- **F-T3** Lỗi thiết bị (thiết bị: thường, nhiều; vật tư thay thế: `serviceQuotationOnly`) + Xử lý YC BH (hàng tương đương: chọn 1).
- **F-T4** Gói bảo dưỡng: máy áp dụng gom theo **Loại sản phẩm** ("Chưa phân loại" khi trống) — BE chi tiết gói trả `product_type_name` (hrm-api CustomerCare), FE gom lại; bỏ nút + `GroupSearchModal` "Chọn nhóm hàng". PHPUnit BE.
- **F-T5** Thêm thiết bị ngoài / thiết bị cũ / Tab thiết bị KH (hàng tương đương): chọn 1, popup lồng.
- **F-T6** Gỡ `ProductSearchModal.vue` + `GroupSearchModal.vue`; Tra cứu tồn công ty đổi ô tìm sang API picker; gỡ route/method BE hết người gọi (`customer-care/services/search-products|product-catalogs|search-models`, `customer-care/device-errors/search-products`) sau `git grep` 0 ở cả hrm-client; cập nhật spec e2e liên quan (không tự chạy cả bộ).

Phạm vi: hrm-client + hrm-api nhánh con từ `feat/chuyen-doi-hang-hoa` (worktree `wt-chuyen-doi-hang-hoa`). Không migration / seeder / ghi DB (trừ role tạm + bản ghi thử gỡ khi xong). Kiểm bằng Playwright MCP trên 3031/8031 từng màn. Không merge gop_db.

---

## Trạng thái các phần (wrap up 14/10/2026)
- [x] Phần A/B — 4.1 + 4.2 (API picker) — đã push 13/10
- [x] Phần C — 4.3 (FE HRM popup báo giá/BOM/kho) — đã push 14/10
- [x] Phần D — 4.4 (ERP thay ruột searchProduct + searchProductQuotation) — đã push 14/10 (api db6f95787, ERP 4a0b8a60e3)
- [x] Phần E — 4.5 (ERP popup còn lại + gỡ code cũ N94) — đã push 14/10 (api f5bf2e01c, ERP 370fdd64de)
- [x] Phần F — 4.3b (HRM CSKH + V2ProductPickerModal + all_active + ERP đồng bộ) — đã push 14/10 (api 3b7dd0f1a, client e3377eb7e, ERP d7f15cfcca)

### Checkpoint — 2026-10-14 (wrap up)
Vừa hoàn thành: A7 Phase 4 trọn (4.4 · 4.5 · 4.3b) — code + review từng task + review tổng + đã push 3 repo.
Đang làm dở: không. Role tạm / bản ghi thử đã gỡ hết (role 120113 gỡ sau khi user bỏ kiểm aria HRM). Server ERP tắt; HRM 8031/3031 chạy.
Bước tiếp theo: A7 Phase 2c (3 danh mục xe còn lại) — khảo sát; N100 (gói BD group_id → Loại SP) task riêng khi user gửi mapping. Danh sách đầy đủ: `../viec-con-lai.md` (bản 14/10).
Blocked: N100 chờ mapping user.

## Phần G — Sửa popup sau nghiệm thu (15/10/2026, user báo trực tiếp)
- [x] N129 Lọc Thương hiệu / Hãng SX / Xuất xứ ra 0 hàng (V2BaseSelectInModal bỏ qua `multiple` trần ⇒ 422) + bố cục ô tag + 2 công tắc lệch + nhãn "Gồm hàng ngoài catalog" — client
- [x] N131 Nhãn công tắc ERP đồng bộ — ERP
- [x] N132 Panel cây catalog 330 ⇒ 280px — client + ERP
- [x] N134 Cấu hình cột: bấm khi đang nạp tự mở (mixin chung) + STT khoá trong popup; Tên khoá giữ ngoại lệ — client
- [x] N135 Bảng chuẩn popup (table-sm, kẻ ô, 10/20/50/100) + sửa báo nhầm "Không có hàng hoá" lúc mới mở — client + ERP
- [x] N136 Bảng theo mẫu MISA (header phẳng #d8e7e1, hover #e6f5ef, 1 dòng "…" + tooltip đen, tên đủ trong popover, mặc định 20) — client (+ `utils/directives/overflowTooltip.js`) + ERP
- [x] Spec e2e mới `e2e/tests/master-data/product-picker-filters-ui.spec.ts` (6 ca, có cả bản ở `wt-chuyen-doi-hang-hoa/e2e`) — 6/6 xanh trên worktree 3031/8031
- [x] Push 15/10: hrm-client `41085f380`, ERP `4462d1178b` (không nằm trong origin/gop_db)
- [ ] N130 Popup nuốt lỗi request (422…) thành "0 hàng hoá" — ngoài luồng, chưa sửa

### Checkpoint — 2026-10-15 (wrap up)
Vừa hoàn thành: Phần G (N129 N131 N132 N134 N135 N136) — ĐÃ PUSH hrm-client `41085f380` + ERP `4462d1178b`; e2e popup 6/6.
Đang làm dở: không. Server ERP 8090 đã tắt; HRM 8031/3031 chạy; cấu hình cột tài khoản e2e_assign đã trả như cũ.
Bước tiếp theo: N130 (báo lỗi request thay vì "0 hàng") nếu user cho làm; còn lại theo `../viec-con-lai.md` (N100 chờ mapping, N128 chờ chốt HP, N122/N123/N126/N127).
Blocked: N100 chờ mapping user; N128 chờ chốt nghiệp vụ.

### Checkpoint — 2026-10-15 (wrap up 2 — sau merge gop_db)
Vừa hoàn thành: merge gop_db vào nhánh chung — popup báo giá giữ bản ProductPickerPanel (9 khối gop_db thuộc bảng ERP cũ), gỡ đăng ký FilePreviewModal sót; popup chạy lại đạt (20 dòng, header MISA, 0 lỗi JS). ĐÃ PUSH client `0d7c28f11`.
Đang làm dở: không.
Bước tiếp theo: N140 (port "bấm ảnh xem trước" của gop_db vào ProductPickerPanel) nếu user muốn; N130.
Blocked: —


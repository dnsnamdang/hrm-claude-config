# Đợt 2-C1 — Tạo + sửa hàng hoá do công ty tạo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Công ty tạo (quyền 1652) tạo mới và sửa hàng hoá trên HRM bằng form 2 tầng tab, ghi thẳng bảng ERP đúng bất biến ERP (mã, ĐVT, 6 dòng giá 0, dòng công ty), kèm cờ "Phụ tùng ô tô" ở Tính chất hàng hoá để ẩn/hiện tab xe.

**Architecture:** BE thêm 1 service ghi (`ProductWriteService`) + 1 FormRequest (`ProductRequest`) + 4 endpoint phụ cho form, tất cả trong `Modules/MasterData`; đường tạo và đường sửa (chủ) ghi lớp chung + tab Quản trị của công ty mình trong 1 transaction. FE dựng bộ component form riêng `components/product/form/*` (KHÔNG đụng 6 tab chỉ đọc của 2-B), tái dùng 2 thanh tab của màn chi tiết, page `create.vue` + `_id/edit.vue`.

**Tech Stack:** Laravel 8 + nwidart modules, PHP 7.4 (`/opt/homebrew/opt/php@7.4/bin/php`), PHPUnit trên DB dev `hrm_erp` trong `DatabaseTransactions` · Nuxt 2 / Vue 2, V2Base*, vee-validate v2, CKEditor 5 · Playwright (MCP để kiểm + spec e2e viết sẵn).

**Spec:** `2c-ghi/chot.md` (G1–G11, T6, H1', mục *Chốt riêng đợt 2-C1* C1–C12, A1) · `2c-ghi/c1-ton.md` (A/B tự chốt) · khảo sát `2c-ghi/c1-khao-sat-be.md`, `2c-ghi/c1-khao-sat-fe.md` · `2c-ghi/yeu-cau-ghi.md` §1.1/§1.2/§5 · `2c-ghi/erp-ghi-hang-hoa.md` §2–§7.

---

## 0. Phạm vi xin phép (đưa user duyệt "làm" — mỗi PHA xin riêng)

| | |
|---|---|
| Repo | `hrm-api` + `hrm-client`, worktree `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}` |
| Nhánh | **`feat/p2c1-tao-sua`** tạo từ `feat/chuyen-doi-hang-hoa` (api `626113419`, client `e046aff2c`) ở cả 2 repo. Xong từng pha: commit trên nhánh con; xong cả đợt: merge `--no-ff` về `feat/chuyen-doi-hang-hoa` + push. ⛔ KHÔNG `gop_db` |
| Bảng GHI (qua API khi chạy thật / trong transaction khi PHPUnit) | `products`, `product_units`, `product_unit_prices`, `product_company_coefficients`, `product_suppliers`, `product_business_catalogs`, `attribute_products`, `recipe_products`, `product_has_accessories`, `product_has_install_accessories`, `product_has_repair_accessories`, `productables`, `product_vehicle_model_has_life`, `product_tech_attachments`, `files`, `product_galleries`, `product_videos`, `product_natures` |
| Migration | **1 file**: `Modules/MasterData/Database/Migrations/2026_10_07_000001_add_is_auto_parts_to_product_natures_table.php` — thêm `product_natures.is_auto_parts` tinyint unsigned NOT NULL DEFAULT 0 |
| DB local | Chạy đúng 1 migration trên vào **`hrm_erp`** (cần trước khi chạy PHPUnit pha 1, vì PHPUnit chạy trên DB dev) — **hỏi riêng**. Không seeder, không quyền mới (1652 đã có) |
| S3 | Ảnh upload thật lên bucket `tanphat` (CMC, khoá hard-code trong `CmcS3Helper`) khi kiểm tay/e2e; PHPUnit giả lập S3 (không đẩy file) |
| Không đụng | 6 component tab chỉ đọc `components/product/detail/ProductTab*.vue`, popup 2-C3, ERP |

**3 pha, 17 task:**

| Pha | Task | Deliverable kiểm được |
|---|---|---|
| **P1 — BE nền + G11 + endpoint phụ** | 1–5 | PHPUnit `ProductNatureAutoPartsTest`, `ProductCodeGeneratorTest`, `ProductFormOptionsTest`, `ProductImageUploadTest`, `ProductCatalogApiTest` (hồi quy) xanh; `GET` 4 endpoint phụ trả đúng |
| **P2 — BE ghi tạo/sửa** | 6–9 | PHPUnit `ProductWriteApiTest` (tạo, sửa, quyền, 2 công ty, bất biến) xanh; hồi quy `ProductReadApiTest`, `ProductCompanyFoundationTest` |
| **P3 — FE** | 10–17 | Playwright MCP đo DOM từng luồng; spec `products-form-ui.spec.ts` + `products-write.api.spec.ts` viết sẵn (`--list` OK, chạy khi user yêu cầu) |

---

## Global Constraints

- Luật cao nhất `chot.md`; thứ tự: chốt > ERP đang chạy > mockup.
- **G1** hàng HRM tạo `products.status = 1`. **H1'** Lưu KHÔNG đổi trạng thái quy trình; dòng công ty tạo mới `status = 1` (Đang nhập thông tin).
- **G2** mỗi `product_units` mới: đúng **6 dòng** `product_unit_prices` (price_type_id 1..6) `price = 0, coefficient = 0, sale_max_percent = 0`; `product_units.cost_price = 0`, `buy_price = 0` ghi tường minh. Đúng 1 đơn vị cơ bản `unit_coefficient = 1`; đơn vị phụ hệ số ∉ {0, 1}.
- **G3** chỉ 1 nút **Lưu**, không Lưu nháp; báo lỗi đồng thời mọi ô (BE 422 một lượt; FE chỉ `required` ô Tên — skill form-validate).
- **G5** KHÔNG ghi kép `products.min_stock_qty / guarantee / guarantee_type`; 4 ô quản trị chỉ ghi `product_company_coefficients`.
- **G4 / A2 + D1** sửa hàng CŨ chưa có dòng công ty ⇒ CHỈ khi 4 ô quản trị (chính sách KD, tồn tối thiểu, bảo hành, đơn vị bảo hành) khác giá trị form đang hiện mới sinh dòng `coefficient = 1, status = 3` (NCC + catalog ghi bảng riêng, không cần dòng); dòng đã có (kể cả `status NULL` có hệ số cũ) ⇒ UPDATE, giữ `coefficient`, `status NULL → 3`.
- **G9a / C12** Sửa ở menu dòng màn *Hàng hoá nhập thông tin* + *Dữ liệu hàng hoá công ty* + footer chi tiết, theo `can_edit` BE trả; trạng thái 4 ẩn Sửa.
- **G11** tab *Phân loại xe* chỉ hiện khi Tính chất (suy từ Loại SP) có `is_auto_parts = 1`; Hãng xe không bắt buộc; tab *Nhóm máy* luôn hiện.
- **T6 / C3** `products.tech_coefficient` chung, chỉ công ty tạo sửa; rule `nullable|numeric|min:0|max:1000`; tạo mới mặc định 1.
- **C1** Lưu bắt buộc ≥ 1 Tiểu mục catalog (tạo + sửa, kể cả hàng cũ). **C2** Loại SP bắt buộc (cả hàng cũ). **C4** trùng Tên×Model×Thương hiệu×Hãng: tạo luôn kiểm, sửa chỉ kiểm khi 1 trong 4 ô đổi.
- **C5** ảnh không bắt buộc, ≤ 10; ảnh đầu = `products.avatar`; upload qua `CmcS3Helper::putFileProduct($file, 'erp_products')` (sinh `-thumbnail` + `-large`).
- **C6** tài liệu kỹ thuật: bảng dòng *Loại tài liệu + tệp*; giữ `product_tech_attachments.id` cũ khi sửa (tệp ở `files` khuôn `table='product_tech_attachments'`, `table_id`).
- **C7** ĐVT đã lưu KHOÁ: không xoá, không đổi `unit_id`/`unit_coefficient`/`is_base`; chỉ thêm dòng mới (+ 6 dòng giá 0).
- **C8** Loại SP thuộc Tính chất `is_auto_parts = 0` ⇒ BE xoá `productables` 3 loại xe + `product_vehicle_model_has_life` khi Lưu (FE cảnh báo trước).
- **C9** thuộc tính: chỉ dòng tick ("Bắt buộc" = dùng) mới gửi + phải có giá trị; ghi xoá-hết-chèn như ERP; FE hiển thị hợp (thuộc tính theo Loại SP ∪ thuộc tính đang có).
- **C10** chọn Loại SP tự điền % VAT chỉ khi ô VAT trống. **C11** nút "+" chỉ cạnh Model, ẩn khi thiếu quyền `Quản lý danh mục model`.
- **A1** `products.product_type` (chuỗi) để NULL (N9). `product_cate` không ghi. `rate_liquidation`, `group_id` không ghi.
- **Không** lịch sử (§14b), **không** giá ở request/response, **không** đụng `product_barcodes`, không xoá dòng công ty khác.
- `company_id` gán tay = `auth()->user()->current_company_role` ở `products`, `product_company_coefficients`, `product_suppliers`, `product_business_catalogs` (hook `BaseModel::creating` gán sai `info->company_id`).
- `productables` xoá/chèn luôn kẹp `productable_type`, không `sync()`, không `morphedByMany`.
- Cấm `$product->fill($request->all())` — gán từng cột (fillable còn `code`, `status`, `company_id`, `rate_liquidation`).
- FE: V2Base* cho mọi ô; không prop `trim`; `V2BaseRadio` option `{value,label}`; `V2BaseDataTable` slot `#cell-<key>`; mỗi hàng form đủ 12 cột; marker lỗi `.v2-error`; không chờ `networkidle` trong e2e; e2e `--workers=1`; KHÔNG tự chạy e2e (chỉ `--list`), nhưng BẮT BUỘC kiểm bằng Playwright MCP + đo DOM trước khi báo xong.
- Test quyền: luôn 2 phía có/không quyền 1652; ca 2 công ty ghi chéo ⇒ 403.
- **Quyền — 2 đường đọc khác nhau (lead kiểm 07/10):** middleware `checkPermission` đọc `getAllPermissions()` (gán thẳng + qua role, KHÔNG lọc công ty); `PermissionService::isCurrentEmployeeHasPermission` (dùng cho `can_edit`, `can_*`) chỉ đọc quyền **qua role + `role_has_permissions.company_id = current_company_role`**. Trait `ActsAsProductUser` hiện gán `employee_has_permissions` (dòng 57) ⇒ `can_edit` sẽ ra false ở ca có quyền. Task đầu tiên đụng trait: đổi sang **role tạm** (`roles` + `role_has_permissions.company_id` + `employee_has_roles`) rồi `RequestCache::flush()`; giữ hồi quy 2-B/2-C3 xanh. `can_edit` dùng `PermissionService` (theo công ty hiện tại) — đúng ý nghĩa gate theo công ty.

## Review Focus

1. **Hàng CŨ bị chặn Lưu vì dữ liệu cũ** (tech_coefficient = 0 ở 11.156 hàng, 30 nhóm trùng tên, 356 hàng không ảnh, ĐVT phụ cũ hệ số lạ): mở hàng cũ, chỉ chọn Loại SP + 1 Tiểu mục rồi Lưu phải qua. → test `sua_hang_cu_chi_bo_sung_loai_va_catalog_thi_luu_duoc` (Task 8).
2. **ĐVT / giá đã lưu bị ghi đè hoặc xoá**: gửi lại payload thiếu/khác ĐVT cũ ⇒ dòng `product_units` + 6 dòng giá cũ y nguyên, chỉ ĐVT mới có giá 0. → test `sua_khong_dung_dvt_cu_chi_them_dvt_moi_kem_6_dong_gia` (Task 8).
3. **`productables` xoá nhầm loại không thuộc tab**: lưu tab xe không được đụng `Group`/`App\Product` và ngược lại. → test `luu_xe_va_may_khong_dung_loai_khac` (Task 8).
4. **`company_id` bị hook gán theo `info->company_id`** thay vì `company_role` (người dùng làm việc ở công ty khác công ty gốc). → test `tao_moi_ghi_dung_cong_ty_dang_lam_viec` dùng nhân viên `company_id` gốc ≠ `company_role` (Task 7).
5. **Ảnh thiếu bản thumbnail ⇒ ảnh vỡ ở danh sách ERP**: upload phải đi `putFileProduct`, avatar = URL bản chính của ảnh đầu. → test `upload_anh_dung_putFileProduct_tra_url_ban_chinh` (Task 5) + assert avatar trong `tao_moi_ghi_du_bat_bien_erp` (Task 7).

---

## Fixture test dùng chung (đọc trước Task 1)

DB dev `hrm_erp`: `product_types` = 0 dòng, `product_families` = 0, `product_function_groups` = 0, `product_natures` = 1 dòng rác, `product_type_attributes` = 0 ⇒ mọi test cần Loại SP phải tự chèn (rollback cuối ca nhờ `DatabaseTransactions`). Thêm vào trait `Modules/MasterData/Tests/Feature/Concerns/ActsAsProductUser.php` (Task 1 bước 1):

```php
    /** Loại SP mẫu kèm 3 cấp cha. `$autoParts` = cờ Phụ tùng ô tô của Tính chất (G11) */
    protected function productTypeFixture(bool $autoParts = false, array $attributeIds = []): array
    {
        $token = 'PW' . substr(uniqid(), -6);
        $nature = DB::table('product_natures')->insertGetId([
            'code' => $token . 'N', 'name' => $token . ' Tính chất', 'barcode_template_type' => 1,
            'status' => 1, 'is_auto_parts' => $autoParts ? 1 : 0, 'created_at' => now(), 'updated_at' => now(),
        ]);
        $group = DB::table('product_function_groups')->insertGetId([
            'code' => $token . 'G', 'name' => $token . ' Nhóm CN', 'product_nature_id' => $nature,
            'status' => 1, 'created_at' => now(), 'updated_at' => now(),
        ]);
        $family = DB::table('product_families')->insertGetId([
            'code' => $token . 'F', 'name' => $token . ' Nhóm SP', 'product_function_group_id' => $group,
            'status' => 1, 'created_at' => now(), 'updated_at' => now(),
        ]);
        $type = DB::table('product_types')->insertGetId([
            'code' => $token . 'T', 'name' => $token . ' Loại SP', 'product_family_id' => $family,
            'status' => 1, 'created_at' => now(), 'updated_at' => now(),
        ]);
        foreach ($attributeIds as $attributeId) {
            DB::table('product_type_attributes')->insert([
                'product_type_id' => $type, 'attribute_id' => $attributeId, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }

        return compact('nature', 'group', 'family', 'type');
    }
```

> ⚠️ `product_types` có thể còn cột NOT NULL khác trên DB local (2 cột `declare_*` lỡ chạy batch 414). Chạy Task 1 bước 2 trước: nếu insert báo thiếu cột, bổ sung cột đó vào mảng insert với giá trị mặc định đọc từ `information_schema` — KHÔNG sửa schema.

Lệnh chạy test (mọi task BE): `cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/<File>.php` (thêm `--filter <tên ca>` khi chạy lẻ). KHÔNG `config:cache`.

---

# PHA 1 — BE nền + G11 + endpoint phụ

### Task 1: Cờ "Phụ tùng ô tô" ở Tính chất hàng hoá (G11, BE)

**Files:**
- Create: `hrm-api/Modules/MasterData/Database/Migrations/2026_10_07_000001_add_is_auto_parts_to_product_natures_table.php`
- Modify: `Modules/MasterData/Entities/ProductClassification/ProductNature.php` (`$fillable` :27-37, thêm cast)
- Modify: `Modules/MasterData/Http/Requests/ProductClassification/ProductNatureRequest.php` (`ownRules` :25)
- Modify: `Modules/MasterData/Transformers/ProductClassification/ProductNatureResource.php` (`ownFields` :8)
- Modify: `Modules/MasterData/Services/ProductClassification/ProductNatureService.php` (`fillableFrom` :40, `catalogColumns` :53, `catalogDisplay`)
- Modify: `Modules/MasterData/Services/Product/ProductOptionService.php` (`productTypes` :134-169)
- Modify: `Modules/MasterData/Tests/Feature/Concerns/ActsAsProductUser.php` (thêm `productTypeFixture` — mục Fixture)
- Test: `Modules/MasterData/Tests/Feature/ProductNatureAutoPartsTest.php`

**Interfaces:**
- Produces: cột `product_natures.is_auto_parts` (0/1); `form-options.product_types[].path.nature_is_auto_parts` (bool); resource Tính chất trả `is_auto_parts` (bool); trait `productTypeFixture(bool $autoParts = false, array $attributeIds = []): array{nature,group,family,type}`.

- [ ] **Step 1: Migration + trait fixture**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Đợt 2-C1 (G11, chốt 04/10/2026): cờ "Phụ tùng ô tô" đặt ở Tính chất hàng hoá — tab Phân loại xe
 * của form hàng hoá chỉ hiện khi Tính chất (suy từ Loại SP) có tick. Thay §18b (2 cờ ở Loại SP).
 */
class AddIsAutoPartsToProductNaturesTable extends Migration
{
    public function up()
    {
        if (!Schema::hasColumn('product_natures', 'is_auto_parts')) {
            Schema::table('product_natures', function (Blueprint $table) {
                $table->unsignedTinyInteger('is_auto_parts')->default(0)->after('barcode_template_type')
                    ->comment('1 = Phụ tùng ô tô: hiện tab Phân loại xe ở form hàng hoá (G11)');
            });
        }
    }

    public function down()
    {
        if (Schema::hasColumn('product_natures', 'is_auto_parts')) {
            Schema::table('product_natures', function (Blueprint $table) {
                $table->dropColumn('is_auto_parts');
            });
        }
    }
}
```

Thêm `productTypeFixture` (mục Fixture) vào trait.

- [ ] **Step 2: Chạy migration vào `hrm_erp` (ĐÃ được user cho phép riêng)**

Run: `/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_10_07_000001_add_is_auto_parts_to_product_natures_table.php`
Expected: `Migrated: 2026_10_07_000001_add_is_auto_parts_to_product_natures_table`. Kiểm: `php artisan tinker --execute='echo json_encode(Schema::getColumnListing("product_natures"));'` có `is_auto_parts`.

- [ ] **Step 3: Viết test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

/** Đợt 2-C1 — G11: cờ Phụ tùng ô tô ở Tính chất hàng hoá + nguồn ô chọn Loại SP của form */
class ProductNatureAutoPartsTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    /** @test */
    public function luu_va_doc_lai_co_phu_tung_o_to()
    {
        $this->actAs(1, ['Quản lý danh mục tính chất hàng hóa', 'Xem danh mục tính chất hàng hóa']);
        $code = 'PWN' . substr(uniqid(), -5);

        $id = $this->postJson('/api/v1/master-data/product-natures', [
            'code' => $code, 'name' => $code, 'status' => 1, 'barcode_template_type' => 4, 'is_auto_parts' => 1,
        ])->assertSuccessful()->json('data.id');

        $this->assertSame(1, (int) DB::table('product_natures')->where('id', $id)->value('is_auto_parts'));
        $this->getJson('/api/v1/master-data/product-natures/' . $id)->assertOk()->assertJsonPath('data.is_auto_parts', true);
    }

    /** @test */
    public function form_options_tra_co_cua_tinh_chat_theo_loai_san_pham()
    {
        $auto = $this->productTypeFixture(true);
        $plain = $this->productTypeFixture(false);
        $this->actAs(1, []);

        $types = collect($this->getJson('/api/v1/master-data/products/form-options')->assertOk()->json('data.product_types'))
            ->keyBy('id');
        $this->assertTrue($types[$auto['type']]['path']['nature_is_auto_parts']);
        $this->assertFalse($types[$plain['type']]['path']['nature_is_auto_parts']);
    }
}
```

> Trước khi viết: mở `ActsAsProductUser::actAs` — mảng id quyền cứng chỉ có 3 quyền hàng hoá. Quyền danh mục Tính chất đã có trong DB (kiểm `SELECT id FROM permissions WHERE name LIKE '%tính chất hàng hóa%'`); nếu `actAs` nhận tên quyền không có trong mảng cứng mà DB đã có thì chạy bình thường. Nếu response tạo trả id ở khoá khác `data.id`, sửa đường dẫn assert theo response thật của `BaseCatalog` (xem `ProductClassificationCatalogTest`).

- [ ] **Step 4: Chạy test — phải FAIL**

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductNatureAutoPartsTest.php`
Expected: FAIL (`is_auto_parts` không lưu / khoá `nature_is_auto_parts` không có).

- [ ] **Step 5: Code**

`ProductNature.php`: thêm `'is_auto_parts'` vào `$fillable`, thêm `protected $casts = ['is_auto_parts' => 'boolean'];` (nếu lớp cha đã có `$casts` thì merge).

`ProductNatureRequest::ownRules()`:
```php
        return [
            'barcode_template_type' => [
                'required',
                'in:' . implode(',', array_keys(ProductNature::BARCODE_TEMPLATES)),
            ],
            'is_auto_parts' => 'nullable|boolean',
        ];
```
và `attributes()` thêm `'is_auto_parts' => 'Phụ tùng ô tô'`.

`ProductNatureResource::ownFields()` thêm `'is_auto_parts' => (bool) $this->is_auto_parts,`.

`ProductNatureService`:
```php
    protected function fillableFrom(Request $request): array
    {
        return parent::fillableFrom($request) + [
            'barcode_template_type' => (int) $request->barcode_template_type,
            'is_auto_parts' => $request->boolean('is_auto_parts') ? 1 : 0,
        ];
    }

    protected function catalogColumns(): array
    {
        return array_merge(parent::catalogColumns(), ['barcode_template_type', 'is_auto_parts']);
    }
```
`catalogDisplay`: thêm nhánh `if ($column === 'is_auto_parts') return (int) $value === 1 ? 'Có' : 'Không';`. Import Excel KHÔNG đổi (B4).

`ProductOptionService::productTypes()`: thêm `'n.is_auto_parts as nature_is_auto_parts'` và `'t.vat_percent_tax_rate_id'` vào `select`; trong `path`: `'nature_is_auto_parts' => (int) $row->nature_is_auto_parts === 1,`; ở mức dòng: `'vat_percent_tax_rate_id' => $row->vat_percent_tax_rate_id ? (int) $row->vat_percent_tax_rate_id : null,` (C10 — form tự điền % VAT).

- [ ] **Step 6: Chạy test — PASS; hồi quy danh mục**

Run: `… phpunit Modules/MasterData/Tests/Feature/ProductNatureAutoPartsTest.php` → OK (2). Rồi `… phpunit Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php` → OK như trước.

- [ ] **Step 7: Commit**

```bash
git add Modules/MasterData/Database/Migrations/2026_10_07_000001_add_is_auto_parts_to_product_natures_table.php Modules/MasterData/Entities/ProductClassification/ProductNature.php Modules/MasterData/Http/Requests/ProductClassification/ProductNatureRequest.php Modules/MasterData/Transformers/ProductClassification/ProductNatureResource.php Modules/MasterData/Services/ProductClassification/ProductNatureService.php Modules/MasterData/Services/Product/ProductOptionService.php Modules/MasterData/Tests/Feature/Concerns/ActsAsProductUser.php Modules/MasterData/Tests/Feature/ProductNatureAutoPartsTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: cờ Phụ tùng ô tô ở Tính chất hàng hoá (G11)"
```

---

### Task 2: Entity còn thiếu + sinh mã (lấy từ nhánh cũ)

**Files:**
- Create: `Modules/MasterData/Entities/Product/ProductUnitPrice.php`
- Create: `Modules/MasterData/Entities/Product/ProductVehicleModelLife.php`
- Create (chép nguyên): `Modules/MasterData/Services/Product/ProductCodeGenerator.php` ← `feat/p1-danh-muc-hang-hoa`
- Create (chép rồi đổi khung): `Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php` ← `feat/p1-danh-muc-hang-hoa`
- Modify: `Modules/MasterData/Entities/Product/Product.php` (thêm quan hệ `vehicleModelLives()`)

**Interfaces:**
- Produces: `ProductUnitPrice` (bảng `product_unit_prices`, hằng `PRICE_TYPES = [1,2,3,4,5,6]`); `ProductVehicleModelLife` (bảng `product_vehicle_model_has_life`, cột `product_id, model_id, life_id`, không timestamps); `ProductCodeGenerator::generate(?int $manufactureId, ?int $barcodeId, ?int $modelId, ?int $ignoreId = null): string` (ném `RuntimeException`); `Product::vehicleModelLives(): HasMany`.

- [ ] **Step 1: Chép generator + test từ nhánh cũ**

```bash
git show feat/p1-danh-muc-hang-hoa:Modules/MasterData/Services/Product/ProductCodeGenerator.php > Modules/MasterData/Services/Product/ProductCodeGenerator.php
git show feat/p1-danh-muc-hang-hoa:Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php > Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php
git diff --stat
```

- [ ] **Step 2: Đổi khung test sang `DatabaseTransactions`**

Trong `ProductCodeGeneratorTest.php`: thêm `use Illuminate\Foundation\Testing\DatabaseTransactions;` + `use DatabaseTransactions;` trong class; XOÁ `tearDown()` + `donRac()` và lời gọi `donRac()` trong `setUp()` (giữ phần còn lại của `setUp`). Giữ nguyên 9 ca. Nếu `taoHang()` insert `products` thiếu cột NOT NULL (`status, code, name, brand_id, manufacture_id, origin_id, created_by`) thì bổ sung theo schema mục 3 khảo sát BE.

- [ ] **Step 3: Chạy — 9 ca phải PASS ngay (code lấy nguyên)**

Run: `… phpunit Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php`
Expected: OK (9 tests). Ca `test_khong_duoc_doi_ma_cua_hang_hoa_da_ton_tai` dựa `Product::boot()` đã có.

- [ ] **Step 4: 2 entity mới + quan hệ**

```php
<?php

namespace Modules\MasterData\Entities\Product;

use Illuminate\Database\Eloquent\Model;

/**
 * Giá theo loại giá của 1 đơn vị tính — bảng ERP `product_unit_prices` (264.646 dòng, KHÔNG có UNIQUE
 * (product_unit_id, price_type_id)). ERP luôn có 6 dòng / ĐVT; thiếu dòng là hàng biến mất khỏi popup
 * hoặc 404 ở `getPriceByUnitAndType` (`erp-ghi-hang-hoa.md` §6).
 *
 * HRM KHÔNG ghi giá (giá ngoài phạm vi): chỉ sinh 6 dòng giá 0 / hệ số 0 cho ĐVT MỚI (G2).
 * `extends Model` (không BaseModel): bảng không có created_by/company_id.
 */
class ProductUnitPrice extends Model
{
    /** 1 Bán lẻ · 2 Đại lý cấp 1 · 3 Đại lý cấp 2 · 4 Đại lý cấp 3 · 5 Giá bán theo lô · 6 TMĐT */
    const PRICE_TYPES = [1, 2, 3, 4, 5, 6];

    protected $table = 'product_unit_prices';

    protected $fillable = ['price_type_id', 'product_unit_id', 'price', 'coefficient', 'sale_max_percent'];
}
```

```php
<?php

namespace Modules\MasterData\Entities\Product;

use Illuminate\Database\Eloquent\Model;

/**
 * Đời xe theo model xe của hàng hoá — bảng ERP `product_vehicle_model_has_life` (48.736 dòng),
 * 3 cột `int` KHÔNG FK, không timestamps. ERP ghi xoá + chèn (`Product::syncVehicleModelLife`).
 */
class ProductVehicleModelLife extends Model
{
    protected $table = 'product_vehicle_model_has_life';

    public $timestamps = false;

    protected $fillable = ['product_id', 'model_id', 'life_id'];
}
```

`Product.php` thêm sau `vehicleModelLinks()`:
```php
    /** Đời xe theo từng model xe (bảng nối ERP, không FK) */
    public function vehicleModelLives()
    {
        return $this->hasMany(ProductVehicleModelLife::class, 'product_id');
    }
```

> ⚠️ Kiểm bảng có cột `id` không (`Schema::getColumnListing`). Nếu KHÔNG có `id`, thêm `protected $primaryKey = null; public $incrementing = false;` và mọi xoá đi `DB::table(...)->where('product_id', …)->delete()`.

- [ ] **Step 5: Hồi quy đọc**

Run: `… phpunit Modules/MasterData/Tests/Feature/ProductReadApiTest.php` → OK như trước (8).

- [ ] **Step 6: Commit**

```bash
git add Modules/MasterData/Entities/Product/ProductUnitPrice.php Modules/MasterData/Entities/Product/ProductVehicleModelLife.php Modules/MasterData/Entities/Product/Product.php Modules/MasterData/Services/Product/ProductCodeGenerator.php Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: sinh mã hàng hoá + entity giá ĐVT, đời xe"
```

---

### Task 3: Nguồn ô chọn cho form (form-options, vehicle-options, attributes-by-type, item-search)

**Files:**
- Modify: `Modules/MasterData/Services/Product/ProductOptionService.php`
- Modify: `Modules/MasterData/Http/Controllers/V1/Product/ProductOptionController.php`
- Modify: `Modules/MasterData/Routes/api.php` (khối products :253-279, route tĩnh TRƯỚC `/{product}`)
- Test: `Modules/MasterData/Tests/Feature/ProductFormOptionsTest.php`

**Interfaces:**
- Produces:
  - `GET master-data/products/form-options` thêm `machine_groups: [{id,name,is_locked}]` (bảng `groups`, 893 dòng) và `attachment_types: [{id,name,is_locked}]` (8 dòng); `include_ids` nhận thêm khoá `machine_groups`, `attachment_types`.
  - `GET master-data/products/vehicle-options` thêm `vehicle_lives: [{id,name,is_locked}]` (bảng `vehicle_life`, 61 dòng).
  - `GET master-data/products/attributes-by-type?product_type_id=` → `[{attribute_id, name}]` theo `product_type_attributes` (không gate quyền danh mục).
  - `GET master-data/products/item-search?keyword=&exclude_id=&limit=` → `[{id, code, name, base_unit_id, base_unit_name, units:[{unit_id,name}]}]`, chỉ `products.status = 1` có ĐVT cơ bản, ≤ 50.

- [ ] **Step 1: Test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

/** Đợt 2-C1 — nguồn ô chọn của form tạo/sửa hàng hoá */
class ProductFormOptionsTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private const BASE = '/api/v1/master-data/products';

    /** @test */
    public function form_options_co_nhom_may_va_loai_tai_lieu()
    {
        $this->actAs(1, []);
        $data = $this->getJson(self::BASE . '/form-options')->assertOk()->json('data');
        $this->assertNotEmpty($data['machine_groups']);
        $this->assertCount(DB::table('attachment_types')->where('status', 1)->count(), $data['attachment_types']);
    }

    /** @test */
    public function vehicle_options_co_doi_xe()
    {
        $this->actAs(1, []);
        $lives = $this->getJson(self::BASE . '/vehicle-options')->assertOk()->json('data.vehicle_lives');
        $this->assertCount(DB::table('vehicle_life')->count(), $lives);
    }

    /** @test */
    public function thuoc_tinh_theo_loai_san_pham_khong_can_quyen_danh_muc()
    {
        $attrs = DB::table('attributes')->where('status', 1)->orderBy('id')->limit(2)->pluck('id')->map('intval')->all();
        $fx = $this->productTypeFixture(false, $attrs);
        $this->actAs(1, []); // không quyền "Xem danh mục loại sản phẩm"

        $rows = $this->getJson(self::BASE . '/attributes-by-type?product_type_id=' . $fx['type'])->assertOk()->json('data');
        $this->assertSame($attrs, array_column($rows, 'attribute_id'));
    }

    /** @test */
    public function tim_hang_hoa_kem_dvt_va_loai_tru_chinh_no()
    {
        $this->actAs(1, []);
        $one = DB::table('products as p')->join('product_units as u', function ($j) {
            $j->on('u.product_id', '=', 'p.id')->where('u.is_base', 1);
        })->where('p.status', 1)->orderBy('p.id')->first(['p.id', 'p.code']);

        $rows = $this->getJson(self::BASE . '/item-search?keyword=' . urlencode($one->code))->assertOk()->json('data');
        $this->assertSame($one->id, $rows[0]['id']);
        $this->assertNotNull($rows[0]['base_unit_id']);

        $rows = $this->getJson(self::BASE . '/item-search?keyword=' . urlencode($one->code) . '&exclude_id=' . $one->id)->json('data');
        $this->assertNotContains($one->id, array_column($rows, 'id'));
    }
}
```

- [ ] **Step 2: FAIL** — Run `… phpunit Modules/MasterData/Tests/Feature/ProductFormOptionsTest.php` → 4 lỗi (khoá thiếu / 404 route).

- [ ] **Step 3: Code service**

Trong `formOptions()` thêm 2 khoá:
```php
            // --- Đợt 2-C1: tab Nhóm máy + Tài liệu kỹ thuật ---
            'machine_groups' => $this->plainOptions('groups', $include['machine_groups']),
            'attachment_types' => $this->plainOptions('attachment_types', $include['attachment_types']),
```
`includeIds()`: thêm `'machine_groups', 'attachment_types'` vào `$keys`.

Hàm mới:
```php
    /** Bảng ERP 2 trạng thái 0/1 không có model HRM riêng: trả đang hoạt động + bản ghi đang chọn */
    private function plainOptions(string $table, array $includeIds): array
    {
        $query = DB::table($table)->select(['id', 'name', 'status']);
        $this->whereActiveOrIncluded($query, 'status', 1, $includeIds, 'id');

        return $query->orderBy('name')->get()->map(function ($row) {
            return ['id' => $row->id, 'name' => $row->name, 'is_locked' => (int) $row->status !== 1];
        })->all();
    }

    /** Thuộc tính khai cho Loại SP (`product_type_attributes`) — nguồn bảng thuộc tính tab Thông số (C9) */
    public function attributesByType(int $productTypeId): array
    {
        return DB::table('product_type_attributes as pta')
            ->join('attributes as a', 'a.id', '=', 'pta.attribute_id')
            ->where('pta.product_type_id', $productTypeId)
            ->orderBy('a.position')->orderBy('a.id')
            ->get(['a.id as attribute_id', 'a.name'])
            ->map(function ($row) {
                return ['attribute_id' => (int) $row->attribute_id, 'name' => $row->name];
            })->all();
    }

    /**
     * Tìm hàng hoá cho 4 bảng hàng kèm theo + bảng Máy (tab Nhóm máy). Chỉ hàng ERP đang hoạt động có
     * ĐVT cơ bản: ERP `syncRecipeProducts` lấy `unit_id` = ĐVT cơ bản của hàng thành phần và
     * `syncAccessories` `firstOrFail` dòng `product_units(product_id, unit_id)`.
     */
    public function itemSearch(string $keyword, ?int $excludeId, int $limit): array
    {
        $limit = max(1, min($limit ?: self::SEARCH_LIMIT, self::SEARCH_LIMIT_MAX));
        $query = DB::table('products as p')
            ->join('product_units as bu', function ($join) {
                $join->on('bu.product_id', '=', 'p.id')->where('bu.is_base', 1);
            })
            ->leftJoin('units as un', 'un.id', '=', 'bu.unit_id')
            ->where('p.status', 1)
            ->select(['p.id', 'p.code', 'p.name', 'bu.unit_id as base_unit_id', 'un.name as base_unit_name']);

        if ($excludeId) {
            $query->where('p.id', '<>', $excludeId);
        }
        if ($keyword !== '') {
            $query->where(function ($w) use ($keyword) {
                $w->where('p.code', 'like', '%' . $keyword . '%')->orWhere('p.name', 'like', '%' . $keyword . '%');
            });
        }

        $rows = $query->orderBy('p.code')->limit($limit)->get();
        $units = DB::table('product_units as pu')->join('units as u', 'u.id', '=', 'pu.unit_id')
            ->whereIn('pu.product_id', $rows->pluck('id'))
            ->get(['pu.product_id', 'pu.unit_id', 'u.name'])->groupBy('product_id');

        return $rows->map(function ($row) use ($units) {
            return [
                'id' => (int) $row->id, 'code' => $row->code, 'name' => $row->name,
                'base_unit_id' => (int) $row->base_unit_id, 'base_unit_name' => $row->base_unit_name,
                'units' => collect($units->get($row->id, []))->map(function ($u) {
                    return ['unit_id' => (int) $u->unit_id, 'name' => $u->name];
                })->values()->all(),
            ];
        })->all();
    }
```
`vehicleOptions()` thêm `'vehicle_lives' => $this->vehicleLives(),` với
```php
    /** Đời xe — bảng ERP `vehicle_life` (61 dòng), trả hết kèm `is_locked` như 3 cấp xe */
    private function vehicleLives(): array
    {
        return DB::table('vehicle_life')->orderBy('name')->get(['id', 'name', 'status'])
            ->map(function ($row) {
                return ['id' => $row->id, 'name' => $row->name, 'is_locked' => (int) $row->status !== 1];
            })->all();
    }
```
> Kiểm `attributes.position` có thật (đã đo: có). Kiểm `groups.status`/`attachment_types.status` 1 = hoạt động (đo: có cột `status`).

- [ ] **Step 4: Controller + route**

`ProductOptionController`:
```php
    public function attributesByType(Request $request)
    {
        $request->validate(['product_type_id' => 'required|integer|exists:product_types,id']);

        return $this->responseJson('success', Response::HTTP_OK, $this->service->attributesByType((int) $request->product_type_id));
    }

    public function itemSearch(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->itemSearch(
            trim((string) $request->get('keyword', '')),
            $request->filled('exclude_id') ? (int) $request->exclude_id : null,
            (int) $request->get('limit', 0)
        ));
    }
```
(Đặt cùng kiểu với `formOptions`/`vehicleOptions` đang có — dùng đúng tên property service của controller, đọc file trước.)

`Routes/api.php` sau `Route::get('/option-search', …)`:
```php
        Route::get('/attributes-by-type', $option . '@attributesByType');
        Route::get('/item-search', $option . '@itemSearch');
```

- [ ] **Step 5: PASS** — `… phpunit Modules/MasterData/Tests/Feature/ProductFormOptionsTest.php` → OK (4). Hồi quy `ProductReadApiTest` → OK.

- [ ] **Step 6: Commit**

```bash
git add Modules/MasterData/Services/Product/ProductOptionService.php Modules/MasterData/Http/Controllers/V1/Product/ProductOptionController.php Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductFormOptionsTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: nguồn ô chọn form (nhóm máy, loại tài liệu, đời xe, thuộc tính theo loại, tìm hàng)"
```

---

### Task 4: Tách luật "nhánh catalog đang mở" để form dùng chung (B2)

**Files:**
- Create: `Modules/MasterData/Services/Product/CatalogBranchGuard.php`
- Modify: `Modules/MasterData/Services/Product/ProductCatalogService.php` (`checkClustersOpen` :158-186 → gọi guard)

**Interfaces:**
- Produces: `CatalogBranchGuard::closedErrors(array $clusterIds): array` (mảng câu lỗi, rỗng = hợp lệ) — cùng nội dung `checkClustersOpen` hiện tại.

- [ ] **Step 1: Chuyển nguyên thân hàm**

```php
<?php

namespace Modules\MasterData\Services\Product;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Entities\BusinessCatalog\InternalBusinessScope;
use Modules\MasterData\Entities\BusinessCatalog\JobCluster;
use Modules\MasterData\Entities\BusinessCatalog\JobGroup;

/**
 * Tiểu mục chỉ nhận THÊM hàng khi thuộc cây mới (có Lĩnh vực) và cả 4 cấp đang hoạt động (chốt B2).
 * Dùng chung: popup Xây dựng catalog (2-C3) + tab Quản trị của form hàng hoá (2-C1).
 */
class CatalogBranchGuard
{
    public function closedErrors(array $clusterIds): array
    {
        // <-- dán NGUYÊN thân `ProductCatalogService::checkClustersOpen()` hiện tại (dòng 158-186) -->
    }
}
```
> Đây là chép nguyên văn khối code đang có (query join 4 bảng + vòng `foreach` tạo `$errors`), giữ đúng `use` của 4 entity như file gốc. Không viết lại logic.

Trong `ProductCatalogService`: xoá `checkClustersOpen`, thay mọi lời gọi `$this->checkClustersOpen($ids)` bằng `app(CatalogBranchGuard::class)->closedErrors($ids)`.

- [ ] **Step 2: Hồi quy 2-C3 — phải PASS không đổi**

Run: `… phpunit Modules/MasterData/Tests/Feature/ProductCatalogApiTest.php` → OK (6).

- [ ] **Step 3: Commit**

```bash
git add Modules/MasterData/Services/Product/CatalogBranchGuard.php Modules/MasterData/Services/Product/ProductCatalogService.php
git commit -m "[gop_db] Hàng hoá 2-C1: tách luật nhánh catalog đang mở dùng chung"
```

---

### Task 5: Upload ảnh hàng hoá đúng khuôn ERP (C5)

**Files:**
- Create: `Modules/MasterData/Http/Controllers/V1/Product/ProductImageController.php`
- Modify: `Modules/MasterData/Routes/api.php`
- Test: `Modules/MasterData/Tests/Feature/ProductImageUploadTest.php`

**Interfaces:**
- Produces: `POST master-data/products/upload-images` (gate 1652), form-data `files[]` (≤ 10, `image|max:5120`) → `data: [{url, thumbnail, large}]`. Service lấy `CmcS3Helper` qua container `app(\App\Helper\CmcS3Helper::class)` để test thay được.

- [ ] **Step 1: Test fail**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use App\Helper\CmcS3Helper;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Http\UploadedFile;
use Tests\TestCase;

class ProductImageUploadTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private const URL = '/api/v1/master-data/products/upload-images';

    /** @test */
    public function upload_anh_dung_putFileProduct_tra_url_ban_chinh()
    {
        $s3 = \Mockery::mock(CmcS3Helper::class);
        $s3->shouldReceive('putFileProduct')->once()->withArgs(function ($file, $folder) {
            return $folder === 'erp_products';
        })->andReturn(['https://s3/x/a.png', 'https://s3/x/a-thumbnail.png', 'https://s3/x/a-large.png']);
        $this->app->instance(CmcS3Helper::class, $s3);
        $this->actAs(1, ['Xây dựng thông tin hàng hoá']);

        $this->post(self::URL, ['files' => [UploadedFile::fake()->image('a.png')]], ['Accept' => 'application/json'])
            ->assertOk()
            ->assertJsonPath('data.0.url', 'https://s3/x/a.png')
            ->assertJsonPath('data.0.thumbnail', 'https://s3/x/a-thumbnail.png');
    }

    /** @test */
    public function khong_quyen_1652_bi_403()
    {
        $this->actAs(1, []);
        $this->post(self::URL, ['files' => [UploadedFile::fake()->image('a.png')]], ['Accept' => 'application/json'])
            ->assertStatus(403);
    }

    /** @test */
    public function qua_10_anh_bi_422()
    {
        $this->actAs(1, ['Xây dựng thông tin hàng hoá']);
        $files = array_map(function ($i) {
            return UploadedFile::fake()->image("a{$i}.png");
        }, range(1, 11));
        $this->post(self::URL, ['files' => $files], ['Accept' => 'application/json'])
            ->assertStatus(422)->assertJsonValidationErrors(['files']);
    }
}
```

- [ ] **Step 2: FAIL** — `… phpunit Modules/MasterData/Tests/Feature/ProductImageUploadTest.php` → 404.

- [ ] **Step 3: Code**

```php
<?php

namespace Modules\MasterData\Http\Controllers\V1\Product;

use App\Helper\CmcS3Helper;
use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

/**
 * Ảnh hàng hoá (C5) — ĐÚNG khuôn ERP `UploadController::uploadProductImg`: thư mục `erp_products` + 2 bản
 * `-thumbnail` (75px) / `-large` (200px). ERP dựng URL thumbnail từ `products.avatar`
 * (`app/Product.php:891-897`) ⇒ dùng `putFile` thường là ảnh vỡ ở danh sách ERP.
 */
class ProductImageController extends ApiController
{
    const MAX_FILES = 10;

    public function upload(Request $request)
    {
        $request->validate([
            'files' => 'required|array|max:' . self::MAX_FILES,
            'files.*' => 'image|max:5120',
        ], ['files.max' => 'Tối đa ' . self::MAX_FILES . ' ảnh.']);

        $s3 = app(CmcS3Helper::class);
        $out = [];
        foreach ($request->file('files') as $file) {
            $urls = $s3->putFileProduct($file, 'erp_products');
            if (!$urls) {
                return $this->responseJson('error', Response::HTTP_UNPROCESSABLE_ENTITY, null, 'Tải ảnh thất bại, vui lòng thử lại.');
            }
            $out[] = ['url' => $urls[0], 'thumbnail' => $urls[1], 'large' => $urls[2]];
        }

        return $this->responseJson('success', Response::HTTP_OK, $out);
    }
}
```
> Đọc chữ ký `ApiController::responseJson` trước khi viết nhánh lỗi; nếu không nhận tham số message thì ném `ValidationException::withMessages(['files' => 'Tải ảnh thất bại, vui lòng thử lại.'])`.

Route (trong khối products, trước `/{product}`):
```php
        Route::post('/upload-images', 'V1\Product\ProductImageController@upload')->middleware('checkPermission:' . $build);
```

- [ ] **Step 4: PASS** — 3 ca OK.

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Http/Controllers/V1/Product/ProductImageController.php Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductImageUploadTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: upload ảnh hàng hoá khuôn ERP (thumbnail/large)"
```

**🏁 Kết thúc Pha 1:** chạy cả 6 file test (`ProductNatureAutoPartsTest`, `ProductCodeGeneratorTest`, `ProductFormOptionsTest`, `ProductImageUploadTest`, `ProductCatalogApiTest`, `ProductReadApiTest`) → xanh hết; báo user, xin "làm" Pha 2.

---

# PHA 2 — BE ghi tạo / sửa

### Task 6: FormRequest `ProductRequest` (1 bộ rule cho tạo + sửa, G3)

**Files:**
- Create: `Modules/MasterData/Http/Requests/Product/ProductRequest.php` (khung từ `git show feat/p1-danh-muc-hang-hoa:Modules/MasterData/Http/Requests/Product/ProductRequest.php`, sửa theo bảng mục 2.2 khảo sát BE)

**Interfaces:**
- Consumes: `CatalogBranchGuard::closedErrors()` (Task 4).
- Produces: payload chuẩn (khoá đúng như dưới) mà `ProductWriteService` (Task 7) và FE (Task 11–16) dùng chung:

```
name*, english_name, common_name, barcode, note,
model_id*, barcode_id (Code đặt hàng), brand_id*, manufacture_id*, origin_id*,
product_type_id*, product_characteristic_id,
units*[]: {id?, unit_id*, is_base*, unit_coefficient*}
tech_attachments[]: {id?, attachment_type_id*, files[]: {id?, file_path*, name}}
galleries[]: url (≤10, phần tử đầu = avatar)
videos[]: url
weight, size, norm, standard_accessories, product_attributes (Đặc điểm), special_feature
attributes[]: {attribute_id*, value*, unittech_id, need_print}
recipes[]: {product_id*, qty*, is_main}
accessories[] / install_accessories[]: {product_id*, unit_id*, qty*}
repair_accessories[]: {product_id*}
customs_name, hs_code, min_buy_qty, vat_percent_tax_rate_id*, import_tax_tax_rate_id,
import_tax_has_co_tax_rate_id, antidump_duty_tax_rate_id, environment_tax_coefficient
vehicle_manufact_ids[], vehicle_brand_ids[], vehicle_model_ids[], vehicle_lives[]: {model_id*, life_ids[]}
machine_group_ids[], machine_ids[]
admin: {business_policy_id, min_stock_qty, guarantee, guarantee_type, supplier_ids[], job_cluster_ids*[]}
tech_coefficient
```

- [ ] **Step 1: Viết file**

```php
<?php

namespace Modules\MasterData\Http\Requests\Product;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\Rule;
use Modules\MasterData\Services\Product\CatalogBranchGuard;

/**
 * Tạo / sửa hàng hoá (đợt 2-C1). MỘT bộ rule (G3 bỏ Lưu nháp) — FormRequest gom mọi lỗi một lượt
 * ⇒ FE báo đồng thời mọi ô. Luật: `.plans/gop-db/quan-ly-hang-hoa/2c-ghi/chot.md` (G1–G11, C1–C12).
 *
 * Không nhận từ client: `code`, `status`, `company_id`, giá, `product_type` (chuỗi cũ), `product_cate`,
 * `rate_liquidation`, `group_id` — Service gán / bỏ qua.
 */
class ProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // quyền 1652 ở route; quyền chủ hàng ở Service (403)
    }

    private function productId(): ?int
    {
        $id = $this->route('product');
        return $id ? (int) $id : null;
    }

    public function rules(): array
    {
        $exists = function (string $table) {
            return 'nullable|integer|exists:' . $table . ',id';
        };

        return [
            'name' => 'required|string|max:255',
            'english_name' => 'nullable|string|max:255',
            'common_name' => 'nullable|string|max:255',
            'barcode' => 'nullable|string|max:255',
            'note' => 'nullable|string',
            'model_id' => 'required|integer|exists:product_models,id',
            'barcode_id' => $exists('barcodes'),
            'brand_id' => 'required|integer|exists:brands,id',
            'manufacture_id' => 'required|integer|exists:manufactures,id',
            'origin_id' => 'required|integer|exists:origins,id',
            'product_type_id' => 'required|integer|exists:product_types,id',
            'product_characteristic_id' => $exists('product_characteristics'),

            'units' => 'required|array|min:1',
            'units.*.id' => 'nullable|integer',
            'units.*.unit_id' => 'required|integer|distinct|exists:units,id',
            'units.*.is_base' => 'required|boolean',
            'units.*.unit_coefficient' => 'required|numeric|gt:0|max:9999999999',

            'tech_attachments' => 'nullable|array',
            'tech_attachments.*.id' => 'nullable|integer',
            'tech_attachments.*.attachment_type_id' => 'required|integer|exists:attachment_types,id',
            'tech_attachments.*.files' => 'nullable|array',
            'tech_attachments.*.files.*.file_path' => 'required|string|max:1000',
            'tech_attachments.*.files.*.name' => 'nullable|string|max:255',
            'galleries' => 'nullable|array|max:10',
            'galleries.*' => 'required|string|max:1000',
            'videos' => 'nullable|array',
            'videos.*' => 'required|string|max:1000',

            'weight' => 'nullable|numeric|min:0',
            'size' => 'nullable|string|max:255',
            'norm' => 'nullable|numeric|min:0',
            'standard_accessories' => 'nullable|string',
            'product_attributes' => 'nullable|string',
            'special_feature' => 'nullable|string',
            'attributes' => 'nullable|array',
            'attributes.*.attribute_id' => 'required|integer|distinct|exists:attributes,id',
            'attributes.*.value' => 'required|string|max:255',
            'attributes.*.unittech_id' => $exists('attribute_units'),
            'attributes.*.need_print' => 'nullable|boolean',

            'recipes' => 'nullable|array',
            'recipes.*.product_id' => 'required|integer|distinct|exists:products,id',
            'recipes.*.qty' => 'required|numeric|gt:0',
            'recipes.*.is_main' => 'nullable|boolean',
            'accessories' => 'nullable|array',
            'accessories.*.product_id' => 'required|integer|distinct|exists:products,id',
            'accessories.*.unit_id' => 'required|integer',
            'accessories.*.qty' => 'required|numeric|gt:0',
            'install_accessories' => 'nullable|array',
            'install_accessories.*.product_id' => 'required|integer|distinct|exists:products,id',
            'install_accessories.*.unit_id' => 'required|integer',
            'install_accessories.*.qty' => 'required|numeric|gt:0',
            'repair_accessories' => 'nullable|array',
            'repair_accessories.*.product_id' => 'required|integer|distinct|exists:products,id',

            'customs_name' => 'nullable|string|max:255',
            'hs_code' => 'nullable|string|max:255',
            'min_buy_qty' => 'nullable|numeric|min:0',
            'vat_percent_tax_rate_id' => 'required|integer|exists:tax_rates,id',
            'import_tax_tax_rate_id' => $exists('tax_rates'),
            'import_tax_has_co_tax_rate_id' => $exists('tax_rates'),
            'antidump_duty_tax_rate_id' => $exists('tax_rates'),
            'environment_tax_coefficient' => 'nullable|numeric|min:1|max:999.999',

            'vehicle_manufact_ids' => 'nullable|array',
            'vehicle_manufact_ids.*' => 'integer|exists:vehicle_manufacts,id',
            'vehicle_brand_ids' => 'nullable|array',
            'vehicle_brand_ids.*' => 'integer|exists:vehicle_brands,id',
            'vehicle_model_ids' => 'nullable|array',
            'vehicle_model_ids.*' => 'integer|exists:vehicle_models,id',
            'vehicle_lives' => 'nullable|array',
            'vehicle_lives.*.model_id' => 'required|integer|exists:vehicle_models,id',
            'vehicle_lives.*.life_ids' => 'array',
            'vehicle_lives.*.life_ids.*' => 'integer|exists:vehicle_life,id',

            'machine_group_ids' => 'nullable|array',
            'machine_group_ids.*' => 'integer|exists:groups,id',
            'machine_ids' => 'nullable|array',
            'machine_ids.*' => 'integer|exists:products,id',

            'tech_coefficient' => 'nullable|numeric|min:0|max:1000',

            'admin' => 'required|array',
            'admin.business_policy_id' => $exists('business_policies'),
            'admin.min_stock_qty' => 'nullable|numeric|min:0',
            'admin.guarantee' => 'nullable|integer|min:0|max:1000',
            'admin.guarantee_type' => 'nullable|in:ngay,thang,nam',
            'admin.supplier_ids' => 'nullable|array',
            'admin.supplier_ids.*' => 'integer|distinct|exists:customers,id',
            'admin.job_cluster_ids' => 'required|array|min:1',
            'admin.job_cluster_ids.*' => 'integer|distinct|exists:job_clusters,id',
        ];
    }

    public function messages(): array
    {
        return [
            'admin.job_cluster_ids.required' => 'Phải xếp hàng hoá vào ít nhất 1 Tiểu mục catalog kinh doanh.',
            'admin.job_cluster_ids.min' => 'Phải xếp hàng hoá vào ít nhất 1 Tiểu mục catalog kinh doanh.',
            'units.required' => 'Phải khai ít nhất 1 đơn vị tính.',
            'attributes.*.value.required' => 'Thuộc tính đã tick phải nhập giá trị.',
            'machine_ids.required' => 'Đã chọn nhóm máy thì phải chọn máy.',
        ];
    }

    public function attributes(): array
    {
        return [
            'name' => 'Tên hàng hoá', 'model_id' => 'Model', 'brand_id' => 'Thương hiệu',
            'manufacture_id' => 'Hãng sản xuất', 'origin_id' => 'Xuất xứ', 'product_type_id' => 'Loại sản phẩm',
            'vat_percent_tax_rate_id' => '% VAT', 'units.*.unit_id' => 'Đơn vị', 'units.*.unit_coefficient' => 'Hệ số quy đổi',
            'tech_coefficient' => 'Hệ số công nghệ', 'environment_tax_coefficient' => 'Hệ số tính thuế BVMT',
        ];
    }

    public function withValidator($validator): void
    {
        $validator->after(function ($v) {
            $this->checkUnits($v);
            $this->checkUniqueName($v);
            $this->checkKits($v);
            $this->checkMachines($v);
            $this->checkClusters($v);
        });
    }

    /** G2 + C7: đúng 1 đơn vị cơ bản hệ số 1; phụ ∉ {0,1}; dòng đã lưu không được đổi */
    private function checkUnits($v): void
    {
        $units = collect((array) $this->input('units', []));
        $saved = $this->productId()
            ? DB::table('product_units')->where('product_id', $this->productId())->get()->keyBy('id')
            : collect();

        // Dòng đã lưu luôn còn (C7) dù client có gửi hay không ⇒ gộp để kiểm "đúng 1 cơ bản"
        $merged = $saved->map(function ($u) {
            return ['unit_id' => (int) $u->unit_id, 'is_base' => (bool) $u->is_base, 'unit_coefficient' => (float) $u->unit_coefficient];
        })->values()->merge($units->filter(function ($u) {
            return empty($u['id']);
        })->map(function ($u) {
            return ['unit_id' => (int) $u['unit_id'], 'is_base' => (bool) $u['is_base'], 'unit_coefficient' => (float) $u['unit_coefficient']];
        }));

        if ($merged->where('is_base', true)->count() !== 1) {
            $v->errors()->add('units', 'Phải có đúng 1 đơn vị cơ bản.');
        }
        if ($merged->pluck('unit_id')->duplicates()->isNotEmpty()) {
            $v->errors()->add('units', 'Đơn vị tính bị trùng.');
        }
        foreach ($units as $i => $u) {
            if (!empty($u['id'])) {
                $old = $saved->get((int) $u['id']);
                if (!$old) {
                    $v->errors()->add("units.$i.unit_id", 'Đơn vị tính không thuộc hàng hoá này.');
                } elseif ((int) $old->unit_id !== (int) $u['unit_id'] || (bool) $old->is_base !== (bool) $u['is_base']
                    || abs((float) $old->unit_coefficient - (float) $u['unit_coefficient']) > 0.0001) {
                    $v->errors()->add("units.$i.unit_id", 'Đơn vị tính đã lưu không được sửa.');
                }
                continue;
            }
            if (!empty($u['is_base']) && (float) $u['unit_coefficient'] !== 1.0) {
                $v->errors()->add("units.$i.unit_coefficient", 'Đơn vị cơ bản có hệ số quy đổi bằng 1.');
            }
            if (empty($u['is_base']) && in_array((float) $u['unit_coefficient'], [0.0, 1.0], true)) {
                $v->errors()->add("units.$i.unit_coefficient", 'Hệ số quy đổi của đơn vị phụ phải khác 0 và 1.');
            }
        }
    }

    /** C4: Tên × Model × Thương hiệu × Hãng SX duy nhất; đường sửa chỉ kiểm khi 1 trong 4 ô đổi */
    private function checkUniqueName($v): void
    {
        $keys = ['name', 'model_id', 'brand_id', 'manufacture_id'];
        if ($this->productId()) {
            $old = DB::table('products')->where('id', $this->productId())->first($keys);
            $changed = $old && collect($keys)->contains(function ($k) use ($old) {
                return (string) $old->{$k} !== (string) $this->input($k);
            });
            if (!$changed) {
                return;
            }
        }
        $dup = DB::table('products')
            ->where('name', $this->input('name'))->where('model_id', $this->input('model_id'))
            ->where('brand_id', $this->input('brand_id'))->where('manufacture_id', $this->input('manufacture_id'))
            ->where('status', '<>', 0)
            ->when($this->productId(), function ($q) {
                $q->where('id', '<>', $this->productId());
            })->exists();
        if ($dup) {
            $v->errors()->add('name', 'Đã có hàng hoá cùng Tên, Model, Thương hiệu và Hãng sản xuất.');
        }
    }

    /** Hàng kèm theo không chứa chính nó; phụ kiện phải có dòng ĐVT đã chọn (ERP firstOrFail) */
    private function checkKits($v): void
    {
        foreach (['recipes', 'accessories', 'install_accessories', 'repair_accessories'] as $key) {
            foreach ((array) $this->input($key, []) as $i => $row) {
                if ($this->productId() && (int) ($row['product_id'] ?? 0) === $this->productId()) {
                    $v->errors()->add("$key.$i.product_id", 'Không chọn chính hàng hoá đang khai.');
                }
                if (in_array($key, ['accessories', 'install_accessories'], true) && !empty($row['product_id'])
                    && !DB::table('product_units')->where('product_id', $row['product_id'])->where('unit_id', $row['unit_id'] ?? 0)->exists()) {
                    $v->errors()->add("$key.$i.unit_id", 'Đơn vị tính không thuộc hàng hoá đã chọn.');
                }
            }
        }
    }

    /** Tab Nhóm máy: có nhóm thì phải có máy (mockup `*`) */
    private function checkMachines($v): void
    {
        if (count((array) $this->input('machine_group_ids', [])) && !count((array) $this->input('machine_ids', []))) {
            $v->errors()->add('machine_ids', 'Đã chọn nhóm máy thì phải chọn máy.');
        }
    }

    /** C1 + B2: Tiểu mục MỚI thêm phải thuộc nhánh đang mở; nhánh đã lưu nay bị khoá thì giữ (xem D3) */
    private function checkClusters($v): void
    {
        $ids = array_map('intval', (array) $this->input('admin.job_cluster_ids', []));
        if (!$ids) {
            return;
        }
        $saved = $this->productId()
            ? DB::table('product_business_catalogs')->where('product_id', $this->productId())
                ->where('company_id', (int) auth()->user()->current_company_role)->pluck('job_cluster_id')->map('intval')->all()
            : [];
        $added = array_values(array_diff($ids, $saved));
        foreach (app(CatalogBranchGuard::class)->closedErrors($added) as $message) {
            $v->errors()->add('admin.job_cluster_ids', $message);
        }
    }
}
```

- [ ] **Step 2: Không có test riêng** — rule được phủ bởi `ProductWriteApiTest` (Task 7–9). Lint: `/opt/homebrew/opt/php@7.4/bin/php -l Modules/MasterData/Http/Requests/Product/ProductRequest.php` → `No syntax errors`.

- [ ] **Step 3: Commit** (gộp cùng Task 7 nếu muốn 1 commit đầu chạy được — không bắt buộc)

```bash
git add Modules/MasterData/Http/Requests/Product/ProductRequest.php
git commit -m "[gop_db] Hàng hoá 2-C1: request tạo/sửa hàng hoá (1 bộ rule, báo lỗi đồng thời)"
```

---

### Task 7: `ProductWriteService::store` + `POST /products`

**Files:**
- Create: `Modules/MasterData/Services/Product/ProductWriteService.php`
- Create: `Modules/MasterData/Http/Controllers/V1/Product/ProductWriteController.php`
- Modify: `Modules/MasterData/Routes/api.php`
- Test: `Modules/MasterData/Tests/Feature/ProductWriteApiTest.php`

**Interfaces:**
- Consumes: `ProductRequest` (Task 6), `ProductCodeGenerator::generate` (Task 2), `ProductUnitPrice::PRICE_TYPES`, `ProductVehicleModelLife`, `Productable::TYPE_*`, `ProductCompany::STATUS_*`/`NEUTRAL_COEFFICIENT`, `CmcS3Helper::promoteTemporary` / `isTemporaryUrl`, `TableFileHelper::createForTable`.
- Produces: `ProductWriteService::store(array $data): Product`, `update(Product $product, array $data): Product` (Task 8); `POST master-data/products` → `{data: {id, code}}`.

- [ ] **Step 1: Test fail — đường TẠO**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use App\Helper\CmcS3Helper;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\ProductCompany;
use Modules\MasterData\Entities\Product\Productable;
use Tests\TestCase;

/**
 * Đợt 2-C1 — tạo + sửa hàng hoá do công ty tạo. Chạy trên DB dev trong transaction.
 * Công ty 6 có 0 hàng ⇒ hàng tạo ở đây dễ đếm. Luật: `2c-ghi/chot.md`.
 */
class ProductWriteApiTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private const COMPANY = 6;
    private const OTHER = 1;
    private const URL = '/api/v1/master-data/products';
    private const PERM = 'Xây dựng thông tin hàng hoá';

    protected function setUp(): void
    {
        parent::setUp();
        // Không đẩy file thật: chỉ "đóng dấu" URL tạm thành URL chính
        $s3 = \Mockery::mock(CmcS3Helper::class);
        $s3->shouldReceive('isTemporaryUrl')->andReturnUsing(function ($url) {
            return strpos($url, '/tmp/') !== false;
        });
        $s3->shouldReceive('promoteTemporary')->andReturnUsing(function ($url) {
            return str_replace('/tmp/', '/products/', $url);
        });
        $this->app->instance(CmcS3Helper::class, $s3);
    }

    private function payload(array $override = []): array
    {
        $fx = $this->productTypeFixture(false);
        $branch = $this->catalogBranch();
        $base = [
            'name' => 'PW hàng ' . uniqid(),
            'model_id' => (int) DB::table('product_models')->where('status', 1)->value('id'),
            'brand_id' => (int) DB::table('brands')->where('status', 1)->value('id'),
            'manufacture_id' => (int) DB::table('manufactures')->where('status', 1)->whereNotNull('code')->where('code', '<>', '')->value('id'),
            'origin_id' => (int) DB::table('origins')->where('status', 1)->value('id'),
            'product_type_id' => $fx['type'],
            'units' => [['unit_id' => (int) DB::table('units')->where('status', 1)->value('id'), 'is_base' => true, 'unit_coefficient' => 1]],
            'vat_percent_tax_rate_id' => (int) DB::table('tax_rates')->where('status', 1)->value('id'),
            'galleries' => ['https://s3/erp_products/a.png', 'https://s3/erp_products/b.png'],
            'admin' => [
                'min_stock_qty' => 5, 'guarantee' => 12, 'guarantee_type' => 'thang',
                'job_cluster_ids' => [$branch['cluster']],
            ],
        ];

        return array_replace_recursive($base, $override);
    }

    /** @test */
    public function tao_moi_ghi_du_bat_bien_erp()
    {
        $employeeId = $this->actAs(self::COMPANY, [self::PERM]);
        $data = $this->payload();

        $res = $this->postJson(self::URL, $data)->assertOk();
        $id = $res->json('data.id');
        $p = DB::table('products')->find($id);

        $this->assertSame(1, (int) $p->status, 'G1');
        $this->assertSame(self::COMPANY, (int) $p->company_id);
        $this->assertSame($employeeId, (int) $p->created_by);
        $this->assertNotEmpty($p->code);
        $this->assertSame($res->json('data.code'), $p->code);
        $this->assertNull($p->product_type, 'A1: cột chuỗi cũ để NULL');
        $this->assertSame(1.0, (float) $p->tech_coefficient, 'C3: mặc định 1');
        $this->assertSame('https://s3/erp_products/a.png', $p->avatar, 'C5: ảnh đầu = avatar');
        $this->assertSame(0.0, (float) $p->min_stock_qty, 'G5: không ghi kép cột chung');

        $unit = DB::table('product_units')->where('product_id', $id)->first();
        $this->assertSame(1, (int) $unit->is_base);
        $this->assertSame(0.0, (float) $unit->cost_price);
        $prices = DB::table('product_unit_prices')->where('product_unit_id', $unit->id)->orderBy('price_type_id')->get();
        $this->assertSame([1, 2, 3, 4, 5, 6], $prices->pluck('price_type_id')->map('intval')->all(), 'G2');
        $this->assertSame(0.0, (float) $prices->sum('price'));

        $row = DB::table('product_company_coefficients')->where('product_id', $id)->get();
        $this->assertCount(1, $row);
        $this->assertSame(self::COMPANY, (int) $row[0]->company_id);
        $this->assertSame(1.0, (float) $row[0]->coefficient);
        $this->assertSame(ProductCompany::STATUS_ENTERING_INFO, (int) $row[0]->status);
        $this->assertSame(12, (int) $row[0]->guarantee);

        $this->assertSame(1, DB::table('product_business_catalogs')->where('product_id', $id)->where('company_id', self::COMPANY)->count());
        $this->assertSame(2, DB::table('product_galleries')->where('product_id', $id)->count());
    }

    /** @test */
    public function tao_moi_ghi_dung_cong_ty_dang_lam_viec()
    {
        // info->company_id gốc = 1, đang làm việc (company_role) ở công ty 6 ⇒ phải ghi 6
        $this->actAs(self::COMPANY, [self::PERM]);
        DB::table('employee_infos')->where('id', auth()->user()->employee_info_id ?? 0)->update(['company_id' => self::OTHER]);
        $id = $this->postJson(self::URL, $this->payload())->assertOk()->json('data.id');

        $this->assertSame(self::COMPANY, (int) DB::table('products')->where('id', $id)->value('company_id'));
        $this->assertSame([self::COMPANY], DB::table('product_company_coefficients')->where('product_id', $id)->pluck('company_id')->map('intval')->all());
    }

    /** @test */
    public function khong_quyen_1652_bi_403()
    {
        $this->actAs(self::COMPANY, []);
        $this->postJson(self::URL, $this->payload())->assertStatus(403);
    }

    /** @test */
    public function luu_thieu_moi_thu_bao_loi_dong_thoi()
    {
        $this->actAs(self::COMPANY, [self::PERM]);
        $this->postJson(self::URL, ['admin' => []])->assertStatus(422)->assertJsonValidationErrors([
            'name', 'model_id', 'brand_id', 'manufacture_id', 'origin_id', 'product_type_id',
            'units', 'vat_percent_tax_rate_id', 'admin.job_cluster_ids',
        ]);
    }

    /** @test */
    public function dvt_khong_dung_1_co_ban_bi_422()
    {
        $this->actAs(self::COMPANY, [self::PERM]);
        $u = DB::table('units')->where('status', 1)->orderBy('id')->limit(2)->pluck('id')->map('intval')->all();
        $this->postJson(self::URL, $this->payload(['units' => [
            ['unit_id' => $u[0], 'is_base' => true, 'unit_coefficient' => 1],
            ['unit_id' => $u[1], 'is_base' => true, 'unit_coefficient' => 1],
        ]]))->assertStatus(422)->assertJsonValidationErrors(['units']);
    }

    /** @test */
    public function trung_ten_model_thuong_hieu_hang_bi_422()
    {
        $this->actAs(self::COMPANY, [self::PERM]);
        $data = $this->payload();
        $this->postJson(self::URL, $data)->assertOk();
        $again = $data;
        $again['admin']['job_cluster_ids'] = [$this->catalogBranch()['cluster']];
        $this->postJson(self::URL, $again)->assertStatus(422)->assertJsonValidationErrors(['name']);
    }

    /** @test */
    public function tai_lieu_ky_thuat_chuyen_tep_tam_sang_chinh()
    {
        $this->actAs(self::COMPANY, [self::PERM]);
        $type = (int) DB::table('attachment_types')->value('id');
        $id = $this->postJson(self::URL, $this->payload(['tech_attachments' => [[
            'attachment_type_id' => $type, 'files' => [['file_path' => 'https://s3/tanphat_hrm/tmp/x.pdf', 'name' => 'x.pdf']],
        ]]]))->assertOk()->json('data.id');

        $pta = DB::table('product_tech_attachments')->where('product_id', $id)->first();
        $file = DB::table('files')->where('table', 'product_tech_attachments')->where('table_id', $pta->id)->first();
        $this->assertSame('https://s3/tanphat_hrm/products/x.pdf', $file->file_path);
    }
}
```

> `actAs` hiện tạo `employee_infos` với `company_role` nhưng KHÔNG có `company_id` — kiểm cột `employee_infos.company_id` (nullable?) và cách `auth()->user()->employee_info_id` đọc ra; điều chỉnh ca `tao_moi_ghi_dung_cong_ty_dang_lam_viec` theo tên cột thật (giữ ý: company gốc ≠ company_role).

- [ ] **Step 2: FAIL** — `… phpunit Modules/MasterData/Tests/Feature/ProductWriteApiTest.php` → 404 route.

- [ ] **Step 3: Service**

```php
<?php

namespace Modules\MasterData\Services\Product;

use App\Helper\CmcS3Helper;
use App\Helper\TableFileHelper;
use Illuminate\Database\QueryException;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Modules\MasterData\Entities\Product\Product;
use Modules\MasterData\Entities\Product\ProductCompany;
use Modules\MasterData\Entities\Product\ProductUnitPrice;
use Modules\MasterData\Entities\Product\Productable;
use RuntimeException;

/**
 * GHI hàng hoá do công ty tạo (đợt 2-C1) — luật `.plans/gop-db/quan-ly-hang-hoa/2c-ghi/chot.md`.
 * Bám thứ tự ERP `Product::createRecord()` (`erp-ghi-hang-hoa.md` §2, §7), trừ: không giá, không duyệt
 * giá, không lịch sử, không job CRM, không ghi kép cột chung (G5), không ép `status=1`/`company_id`
 * khi sửa. Mọi bước trong 1 transaction.
 *
 * ⚠️ `company_id` gán TAY = `current_company_role` — hook `BaseModel::creating` gán `info->company_id`.
 * ⚠️ `productables` xoá/chèn luôn kẹp `productable_type`.
 */
class ProductWriteService
{
    /** Số lần sinh lại mã khi đụng UNIQUE `products_code_unique` do ghi song song */
    const CODE_RETRY = 3;

    /** @var ProductCodeGenerator */
    private $codes;

    public function __construct(ProductCodeGenerator $codes)
    {
        $this->codes = $codes;
    }

    private function companyId(): int
    {
        return (int) auth()->user()->current_company_role;
    }

    public function store(array $data): Product
    {
        for ($attempt = 1; ; $attempt++) {
            try {
                return DB::transaction(function () use ($data) {
                    $product = new Product();
                    $this->fillCommon($product, $data);
                    $product->status = Product::STATUS_ACTIVE;            // G1
                    $product->company_id = $this->companyId();
                    $product->tech_coefficient = $data['tech_coefficient'] ?? 1; // C3
                    $product->code = $this->generateCode($data);
                    $product->save();

                    $this->writeChildren($product, $data, true);
                    $this->writeAdmin($product, (array) $data['admin'], ProductCompany::STATUS_ENTERING_INFO);

                    return $product;
                });
            } catch (QueryException $e) {
                $duplicateCode = (string) $e->getCode() === '23000' && strpos($e->getMessage(), 'products_code_unique') !== false;
                if (!$duplicateCode || $attempt >= self::CODE_RETRY) {
                    throw $e;
                }
            }
        }
    }

    private function generateCode(array $data): string
    {
        try {
            return $this->codes->generate(
                (int) $data['manufacture_id'],
                !empty($data['barcode_id']) ? (int) $data['barcode_id'] : null,
                (int) $data['model_id']
            );
        } catch (RuntimeException $e) {
            throw ValidationException::withMessages(['manufacture_id' => $e->getMessage()]);
        }
    }

    /** Cột lớp chung — gán TỪNG cột (cấm fill request: fillable còn code/status/company_id/rate_liquidation) */
    private function fillCommon(Product $product, array $d): void
    {
        foreach ([
            'name', 'english_name', 'common_name', 'barcode', 'note', 'model_id', 'barcode_id', 'brand_id',
            'manufacture_id', 'origin_id', 'product_type_id', 'product_characteristic_id', 'weight', 'size', 'norm',
            'standard_accessories', 'product_attributes', 'special_feature', 'customs_name', 'hs_code', 'min_buy_qty',
            'vat_percent_tax_rate_id', 'import_tax_tax_rate_id', 'import_tax_has_co_tax_rate_id', 'antidump_duty_tax_rate_id',
        ] as $col) {
            $product->{$col} = $d[$col] ?? null;
        }
        if (array_key_exists('tech_coefficient', $d) && $d['tech_coefficient'] !== null) {
            $product->tech_coefficient = $d['tech_coefficient'];
        }

        // Thuế: BE suy % từ tax_rates như ERP (`ProductsController:1883-1896`)
        $rates = DB::table('tax_rates')->whereIn('id', array_filter([
            $d['vat_percent_tax_rate_id'] ?? null, $d['import_tax_tax_rate_id'] ?? null,
            $d['import_tax_has_co_tax_rate_id'] ?? null, $d['antidump_duty_tax_rate_id'] ?? null,
        ]))->pluck('tax_rate', 'id');
        $product->vat_percent = $rates[$d['vat_percent_tax_rate_id']] ?? null;
        $product->import_tax = isset($d['import_tax_tax_rate_id']) ? ($rates[$d['import_tax_tax_rate_id']] ?? null) : null;
        $product->import_tax_has_co = isset($d['import_tax_has_co_tax_rate_id']) ? ($rates[$d['import_tax_has_co_tax_rate_id']] ?? null) : null;
        $product->antidump_duty = isset($d['antidump_duty_tax_rate_id']) ? ($rates[$d['antidump_duty_tax_rate_id']] ?? null) : null;

        // F7: cờ BVMT do BE suy; trống ⇒ cờ 0 + hệ số 1.00 (cột NOT NULL DEFAULT 1.00)
        $env = $d['environment_tax_coefficient'] ?? null;
        $product->need_environment_tax = $env !== null && $env !== '';
        $product->environment_tax_coefficient = $product->need_environment_tax ? $env : 1;

        $galleries = array_values((array) ($d['galleries'] ?? []));
        $product->avatar = $galleries[0] ?? null; // C5: ảnh đầu = avatar
    }

    /** Bảng con của lớp chung. `$isCreate` = đường tạo (ĐVT mọi dòng là mới) */
    private function writeChildren(Product $product, array $d, bool $isCreate): void
    {
        $this->writeUnits($product, (array) $d['units']);
        $this->writeAttributes($product, (array) ($d['attributes'] ?? []));
        $this->writeKits($product, $d);
        $this->writeTechAttachments($product, (array) ($d['tech_attachments'] ?? []));
        $this->writeGalleries($product, (array) ($d['galleries'] ?? []));
        $this->writeVideos($product, (array) ($d['videos'] ?? []));
        $this->writeVehicles($product, $d);
        $this->writeLinks($product, Productable::TYPE_GROUP, (array) ($d['machine_group_ids'] ?? []));
        $this->writeLinks($product, Productable::TYPE_PRODUCT, (array) ($d['machine_ids'] ?? []));
    }

    /** C7 + G2: chỉ THÊM ĐVT chưa có id; mỗi ĐVT mới kèm 6 dòng giá 0. Dòng cũ không đụng */
    private function writeUnits(Product $product, array $units): void
    {
        foreach ($units as $u) {
            if (!empty($u['id'])) {
                continue;
            }
            $unitRowId = DB::table('product_units')->insertGetId([
                'product_id' => $product->id, 'unit_id' => $u['unit_id'], 'is_base' => !empty($u['is_base']) ? 1 : 0,
                'unit_coefficient' => !empty($u['is_base']) ? 1 : $u['unit_coefficient'],
                'cost_price' => 0, 'buy_price' => 0, 'created_at' => now(), 'updated_at' => now(),
            ]);
            DB::table('product_unit_prices')->insert(array_map(function ($type) use ($unitRowId) {
                return [
                    'price_type_id' => $type, 'product_unit_id' => $unitRowId, 'price' => 0, 'coefficient' => 0,
                    'sale_max_percent' => 0, 'created_at' => now(), 'updated_at' => now(),
                ];
            }, ProductUnitPrice::PRICE_TYPES));
        }
    }

    /** C9: chỉ dòng tick (đã lọc ở FE) — xoá hết + chèn như ERP; `created_by` NOT NULL */
    private function writeAttributes(Product $product, array $rows): void
    {
        DB::table('attribute_products')->where('product_id', $product->id)->delete();
        $by = (int) auth()->user()->id;
        foreach ($rows as $r) {
            DB::table('attribute_products')->insert([
                'product_id' => $product->id, 'attribute_id' => $r['attribute_id'], 'value' => $r['value'],
                'unittech_id' => $r['unittech_id'] ?? null, 'need_print' => !empty($r['need_print']) ? 1 : 0,
                'created_by' => $by, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    /** 4 bảng hàng kèm theo — xoá + ghi như ERP. Công thức: `unit_id` = ĐVT cơ bản của hàng thành phần */
    private function writeKits(Product $product, array $d): void
    {
        $baseUnits = DB::table('product_units')->where('is_base', 1)->whereIn('product_id', collect($d['recipes'] ?? [])->pluck('product_id'))
            ->pluck('unit_id', 'product_id');
        $tables = [
            'recipe_products' => collect($d['recipes'] ?? [])->map(function ($r) use ($baseUnits) {
                return ['product_id' => $r['product_id'], 'unit_id' => $baseUnits[$r['product_id']] ?? null, 'qty' => $r['qty'], 'is_main' => !empty($r['is_main']) ? 1 : 0];
            }),
            'product_has_accessories' => collect($d['accessories'] ?? [])->map(function ($r) {
                return ['product_id' => $r['product_id'], 'unit_id' => $r['unit_id'], 'qty' => $r['qty']];
            }),
            'product_has_install_accessories' => collect($d['install_accessories'] ?? [])->map(function ($r) {
                return ['product_id' => $r['product_id'], 'unit_id' => $r['unit_id'], 'qty' => $r['qty']];
            }),
            'product_has_repair_accessories' => collect($d['repair_accessories'] ?? [])->map(function ($r) {
                return ['product_id' => $r['product_id']];
            }),
        ];
        foreach ($tables as $table => $rows) {
            DB::table($table)->where('base_product_id', $product->id)->delete();
            foreach ($rows as $row) {
                DB::table($table)->insert($row + ['base_product_id' => $product->id, 'created_at' => now(), 'updated_at' => now()]);
            }
        }
    }

    /**
     * C6: dòng Loại tài liệu + tệp. GIỮ id dòng cũ (tệp ở `files` gắn theo `table_id`) — ERP
     * `syncTechAttachments` cũng tạo lại với id cũ. Tệp tạm ⇒ chuyển sang thư mục chính.
     */
    private function writeTechAttachments(Product $product, array $rows): void
    {
        $keepIds = collect($rows)->pluck('id')->filter()->map('intval')->all();
        $drop = DB::table('product_tech_attachments')->where('product_id', $product->id)
            ->when($keepIds, function ($q) use ($keepIds) {
                $q->whereNotIn('id', $keepIds);
            })->pluck('id')->all();
        if ($drop) {
            DB::table('files')->where('table', 'product_tech_attachments')->whereIn('table_id', $drop)->delete();
            DB::table('product_tech_attachments')->whereIn('id', $drop)->delete();
        }

        $s3 = app(CmcS3Helper::class);
        foreach ($rows as $i => $row) {
            $ptaId = !empty($row['id'])
                ? (int) $row['id']
                : DB::table('product_tech_attachments')->insertGetId([
                    'product_id' => $product->id, 'attachment_type_id' => $row['attachment_type_id'],
                    'created_at' => now(), 'updated_at' => now(),
                ]);
            DB::table('product_tech_attachments')->where('id', $ptaId)->update(['attachment_type_id' => $row['attachment_type_id']]);

            $files = [];
            foreach ((array) ($row['files'] ?? []) as $j => $file) {
                $path = $file['file_path'];
                if ($s3->isTemporaryUrl($path)) {
                    $path = $s3->promoteTemporary($path, 'products');
                    if ($path === false) {
                        throw ValidationException::withMessages(["tech_attachments.$i.files.$j.file_path" => 'Tệp tải lên đã quá hạn, vui lòng tải lại.']);
                    }
                }
                $files[] = ['file_path' => $path, 'name' => $file['name'] ?? basename($path), 'file_name' => basename($path)];
            }
            TableFileHelper::syncForTable('product_tech_attachments', $ptaId, $files);
        }
    }

    /** Ảnh: xoá hết + chèn như ERP; `position` theo thứ tự (ERP để NULL) */
    private function writeGalleries(Product $product, array $urls): void
    {
        DB::table('product_galleries')->where('product_id', $product->id)->delete();
        $by = (int) auth()->user()->id;
        foreach (array_values($urls) as $i => $url) {
            DB::table('product_galleries')->insert([
                'product_id' => $product->id, 'name' => '', 'status' => 1, 'url' => $url, 'position' => $i + 1,
                'created_by' => $by, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    private function writeVideos(Product $product, array $urls): void
    {
        DB::table('product_videos')->where('product_id', $product->id)->delete();
        $by = (int) auth()->user()->id;
        foreach (array_values(array_filter($urls)) as $i => $url) {
            DB::table('product_videos')->insert([
                'product_id' => $product->id, 'url' => $url, 'position' => $i + 1, 'status' => 1,
                'created_by' => $by, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    /** G11 + C8: Tính chất không phải phụ tùng ô tô ⇒ xoá sạch 3 loại xe + đời xe dù payload có gửi */
    private function writeVehicles(Product $product, array $d): void
    {
        $autoParts = (bool) DB::table('product_types as t')
            ->join('product_families as f', 'f.id', '=', 't.product_family_id')
            ->join('product_function_groups as g', 'g.id', '=', 'f.product_function_group_id')
            ->join('product_natures as n', 'n.id', '=', 'g.product_nature_id')
            ->where('t.id', $product->product_type_id)->value('n.is_auto_parts');

        $this->writeLinks($product, Productable::TYPE_VEHICLE_MANUFACT, $autoParts ? (array) ($d['vehicle_manufact_ids'] ?? []) : []);
        $this->writeLinks($product, Productable::TYPE_VEHICLE_BRAND, $autoParts ? (array) ($d['vehicle_brand_ids'] ?? []) : []);
        $this->writeLinks($product, Productable::TYPE_VEHICLE_MODEL, $autoParts ? (array) ($d['vehicle_model_ids'] ?? []) : []);

        DB::table('product_vehicle_model_has_life')->where('product_id', $product->id)->delete();
        if (!$autoParts) {
            return;
        }
        foreach ((array) ($d['vehicle_lives'] ?? []) as $row) {
            foreach ((array) ($row['life_ids'] ?? []) as $lifeId) {
                DB::table('product_vehicle_model_has_life')->insert([
                    'product_id' => $product->id, 'model_id' => $row['model_id'], 'life_id' => $lifeId,
                ]);
            }
        }
    }

    /** Xoá + chèn `productables` CHỈ của 1 loại — loại khác không đổi số dòng */
    private function writeLinks(Product $product, string $type, array $ids): void
    {
        DB::table('productables')->where('product_id', $product->id)->where('productable_type', $type)->delete();
        foreach (array_unique(array_map('intval', $ids)) as $id) {
            DB::table('productables')->insert([
                'product_id' => $product->id, 'productable_id' => $id, 'productable_type' => $type,
                'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    /**
     * D1: so 4 ô quản trị gửi lên với giá trị form ĐANG HIỆN cho hàng cũ chưa có dòng — dùng CHUNG nguồn với
     * `ProductFormResource`: `AdminData::formValues($product, $companyId)` (thêm vào helper 2-B
     * `Modules/MasterData/Transformers/Product/AdminData.php`, code ở cuối khối này). So sánh chuẩn hoá (null ≡ '', số so theo float).
     */
    private function sameAsShown(Product $product, array $cols): bool
    {
        $shown = AdminData::formValues($product, $this->companyId());
        foreach (['business_policy_id', 'min_stock_qty', 'guarantee', 'guarantee_type'] as $k) {
            $a = $cols[$k] ?? null; $b = $shown[$k] ?? null;
            if (is_numeric($a) && is_numeric($b) ? (float) $a !== (float) $b : (string) $a !== (string) $b) {
                return false;
            }
        }
        return true;
    }

    /**
     * Tab Quản trị của CÔNG TY ĐANG LÀM VIỆC: dòng công ty (upsert, giữ coefficient) + NCC + catalog.
     * `$statusIfNew` = trạng thái khi dòng chưa có: tạo mới 1 (H1'), hàng cũ 3 (G4).
     */
    private function writeAdmin(Product $product, array $a, int $statusIfNew): void
    {
        $companyId = $this->companyId();
        $by = (int) auth()->user()->id;
        $cols = [
            'business_policy_id' => $a['business_policy_id'] ?? null,
            'min_stock_qty' => $a['min_stock_qty'] ?? null,
            'guarantee' => $a['guarantee'] ?? null,
            'guarantee_type' => $a['guarantee_type'] ?? null,
            'updated_by' => $by, 'updated_at' => now(),
        ];
        $row = DB::table('product_company_coefficients')->where('product_id', $product->id)->where('company_id', $companyId)->first();
        if ($row) {
            // Dòng hệ số cũ (status NULL) ⇒ đưa vào luồng ở trạng thái đang suy ra (3); giữ coefficient
            DB::table('product_company_coefficients')->where('id', $row->id)
                ->update($cols + ($row->status === null ? ['status' => ProductCompany::STATUS_TRADING] : []));
        } elseif ($statusIfNew === ProductCompany::STATUS_TRADING && $this->sameAsShown($product, $cols)) {
            // D1 (user 07/10): hàng CŨ chưa có dòng mà 4 ô quản trị KHÔNG đổi so với giá trị form đang hiện
            // ⇒ KHÔNG sinh dòng (sinh dòng coefficient 1 làm tròn nghìn giá popup ERP). NCC + catalog vẫn ghi bên dưới.
        } else {
            DB::table('product_company_coefficients')->insert($cols + [
                'product_id' => $product->id, 'company_id' => $companyId,
                'coefficient' => ProductCompany::NEUTRAL_COEFFICIENT, 'status' => $statusIfNew,
                'created_by' => $by, 'created_at' => now(),
            ]);
        }

        DB::table('product_suppliers')->where('product_id', $product->id)->where('company_id', $companyId)->delete();
        foreach (array_unique((array) ($a['supplier_ids'] ?? [])) as $supplierId) {
            DB::table('product_suppliers')->insert([
                'product_id' => $product->id, 'supplier_id' => $supplierId, 'company_id' => $companyId,
                'created_at' => now(), 'updated_at' => now(),
            ]);
        }

        DB::table('product_business_catalogs')->where('product_id', $product->id)->where('company_id', $companyId)->delete();
        foreach (array_unique((array) $a['job_cluster_ids']) as $clusterId) {
            DB::table('product_business_catalogs')->insert([
                'product_id' => $product->id, 'company_id' => $companyId, 'job_cluster_id' => $clusterId,
                'created_by' => $by, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }
}
```

Thêm vào `Modules/MasterData/Transformers/Product/AdminData.php` (nguồn DUY NHẤT cho 4 ô quản trị mà form hiện — `ProductFormResource` và `ProductWriteService::sameAsShown` cùng gọi, D1):

```php
    /** 4 ô quản trị form đang hiện cho công ty $companyId: dòng công ty nếu có, không thì cột chung của hàng (hàng cũ) */
    public static function formValues(Product $product, int $companyId): array
    {
        $row = DB::table('product_company_coefficients')
            ->where('product_id', $product->id)->where('company_id', $companyId)->first();

        return [
            'business_policy_id' => $row ? $row->business_policy_id : null,
            'min_stock_qty' => self::minStockQty($product, $companyId),
            'guarantee' => $row && $row->guarantee !== null ? (int) $row->guarantee
                : ($product->guarantee !== null ? (int) $product->guarantee : null),
            'guarantee_type' => $row && $row->guarantee_type ? $row->guarantee_type : $product->guarantee_type,
        ];
    }
```

> Trước khi chạy: đối chiếu cột thật (`created_at/updated_at/created_by/updated_by`) của từng bảng con với mục 3 khảo sát BE (`product_suppliers`, 4 bảng kèm theo, `product_tech_attachments`, `product_business_catalogs`, `product_company_coefficients` có `created_by`? `id`?) — bỏ cột không tồn tại khỏi mảng insert. `ProductBusinessCatalog`/`ProductCompany` đang dùng ở 2-C3: đọc cách 2-C3 insert để chép đúng cột. `isTemporaryUrl` có trên `CmcS3Helper` (MeetingService dùng) — kiểm chữ ký.

- [ ] **Step 4: Controller + route**

```php
<?php

namespace Modules\MasterData\Http\Controllers\V1\Product;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Response;
use Modules\MasterData\Http\Requests\Product\ProductRequest;
use Modules\MasterData\Services\Product\ProductWriteService;

/** Tạo / sửa hàng hoá do công ty tạo (đợt 2-C1). Gate 1652 ở route; quyền chủ hàng ở Service. */
class ProductWriteController extends ApiController
{
    /** @var ProductWriteService */
    protected $service;

    public function __construct(ProductWriteService $service)
    {
        parent::__construct();
        $this->service = $service;
    }

    public function store(ProductRequest $request)
    {
        $product = $this->service->store($request->validated());

        return $this->responseJson('success', Response::HTTP_OK, ['id' => $product->id, 'code' => $product->code]);
    }
}
```
Route (cuối khối products, TRƯỚC `/{product}`):
```php
        // Tạo / sửa hàng hoá do công ty tạo (đợt 2-C1)
        $write = 'V1\Product\ProductWriteController';
        Route::post('/', $write . '@store')->middleware('checkPermission:' . $build);
```

- [ ] **Step 5: PASS** — `… phpunit Modules/MasterData/Tests/Feature/ProductWriteApiTest.php` → OK (7). Ca đỏ thì đọc lỗi SQL (cột thiếu/thừa) và sửa mảng insert — KHÔNG nới assert.

- [ ] **Step 6: Commit**

```bash
git add Modules/MasterData/Services/Product/ProductWriteService.php Modules/MasterData/Http/Controllers/V1/Product/ProductWriteController.php Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductWriteApiTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: tạo hàng hoá (mã, ĐVT + 6 dòng giá 0, dòng công ty, bảng con)"
```

---

### Task 8: Sửa (công ty tạo) — `GET /{product}/edit` + `PUT /{product}`

**Files:**
- Modify: `Modules/MasterData/Services/Product/ProductWriteService.php` (thêm `update`, `assertOwner`)
- Create: `Modules/MasterData/Transformers/Product/ProductFormResource.php`
- Modify: `Modules/MasterData/Http/Controllers/V1/Product/ProductWriteController.php` (`edit`, `update`)
- Modify: `Modules/MasterData/Routes/api.php`
- Test: `Modules/MasterData/Tests/Feature/ProductWriteApiTest.php` (thêm ca)

**Interfaces:**
- Produces: `ProductWriteService::update(Product $product, array $data): Product`; `ProductWriteService::assertOwner(Product $product): void` (abort 403); `GET master-data/products/{product}/edit` → `data` đúng khuôn payload Task 6 (kèm `id`, `code`, `company_status`, `owner_company_name`, `units[].id`, `tech_attachments[].files[].id`, `vehicle_lives`, `admin.*`) + `option_ids` (để FE gọi `form-options?include_ids`); `PUT master-data/products/{product}` → `{data:{id, code}}`.

- [ ] **Step 1: Test fail — đường SỬA**

Thêm vào `ProductWriteApiTest`:
```php
    private function createAs(int $company, array $override = []): int
    {
        $this->actAs($company, [self::PERM]);
        return (int) $this->postJson(self::URL, $this->payload($override))->assertOk()->json('data.id');
    }

    /** @test */
    public function sua_giu_ma_trang_thai_cong_ty()
    {
        $id = $this->createAs(self::COMPANY);
        $form = $this->getJson(self::URL . "/$id/edit")->assertOk()->json('data');
        $code = DB::table('products')->where('id', $id)->value('code');

        $form['name'] = $form['name'] . ' sửa';
        $form['manufacture_id'] = (int) DB::table('manufactures')->where('status', 1)->where('id', '<>', $form['manufacture_id'])->value('id');
        $this->putJson(self::URL . "/$id", $form)->assertOk();

        $p = DB::table('products')->find($id);
        $this->assertSame($code, $p->code, 'mã sinh 1 lần');
        $this->assertSame(1, (int) $p->status);
        $this->assertSame(self::COMPANY, (int) $p->company_id);
        $this->assertSame(ProductCompany::STATUS_ENTERING_INFO,
            (int) DB::table('product_company_coefficients')->where('product_id', $id)->value('status'), "H1': không đổi trạng thái");
    }

    /** @test */
    public function sua_khong_dung_dvt_cu_chi_them_dvt_moi_kem_6_dong_gia()
    {
        $id = $this->createAs(self::COMPANY);
        $oldUnit = DB::table('product_units')->where('product_id', $id)->first();
        DB::table('product_unit_prices')->where('product_unit_id', $oldUnit->id)->update(['price' => 123000]); // giá ERP đã khai
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $newUnitId = (int) DB::table('units')->where('status', 1)->where('id', '<>', $oldUnit->unit_id)->value('id');
        $form['units'][] = ['unit_id' => $newUnitId, 'is_base' => false, 'unit_coefficient' => 12];

        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $this->assertSame(123000.0 * 6, (float) DB::table('product_unit_prices')->where('product_unit_id', $oldUnit->id)->sum('price'));
        $new = DB::table('product_units')->where('product_id', $id)->where('unit_id', $newUnitId)->first();
        $this->assertSame(6, DB::table('product_unit_prices')->where('product_unit_id', $new->id)->count());

        // Đổi hệ số dòng đã lưu ⇒ 422 (C7); bỏ dòng đã lưu khỏi payload ⇒ dòng vẫn còn
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $form['units'][0]['unit_coefficient'] = 99;
        $this->putJson(self::URL . "/$id", $form)->assertStatus(422)->assertJsonValidationErrors(['units.0.unit_id']);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $form['units'] = [];
        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $this->assertSame(2, DB::table('product_units')->where('product_id', $id)->count());
    }

    /** @test */
    public function cong_ty_khac_sua_bi_403_ca_edit_lan_put()
    {
        $id = $this->createAs(self::COMPANY);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $this->actAs(self::OTHER, [self::PERM]);
        $this->getJson(self::URL . "/$id/edit")->assertStatus(403);
        $this->putJson(self::URL . "/$id", $form)->assertStatus(403);
    }

    /** @test */
    public function khong_quyen_1652_sua_bi_403()
    {
        $id = $this->createAs(self::COMPANY);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $this->actAs(self::COMPANY, []);
        $this->putJson(self::URL . "/$id", $form)->assertStatus(403);
    }

    /** @test */
    public function luu_xe_va_may_khong_dung_loai_khac()
    {
        $fx = $this->productTypeFixture(true);
        $id = $this->createAs(self::COMPANY, ['product_type_id' => $fx['type']]);
        $other = DB::table('productables')->insertGetId([ // dòng loại lạ (không thuộc 5 loại form ghi)
            'product_id' => $id, 'productable_id' => 1, 'productable_type' => 'App\Model\Khac\Gi', 'created_at' => now(), 'updated_at' => now(),
        ]);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $form['vehicle_manufact_ids'] = DB::table('vehicle_manufacts')->limit(2)->pluck('id')->map('intval')->all();
        $form['machine_group_ids'] = [(int) DB::table('groups')->value('id')];
        $form['machine_ids'] = [(int) DB::table('products')->where('status', 1)->where('id', '<>', $id)->value('id')];
        $this->putJson(self::URL . "/$id", $form)->assertOk();

        $this->assertSame(2, DB::table('productables')->where('product_id', $id)->where('productable_type', Productable::TYPE_VEHICLE_MANUFACT)->count());
        $this->assertTrue(DB::table('productables')->where('id', $other)->exists(), 'loại khác không bị xoá');
    }

    /** @test */
    public function doi_sang_tinh_chat_khong_phu_tung_thi_xoa_du_lieu_xe()
    {
        $auto = $this->productTypeFixture(true);
        $plain = $this->productTypeFixture(false);
        $id = $this->createAs(self::COMPANY, [
            'product_type_id' => $auto['type'],
            'vehicle_manufact_ids' => [(int) DB::table('vehicle_manufacts')->value('id')],
        ]);
        $this->assertSame(1, DB::table('productables')->where('product_id', $id)->whereIn('productable_type', Productable::VEHICLE_TYPES)->count());

        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $form['product_type_id'] = $plain['type']; // payload vẫn mang vehicle_* cũ
        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $this->assertSame(0, DB::table('productables')->where('product_id', $id)->whereIn('productable_type', Productable::VEHICLE_TYPES)->count(), 'C8');
    }

    /** @test */
    public function tai_lieu_ky_thuat_giu_id_dong_cu()
    {
        $type = (int) DB::table('attachment_types')->value('id');
        $id = $this->createAs(self::COMPANY, ['tech_attachments' => [[
            'attachment_type_id' => $type, 'files' => [['file_path' => 'https://s3/tanphat_hrm/products/a.pdf', 'name' => 'a.pdf']],
        ]]]);
        $ptaId = (int) DB::table('product_tech_attachments')->where('product_id', $id)->value('id');
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $this->assertSame($ptaId, $form['tech_attachments'][0]['id']);
        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $this->assertSame([$ptaId], DB::table('product_tech_attachments')->where('product_id', $id)->pluck('id')->map('intval')->all());
        $this->assertSame(1, DB::table('files')->where('table', 'product_tech_attachments')->where('table_id', $ptaId)->count());
    }

    /** @test */
    public function sua_hang_cu_chi_bo_sung_loai_va_catalog_thi_luu_duoc()
    {
        // Hàng ERP cũ của công ty 1: chưa Loại SP, tech_coefficient = 0, chưa có dòng công ty (G4)
        $id = (int) DB::table('products as p')->where('p.status', 1)->where('p.company_id', self::OTHER)
            ->where('p.tech_coefficient', 0)->whereNull('p.product_type_id')
            ->whereNotExists(function ($q) {
                $q->from('product_company_coefficients as c')->whereColumn('c.product_id', 'p.id');
            })
            ->whereExists(function ($q) {
                $q->from('product_units as u')->whereColumn('u.product_id', 'p.id')->where('u.is_base', 1);
            })->value('p.id');
        $this->actAs(self::OTHER, [self::PERM]);
        $form = $this->getJson(self::URL . "/$id/edit")->assertOk()->json('data');
        $form['product_type_id'] = $this->productTypeFixture(false)['type'];
        $form['admin']['job_cluster_ids'] = [$this->catalogBranch()['cluster']];
        $form['vat_percent_tax_rate_id'] = $form['vat_percent_tax_rate_id'] ?: (int) DB::table('tax_rates')->where('status', 1)->value('id');

        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $q = DB::table('product_company_coefficients')->where('product_id', $id)->where('company_id', self::OTHER);
        $this->assertSame(0, $q->count(), 'D1: 4 ô quản trị không đổi ⇒ KHÔNG sinh dòng công ty');
        $this->assertSame(1, DB::table('product_business_catalogs')->where('product_id', $id)->where('company_id', self::OTHER)->count(), 'catalog vẫn ghi');
        $this->assertSame(0.0, (float) DB::table('products')->where('id', $id)->value('tech_coefficient'), 'C3: giữ 0');

        // Đổi 1 ô quản trị ⇒ G4 sinh dòng coefficient 1, status 3
        $form = $this->getJson(self::URL . "/$id/edit")->assertOk()->json('data');
        $form['admin']['min_stock_qty'] = (float) ($form['admin']['min_stock_qty'] ?? 0) + 5;
        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $row = $q->first();
        $this->assertSame(ProductCompany::STATUS_TRADING, (int) $row->status, 'G4');
        $this->assertSame(1.0, (float) $row->coefficient);
    }

    /** @test */
    public function dong_he_so_cu_cua_chu_duoc_upsert_giu_coefficient()
    {
        $id = $this->createAs(self::COMPANY);
        DB::table('product_company_coefficients')->where('product_id', $id)->update(['status' => null, 'coefficient' => 1.15]);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $this->putJson(self::URL . "/$id", $form)->assertOk();
        $row = DB::table('product_company_coefficients')->where('product_id', $id)->first();
        $this->assertSame(1.15, round((float) $row->coefficient, 2));
        $this->assertSame(ProductCompany::STATUS_TRADING, (int) $row->status);
    }

    /** @test */
    public function thieu_catalog_khi_sua_bi_422()
    {
        $id = $this->createAs(self::COMPANY);
        $form = $this->getJson(self::URL . "/$id/edit")->json('data');
        $form['admin']['job_cluster_ids'] = [];
        $this->putJson(self::URL . "/$id", $form)->assertStatus(422)->assertJsonValidationErrors(['admin.job_cluster_ids']);
    }
```

> Ca `sua_hang_cu_…`: nếu DB dev không có hàng thoả cả 3 điều kiện thì nới `tech_coefficient = 0` thành điều kiện riêng và ghi rõ trong docblock ca đã đo bao nhiêu hàng — KHÔNG bỏ ca.

- [ ] **Step 2: FAIL** — 404 `/edit`, `PUT`.

- [ ] **Step 3: Service `update` + `assertOwner`**

Thêm vào `ProductWriteService`:
```php
    /** Chủ hàng = công ty tạo; hàng ERP đã xoá (status 0) không sửa (D2); Ngừng KD (4) không sửa (G9a) */
    public function assertOwner(Product $product): void
    {
        if ((int) $product->company_id !== $this->companyId()) {
            abort(403, 'Chỉ công ty tạo hàng hoá mới được sửa hàng hoá này.');
        }
        if ((int) $product->status !== Product::STATUS_ACTIVE) {
            abort(403, 'Hàng hoá đã bị xoá ở ERP, không sửa được.');
        }
        $status = DB::table('product_company_coefficients')->where('product_id', $product->id)
            ->where('company_id', $this->companyId())->value('status');
        if ((int) $status === ProductCompany::STATUS_STOPPED) {
            abort(403, 'Hàng hoá đang ngừng kinh doanh, mở khoá trước khi sửa.');
        }
    }

    public function update(Product $product, array $data): Product
    {
        $this->assertOwner($product);

        return DB::transaction(function () use ($product, $data) {
            $this->fillCommon($product, $data);   // KHÔNG đụng code / status / company_id (khác ERP)
            $product->save();
            $this->writeChildren($product, $data, false);
            $this->writeAdmin($product, (array) $data['admin'], ProductCompany::STATUS_TRADING); // G4: hàng cũ chưa có dòng

            return $product;
        });
    }
```
> Lưu ý `fillCommon` có gán `tech_coefficient` chỉ khi payload có giá trị ⇒ hàng cũ = 0 giữ 0 (C3).

- [ ] **Step 4: `ProductFormResource`** — đọc lại đúng khuôn payload

```php
<?php

namespace Modules\MasterData\Transformers\Product;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\Productable;

/**
 * Dữ liệu NẠP FORM SỬA (đợt 2-C1) — đúng khoá payload `ProductRequest` để FE gửi lại nguyên khối.
 * Tách khỏi `ProductDetailResource` (màn chi tiết chỉ đọc, e2e 6/6) để không đổi màn đó.
 * KHÔNG có giá (Q2). Tab Quản trị = của công ty đang làm việc; chưa có dòng ⇒ lùi về cột chung (AdminData).
 */
class ProductFormResource extends JsonResource
{
    public function toArray($request): array
    {
        $companyId = (int) auth()->user()->current_company_role;
        $p = $this->resource;
        $row = $p->companies->firstWhere('company_id', $companyId);
        $links = function (string $type) use ($p) {
            return DB::table('productables')->where('product_id', $p->id)->where('productable_type', $type)
                ->pluck('productable_id')->map('intval')->values()->all();
        };

        return [
            'id' => $p->id, 'code' => $p->code,
            'company_status' => $row && $row->status !== null ? (int) $row->status : null,
            'owner_company_name' => DB::table('companies')->where('id', $p->company_id)->value('name'),
            'name' => $p->name, 'english_name' => $p->english_name, 'common_name' => $p->common_name,
            'barcode' => $p->barcode, 'note' => $p->note,
            'model_id' => $p->model_id, 'barcode_id' => $p->barcode_id, 'brand_id' => $p->brand_id,
            'manufacture_id' => $p->manufacture_id, 'origin_id' => $p->origin_id,
            'product_type_id' => $p->product_type_id, 'product_characteristic_id' => $p->product_characteristic_id,
            'units' => $p->units->map(function ($u) {
                return ['id' => $u->id, 'unit_id' => $u->unit_id, 'is_base' => (bool) $u->is_base, 'unit_coefficient' => (float) $u->unit_coefficient];
            })->values(),
            'tech_attachments' => $p->techAttachments->map(function ($t) {
                return [
                    'id' => $t->id, 'attachment_type_id' => $t->attachment_type_id,
                    'files' => DB::table('files')->where('table', 'product_tech_attachments')->where('table_id', $t->id)
                        ->get(['id', 'file_path', 'name'])->map(function ($f) {
                            return ['id' => $f->id, 'file_path' => $f->file_path, 'name' => $f->name];
                        })->values(),
                ];
            })->values(),
            'galleries' => $p->galleries->sortBy('position')->pluck('url')->values()->all() ?: array_values(array_filter([$p->avatar])),
            'videos' => $p->videos->sortBy('position')->pluck('url')->values(),
            'weight' => $p->weight, 'size' => $p->size, 'norm' => $p->norm,
            'standard_accessories' => $p->standard_accessories, 'product_attributes' => $p->product_attributes,
            'special_feature' => $p->special_feature,
            'attributes' => $p->productAttributes->map(function ($a) {
                return ['attribute_id' => $a->attribute_id, 'name' => optional($a->attribute)->name, 'value' => $a->value,
                    'unittech_id' => $a->unittech_id, 'need_print' => (bool) $a->need_print];
            })->values(),
            'recipes' => $p->recipeProducts->map(function ($r) {
                return ['product_id' => $r->product_id, 'code' => optional($r->product)->code, 'name' => optional($r->product)->name,
                    'unit_name' => optional($r->unit)->name, 'qty' => (float) $r->qty, 'is_main' => (bool) $r->is_main];
            })->values(),
            'accessories' => $this->kits($p->accessories), 'install_accessories' => $this->kits($p->installAccessories),
            'repair_accessories' => $p->repairAccessories->map(function ($r) {
                return ['product_id' => $r->product_id, 'code' => optional($r->product)->code, 'name' => optional($r->product)->name];
            })->values(),
            'customs_name' => $p->customs_name, 'hs_code' => $p->hs_code, 'min_buy_qty' => $p->min_buy_qty,
            'vat_percent_tax_rate_id' => $p->vat_percent_tax_rate_id, 'import_tax_tax_rate_id' => $p->import_tax_tax_rate_id,
            'import_tax_has_co_tax_rate_id' => $p->import_tax_has_co_tax_rate_id, 'antidump_duty_tax_rate_id' => $p->antidump_duty_tax_rate_id,
            'environment_tax_coefficient' => $p->need_environment_tax ? (float) $p->environment_tax_coefficient : null,
            'vehicle_manufact_ids' => $links(Productable::TYPE_VEHICLE_MANUFACT),
            'vehicle_brand_ids' => $links(Productable::TYPE_VEHICLE_BRAND),
            'vehicle_model_ids' => $links(Productable::TYPE_VEHICLE_MODEL),
            'vehicle_lives' => $p->vehicleModelLives->groupBy('model_id')->map(function ($rows, $modelId) {
                return ['model_id' => (int) $modelId, 'life_ids' => $rows->pluck('life_id')->map('intval')->values()];
            })->values(),
            'machine_group_ids' => $links(Productable::TYPE_GROUP),
            'machines' => DB::table('products')->whereIn('id', $links(Productable::TYPE_PRODUCT))->get(['id', 'code', 'name']),
            'machine_ids' => $links(Productable::TYPE_PRODUCT),
            'tech_coefficient' => $p->tech_coefficient !== null ? (float) $p->tech_coefficient : null,
            'admin' => AdminData::formValues($p, $companyId) + [
                'supplier_ids' => $p->suppliers->where('company_id', $companyId)->pluck('supplier_id')->map('intval')->values(),
                'job_cluster_ids' => $p->businessCatalogs->where('company_id', $companyId)->pluck('job_cluster_id')->map('intval')->values(),
                'catalogs' => CatalogBranch::many($p->businessCatalogs->where('company_id', $companyId)),
            ],
        ];
    }

    private function kits($rows)
    {
        return $rows->map(function ($r) {
            return ['product_id' => $r->product_id, 'code' => optional($r->product)->code, 'name' => optional($r->product)->name,
                'unit_id' => $r->unit_id, 'unit_name' => optional($r->unit)->name, 'qty' => (float) $r->qty];
        })->values();
    }
}
```
> Đọc `AdminData::minStockQty` + `CatalogBranch::many` (đang có) để dùng đúng chữ ký; nếu `CatalogBranch::many` cần quan hệ lồng (`jobCluster.jobGroup.chapter.businessScope`) thì eager load đủ ở controller.

- [ ] **Step 5: Controller + route**

```php
    public function edit($product)
    {
        $model = Product::with([
            'units', 'techAttachments', 'galleries', 'videos', 'productAttributes.attribute',
            'recipeProducts.product:id,code,name', 'recipeProducts.unit:id,name',
            'accessories.product:id,code,name', 'accessories.unit:id,name',
            'installAccessories.product:id,code,name', 'installAccessories.unit:id,name',
            'repairAccessories.product:id,code,name', 'vehicleModelLives', 'companies', 'suppliers',
            'businessCatalogs.jobCluster.jobGroup.chapter.businessScope',
        ])->findOrFail((int) $product);
        $this->service->assertOwner($model);

        return $this->responseJson('success', Response::HTTP_OK, new ProductFormResource($model));
    }

    public function update(ProductRequest $request, $product)
    {
        $model = $this->service->update(Product::findOrFail((int) $product), $request->validated());

        return $this->responseJson('success', Response::HTTP_OK, ['id' => $model->id, 'code' => $model->code]);
    }
```
(thêm `use Modules\MasterData\Entities\Product\Product;` + `use Modules\MasterData\Transformers\Product\ProductFormResource;`)

Route:
```php
        Route::get('/{product}/edit', $write . '@edit')->where('product', '[0-9]+')->middleware('checkPermission:' . $build);
        Route::put('/{product}', $write . '@update')->where('product', '[0-9]+')->middleware('checkPermission:' . $build);
```
> `ProductRequest` chạy TRƯỚC `assertOwner` (FormRequest resolve trước thân controller) ⇒ công ty khác gửi payload sai nhận 422 thay vì 403. Ca test `cong_ty_khac_sua_bi_403…` gửi payload hợp lệ nên vẫn 403; nếu muốn 403 trước validate, gọi `assertOwner` trong `ProductRequest::authorize()` (`return` false ⇒ 403) — chọn cách này nếu ca đỏ.

- [ ] **Step 6: PASS** — `ProductWriteApiTest` OK (16). Hồi quy `ProductReadApiTest`, `ProductCompanyFoundationTest`, `ProductCatalogApiTest`.

- [ ] **Step 7: Commit**

```bash
git add Modules/MasterData/Services/Product/ProductWriteService.php Modules/MasterData/Transformers/Product/ProductFormResource.php Modules/MasterData/Http/Controllers/V1/Product/ProductWriteController.php Modules/MasterData/Routes/api.php Modules/MasterData/Tests/Feature/ProductWriteApiTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: sửa hàng hoá do công ty tạo (khoá ĐVT cũ, G4, C8, giữ id tài liệu)"
```

---

### Task 9: Cờ `can_edit` ở danh sách + chi tiết (G9a, C12)

**Files:**
- Modify: `Modules/MasterData/Transformers/Product/ProductListResource.php`
- Modify: `Modules/MasterData/Transformers/Product/ProductDetailResource.php`
- Test: `Modules/MasterData/Tests/Feature/ProductWriteApiTest.php`

**Interfaces:**
- Produces: `can_edit: bool` ở mỗi dòng `GET /entering|/company|/warehouse|/trading` và ở `GET /{product}` = có quyền 1652 ∧ `products.company_id = company_role` ∧ `products.status = 1` ∧ `company_status ≠ 4`.

- [ ] **Step 1: Test fail**

```php
    /** @test */
    public function can_edit_theo_quyen_va_cong_ty_tao()
    {
        $id = $this->createAs(self::COMPANY);
        $this->getJson(self::URL . "/$id")->assertOk()->assertJsonPath('data.can_edit', true);
        $rows = collect($this->getJson(self::URL . '/entering?per_page=100')->json('data'));
        $this->assertTrue($rows->firstWhere('id', $id)['can_edit']);

        $this->actAs(self::COMPANY, ['Xem dữ liệu hàng hoá công ty']); // không 1652
        $this->getJson(self::URL . "/$id")->assertJsonPath('data.can_edit', false);

        $this->actAs(self::OTHER, [self::PERM]); // công ty khác
        $this->getJson(self::URL . "/$id")->assertJsonPath('data.can_edit', false);
    }
```

- [ ] **Step 2: FAIL.**

- [ ] **Step 3: Code** — thêm vào cả 2 resource (`$companyId`, `$status` đã có sẵn trong `toArray`):

```php
            // G9a: Sửa (đợt 2-C1) — công ty tạo + quyền 1652 + chưa bị ERP xoá + không Ngừng KD
            'can_edit' => (int) $this->company_id === $companyId
                && (int) $this->status === \Modules\MasterData\Entities\Product\Product::STATUS_ACTIVE
                && $status !== \Modules\MasterData\Entities\Product\ProductCompany::STATUS_STOPPED
                && \App\Models\BaseModel::isCurrentEmployeeHasPermission('Xây dựng thông tin hàng hoá'),
```
> `isCurrentEmployeeHasPermission` đệm theo request (`RequestCache`) nên 100 dòng chỉ 1 lần đọc quyền. Kiểm `products.status` có trong select của danh sách (`select('products.*')`) — có. Đọc memory *quyen-chi-doc-qua-role*: hàm này bỏ qua `employee_has_permissions` ⇒ trait `actAs` (ghi `employee_has_permissions`) có thể làm ca "có quyền" ra false. Nếu vậy: dùng cùng nguồn với middleware (`Employee::getAllPermissions()` qua `RequestCache 'perm_all_by_emp:'`) — viết helper private trong resource gọi đúng logic `CheckPermission` — KHÔNG sửa trait.

- [ ] **Step 4: PASS** — `ProductWriteApiTest` OK (17); hồi quy `ProductReadApiTest` (8).

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Transformers/Product/ProductListResource.php Modules/MasterData/Transformers/Product/ProductDetailResource.php Modules/MasterData/Tests/Feature/ProductWriteApiTest.php
git commit -m "[gop_db] Hàng hoá 2-C1: cờ can_edit ở danh sách + chi tiết"
```

**🏁 Kết thúc Pha 2:** chạy toàn bộ test `Modules/MasterData/Tests/Feature/Product*Test.php` + `BusinessCatalogTreeTest` → xanh; smoke tay bằng curl (token e2e_assign, API worktree cổng 8031): tạo 1 hàng → kiểm 6 dòng giá + dòng công ty bằng tinker → XOÁ hàng thử bằng tinker (ghi lại id). Báo user, xin "làm" Pha 3.

---

# PHA 3 — FE

> Mọi task FE: chạy Nuxt worktree cổng **3031** (API 8031), kiểm bằng **Playwright MCP** + đo DOM (số phần tử, `getComputedStyle`, toạ độ) TRƯỚC khi báo xong task. Fixture UI: tạo tạm 1 Loại SP thuộc Tính chất có tick + 1 không tick bằng API danh mục (hoặc tinker) với tiền tố `E2EC1`, dọn khi xong.

### Task 10: Ô tick "Phụ tùng ô tô" ở màn Tính chất hàng hoá (G11, FE)

**Files:**
- Modify: `hrm-client/pages/master-data/product-natures/AddProductNatureModal.vue` (hàng 2 :51-66; `emptyData` :139; nạp :198; payload :257)
- Modify: `hrm-client/pages/master-data/product-natures/index.vue` (cột danh sách :341-433)

**Interfaces:** Consumes `is_auto_parts` (Task 1).

- [ ] **Step 1: Modal** — hàng 2 thành Mẫu in barcode col-6 + ô tick col-6 (đủ 12 cột):

```vue
            <div class="col-md-6 mb-2 d-flex align-items-end">
                <V2BaseCheckbox v-model="data.is_auto_parts" :disabled="isShow">
                    Phụ tùng ô tô
                </V2BaseCheckbox>
                <ProductInfoTip class="ml-1" text="Tick: form hàng hoá thuộc tính chất này hiện tab Phân loại xe." />
            </div>
```
`emptyData()` thêm `is_auto_parts: false`; khi nạp `is_auto_parts: !!data.is_auto_parts`; payload thêm `is_auto_parts: this.data.is_auto_parts ? 1 : 0`. Icon ⓘ: theo skill `info-icon-tooltip` (đọc SKILL.md; nếu `V2BaseLabel :hint` là chuẩn thì dùng nó thay `ProductInfoTip`).

- [ ] **Step 2: Danh sách** — thêm cột `is_auto_parts` (nhãn "Phụ tùng ô tô", ô hiện "Có"/trống) theo khuôn cột của màn (slot `#cell-is_auto_parts`), không thêm ô lọc (B4).

- [ ] **Step 3: Playwright MCP** — mở `http://127.0.0.1:3031/master-data/product-natures`, Thêm mới tick ô → Lưu → mở lại: đo `input[type=checkbox]:checked` = 1 trong modal; đo 2 cột của hàng 2 có `offsetTop` bằng nhau (cùng hàng). Dọn bản ghi thử.

- [ ] **Step 4: Commit**

```bash
git add pages/master-data/product-natures/AddProductNatureModal.vue pages/master-data/product-natures/index.vue
git commit -m "[gop_db] Hàng hoá 2-C1: ô Phụ tùng ô tô ở danh mục Tính chất hàng hoá (G11)"
```

---

### Task 11: Khung form — chấm đỏ tab + page tạo/sửa + `ProductForm`

**Files:**
- Modify: `hrm-client/components/product/detail/ProductStepTabs.vue`, `ProductParentTabs.vue` (prop `errorKeys`)
- Create: `hrm-client/components/product/form/ProductForm.vue`
- Create: `hrm-client/components/product/form/productFormModel.js`
- Create: `hrm-client/pages/master-data/products/create.vue`
- Create: `hrm-client/pages/master-data/products/_id/edit.vue`

**Interfaces:**
- Consumes: `GET form-options?include_ids[...]`, `GET {id}/edit`, `POST /`, `PUT /{id}` (Task 3, 7, 8).
- Produces:
  - `productFormModel.js`: `emptyForm(): Object` (đúng khoá payload Task 6), `TAB_OF_FIELD(key): 'general'|'specs'|'purchase'|'vehicles'|'machines'|'admin'`, `toPayload(form): Object`, `includeIdsOf(form): Object`.
  - `ProductForm` props `{ mode: 'create'|'edit', productId: Number|null, backUrl: String }`; con nhận `form`, `options`, `fieldError` qua prop; event `saved({id, code})`.
  - `ProductStepTabs`/`ProductParentTabs` prop `errorKeys: Array<string>` (key tab có lỗi ⇒ chấm đỏ 7px như mockup `.o-loi`).

- [ ] **Step 1: Chấm đỏ tab** — `ProductStepTabs.vue`: props thêm `errorKeys: { type: Array, default: () => [] }`; trong `.fstep` thêm `<span v-if="errorKeys.includes(tab.key)" class="fstep__err" aria-label="Có lỗi"></span>`; CSS:
```scss
.fstep { position: relative; }
.fstep__err { position: absolute; top: -2px; right: -4px; width: 7px; height: 7px; border-radius: 50%; background: #dc2626; }
```
Tương tự `ProductParentTabs.vue` (đặt trên nhãn tab cha). Màn chi tiết không truyền prop ⇒ không đổi.

- [ ] **Step 2: `productFormModel.js`**

```js
/**
 * Khuôn dữ liệu form tạo/sửa hàng hoá (đợt 2-C1) — khoá TRÙNG payload BE `ProductRequest`.
 * Luật: .plans/gop-db/quan-ly-hang-hoa/2c-ghi/chot.md (G1–G11, C1–C12).
 */
export function emptyForm() {
    return {
        name: '', english_name: '', common_name: '', barcode: '', note: '',
        model_id: null, barcode_id: null, brand_id: null, manufacture_id: null, origin_id: null,
        product_type_id: null, product_characteristic_id: null,
        units: [{ id: null, unit_id: null, is_base: true, unit_coefficient: 1 }],
        tech_attachments: [], galleries: [], videos: [],
        weight: null, size: '', norm: null, standard_accessories: '', product_attributes: '', special_feature: '',
        attributes: [], recipes: [], accessories: [], install_accessories: [], repair_accessories: [],
        customs_name: '', hs_code: '', min_buy_qty: null,
        vat_percent_tax_rate_id: null, import_tax_tax_rate_id: null, import_tax_has_co_tax_rate_id: null,
        antidump_duty_tax_rate_id: null, environment_tax_coefficient: null,
        vehicle_manufact_ids: [], vehicle_brand_ids: [], vehicle_model_ids: [], vehicle_lives: [],
        machine_group_ids: [], machines: [], machine_ids: [],
        tech_coefficient: 1,
        admin: { business_policy_id: null, min_stock_qty: null, guarantee: null, guarantee_type: 'thang', supplier_ids: [], job_cluster_ids: [] },
    }
}

const PREFIX_TAB = [
    [/^(name|english_name|common_name|barcode|note|model_id|barcode_id|brand_id|manufacture_id|origin_id|product_type_id|product_characteristic_id|units|tech_attachments|galleries|videos)/, 'general'],
    [/^(weight|size|norm|standard_accessories|product_attributes|special_feature|attributes|recipes|accessories|install_accessories|repair_accessories)/, 'specs'],
    [/^(customs_name|hs_code|min_buy_qty|vat_percent_tax_rate_id|import_tax|antidump|environment_tax)/, 'purchase'],
    [/^vehicle_/, 'vehicles'],
    [/^machine_/, 'machines'],
    [/^(admin|tech_coefficient)/, 'admin'],
]

/** Lỗi 422 key `units.0.unit_id` → tab chứa ô đó */
export function tabOfField(key) {
    const hit = PREFIX_TAB.find(([re]) => re.test(key))
    return hit ? hit[1] : 'general'
}

/** Thuộc tính chỉ gửi dòng tick (C9: "Bắt buộc" = dùng); bỏ khoá hiển thị */
export function toPayload(form) {
    const { machines, ...rest } = form
    return {
        ...rest,
        attributes: form.attributes.filter((a) => a.checked).map(({ attribute_id, value, unittech_id, need_print }) => ({ attribute_id, value, unittech_id, need_print })),
        recipes: form.recipes.map(({ product_id, qty, is_main }) => ({ product_id, qty, is_main })),
        accessories: form.accessories.map(({ product_id, unit_id, qty }) => ({ product_id, unit_id, qty })),
        install_accessories: form.install_accessories.map(({ product_id, unit_id, qty }) => ({ product_id, unit_id, qty })),
        repair_accessories: form.repair_accessories.map(({ product_id }) => ({ product_id })),
        machine_ids: machines.map((m) => m.id),
        admin: { ...form.admin, job_cluster_ids: [...form.admin.job_cluster_ids] },
    }
}

/** Bản ghi đang chọn của danh mục lớn/khoá — để `form-options` trả kèm (🔒 vẫn hiện) */
export function includeIdsOf(form) {
    const one = (v) => (v ? [v] : [])
    return {
        product_types: one(form.product_type_id), product_characteristics: one(form.product_characteristic_id),
        brands: one(form.brand_id), manufacturers: one(form.manufacture_id), origins: one(form.origin_id),
        product_models: one(form.model_id), order_codes: one(form.barcode_id),
        units: form.units.map((u) => u.unit_id).filter(Boolean),
        tax_rates: [form.vat_percent_tax_rate_id, form.import_tax_tax_rate_id, form.import_tax_has_co_tax_rate_id, form.antidump_duty_tax_rate_id].filter(Boolean),
        business_policies: one(form.admin.business_policy_id), suppliers: form.admin.supplier_ids,
        machine_groups: form.machine_group_ids, attachment_types: form.tech_attachments.map((t) => t.attachment_type_id).filter(Boolean),
        attribute_units: form.attributes.map((a) => a.unittech_id).filter(Boolean),
    }
}
```

- [ ] **Step 3: `ProductForm.vue`** (khung; 6 tab con ở Task 12–15)

```vue
<template>
    <div class="product-form">
        <div class="product-tabs-card">
            <ProductParentTabs :tabs="parentTabs" :value="parentTab" :error-keys="parentErrorKeys" @change="parentTab = $event" />
            <template v-if="parentTab === 'info'">
                <ProductStepTabs :tabs="stepTabs" :value="stepTab" :error-keys="errorTabs" @change="stepTab = $event" />
                <ProductFormGeneral v-show="stepTab === 'general'" :form="form" :options="options" :field-error="fieldError" :mode="mode" @type-change="onTypeChange" />
                <ProductFormSpecs v-show="stepTab === 'specs'" :form="form" :options="options" :field-error="fieldError" :product-id="productId" />
                <ProductFormPurchase v-show="stepTab === 'purchase'" :form="form" :options="options" :field-error="fieldError" />
                <ProductFormVehicles v-if="showVehicles" v-show="stepTab === 'vehicles'" :form="form" :field-error="fieldError" :active="stepTab === 'vehicles'" />
                <ProductFormMachines v-show="stepTab === 'machines'" :form="form" :options="options" :field-error="fieldError" :product-id="productId" />
            </template>
            <ProductFormAdmin v-show="parentTab === 'admin'" :form="form" :options="options" :field-error="fieldError" />
        </div>
        <V2Footer :menu="{ submit_form: true }" :url-back="backUrl" @submitForm="save" />
    </div>
</template>

<script>
import formValidateMixin from '@/utils/mixins/formValidateMixin'
import unsavedChangesMixin from '@/utils/mixins/unsavedChangesMixin'
import V2Footer from '@/components/V2Footer.vue'
import ProductParentTabs from '@/components/product/detail/ProductParentTabs.vue'
import ProductStepTabs from '@/components/product/detail/ProductStepTabs.vue'
import ProductFormGeneral from './ProductFormGeneral.vue'
import ProductFormSpecs from './ProductFormSpecs.vue'
import ProductFormPurchase from './ProductFormPurchase.vue'
import ProductFormVehicles from './ProductFormVehicles.vue'
import ProductFormMachines from './ProductFormMachines.vue'
import ProductFormAdmin from './ProductFormAdmin.vue'
import { emptyForm, includeIdsOf, tabOfField, toPayload } from './productFormModel'

const API = 'master-data/products'
const STEP_ORDER = ['general', 'specs', 'purchase', 'vehicles', 'machines']

/**
 * Form tạo / sửa hàng hoá do công ty tạo (đợt 2-C1). 1 nút Lưu (G3), Lưu không đổi trạng thái (H1').
 * FE chỉ `required` ô Tên (skill form-validate); mọi bắt buộc khác BE trả 422 một lượt ⇒ chấm đỏ mọi
 * tab có lỗi, mở tab lỗi ĐẦU TIÊN rồi mới cuộn (pane `v-show` ẩn thì scrollToFirstError bỏ qua).
 */
export default {
    name: 'ProductForm',
    components: { V2Footer, ProductParentTabs, ProductStepTabs, ProductFormGeneral, ProductFormSpecs, ProductFormPurchase, ProductFormVehicles, ProductFormMachines, ProductFormAdmin },
    mixins: [formValidateMixin, unsavedChangesMixin],
    props: {
        mode: { type: String, default: 'create' },
        productId: { type: Number, default: null },
        backUrl: { type: String, required: true },
    },
    data() {
        return { form: emptyForm(), options: {}, parentTab: 'info', stepTab: 'general', saving: false }
    },
    computed: {
        selectedType() {
            return (this.options.product_types || []).find((t) => t.id === this.form.product_type_id) || null
        },
        showVehicles() {
            return !!(this.selectedType && this.selectedType.path && this.selectedType.path.nature_is_auto_parts) // G11
        },
        stepTabs() {
            const all = [
                { key: 'general', label: 'Thông tin chung' }, { key: 'specs', label: 'Thông số kỹ thuật' },
                { key: 'purchase', label: 'Mua hàng' }, { key: 'vehicles', label: 'Phân loại xe' }, { key: 'machines', label: 'Nhóm máy' },
            ]
            return all.filter((t) => t.key !== 'vehicles' || this.showVehicles)
        },
        parentTabs() {
            return [{ key: 'info', label: 'Thông tin hàng hoá' }, { key: 'admin', label: 'Quản trị hàng hoá' }]
        },
        errorTabs() {
            return [...new Set(Object.keys(this.formErrors).map(tabOfField))]
        },
        parentErrorKeys() {
            const keys = []
            if (this.errorTabs.some((t) => t !== 'admin')) keys.push('info')
            if (this.errorTabs.includes('admin')) keys.push('admin')
            return keys
        },
    },
    watch: {
        showVehicles(v) {
            if (!v && this.stepTab === 'vehicles') this.stepTab = 'general'
        },
    },
    async created() {
        if (this.mode === 'edit') {
            const res = await this.$store.dispatch('apiGetMethod', `${API}/${this.productId}/edit`)
            this.form = { ...emptyForm(), ...res.data, attributes: (res.data.attributes || []).map((a) => ({ ...a, checked: true })) }
            this.$emit('loaded', res.data)
        }
        await this.loadOptions()
        this.$nextTick(() => this.markFormPristine())
    },
    methods: {
        unsavedSnapshotSource() {
            return this.form
        },
        async loadOptions() {
            const params = new URLSearchParams()
            Object.entries(includeIdsOf(this.form)).forEach(([k, ids]) => ids.forEach((id) => params.append(`include_ids[${k}][]`, id)))
            const res = await this.$store.dispatch('apiGetMethod', `${API}/form-options?${params.toString()}`)
            this.options = res.data
        },
        onTypeChange(type) {
            // C10: điền % VAT theo Loại SP khi ô đang trống
            if (type && type.vat_percent_tax_rate_id && !this.form.vat_percent_tax_rate_id) {
                this.form.vat_percent_tax_rate_id = type.vat_percent_tax_rate_id
            }
        },
        openFirstErrorTab() {
            if (!this.errorTabs.length) return
            if (this.errorTabs.includes('admin') && this.errorTabs.length === 1) {
                this.parentTab = 'admin'
            } else {
                this.parentTab = 'info'
                this.stepTab = STEP_ORDER.find((k) => this.errorTabs.includes(k)) || 'general'
            }
        },
        async save() {
            if (this.saving) return
            const valid = await this.$validator.validateAll(null, { vmId: null })
            if (!valid) return this.toastFormError('Vui lòng kiểm tra lại dữ liệu nhập')
            this.saving = true
            this.clearServerErrors()
            try {
                const payload = toPayload(this.form)
                const res = this.mode === 'edit'
                    ? await this.$store.dispatch('apiPutMethod', { url: `${API}/${this.productId}`, payload })
                    : await this.$store.dispatch('apiPostMethod', { url: API, payload })
                this.markFormSaved()
                this.$toasted?.global?.success?.({ message: `Đã lưu hàng hoá ${res.data.code}` })
                this.$emit('saved', res.data)
            } catch (error) {
                if (this.applyServerErrors(error)) {
                    this.openFirstErrorTab()
                } else {
                    this.toastFormError(error?.response?.data?.message || 'Lưu không thành công')
                }
            } finally {
                this.saving = false
            }
        },
    },
}
</script>
```
> `form-options.product_types[].vat_percent_tax_rate_id` đã thêm ở Task 1 step 5 (C10). Đọc `V2Footer` (`menu.submit_form` → emit `submitForm`) để bind đúng tên event. CSS `.product-tabs-card*`: chép từ `pages/master-data/products/_id/index.vue:163-198`.

- [ ] **Step 4: 2 page** — `create.vue`:
```vue
<template>
    <div>
        <PageTitle title="Thêm mới hàng hoá" />
        <ProductForm ref="form" mode="create" :back-url="backUrl" @saved="onSaved" />
    </div>
</template>
<script>
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import unsavedChildFormMixin from '@/utils/mixins/unsavedChildFormMixin'
import ProductForm from '@/components/product/form/ProductForm.vue'

const LIST_PREFIX = '/master-data/products/'

/** Tạo hàng hoá (2-C1) — quyền 1652; Lưu xong sang chi tiết hàng vừa tạo (B3) */
export default {
    layout: 'default-sidebar',
    components: { ProductForm },
    mixins: [PageTitleMixin, unsavedChildFormMixin],
    middleware({ store, redirect }) {
        // Không quyền ⇒ trang 404 như chi tiết (BE vẫn chặn 403)
    },
    computed: {
        backUrl() {
            const from = String(this.$route.query.from || '')
            return from.startsWith(LIST_PREFIX) ? from : '/master-data/products/entering'
        },
    },
    methods: {
        onSaved({ id }) {
            this.$router.push(`/master-data/products/${id}?from=${encodeURIComponent(this.backUrl)}`)
        },
    },
}
</script>
```
> Xem `pages/master-data/products/_id/index.vue` để dùng ĐÚNG cách đặt tiêu đề (PageTitleMixin) + cách chặn quyền ở page đang dùng trong repo (`hasAPermission('Xây dựng thông tin hàng hoá')` ở `created` → `this.$router.replace('/pages/extras/404')`); bỏ khối `middleware` rỗng ở trên khi đã có cách thật. `_id/edit.vue` giống hệt, `mode="edit"`, `:product-id="Number($route.params.id)"`, tiêu đề `Sửa hàng hoá: <mã>` lấy từ event `loaded`, lỗi 403/404 khi nạp ⇒ `/pages/extras/404`.

> ⚠️ Kiểm Nuxt: `pages/master-data/products/create.vue` và `_id/` — truy cập `/master-data/products/create` phải ra `route.name` của trang create (memory *nuxt-dynamic-route*); đo `this.$route.name` bằng MCP.

- [ ] **Step 5: Playwright MCP** — mở `/master-data/products/create` (e2e_assign): đo 2 tab cha, 4 step (Loại SP chưa chọn ⇒ không có *Phân loại xe*), footer đúng 2 nút `Lưu`, `Quay lại`. Bấm Lưu form trống: đo `.v2-error` có chữ ≥ 8, chấm đỏ `.fstep__err` ở step 1 + 3, tab cha `admin` có chấm đỏ, step đang mở = `general`, chỉ 1 request POST. (Task 12–15 phải xong mới đo đủ — bước này chạy lại ở Task 16.)

- [ ] **Step 6: Commit**

```bash
git add components/product/detail/ProductStepTabs.vue components/product/detail/ProductParentTabs.vue components/product/form/ProductForm.vue components/product/form/productFormModel.js pages/master-data/products/create.vue pages/master-data/products/_id/edit.vue
git commit -m "[gop_db] Hàng hoá 2-C1: khung form tạo/sửa hàng hoá + chấm đỏ tab lỗi"
```

---

### Task 12: Tab Thông tin chung (ĐVT, Loại SP, tài liệu, ảnh, video, "+" Model)

**Files:**
- Create: `components/product/form/ProductFormGeneral.vue`
- Create: `components/product/form/ProductFormUnitsTable.vue`
- Create: `components/product/form/ProductFormTechDocs.vue`
- Create: `components/product/form/ProductFormGallery.vue`
- Modify: `pages/master-data/product-models/AddProductModelModal.vue` (emit `created` với bản ghi mới — thêm, không đổi event cũ)

**Interfaces:**
- Consumes: `form`, `options` (`product_types[].path`, `brands`, `manufacturers`, `origins`, `units[].can_be_base`, `product_characteristics`, `attachment_types`), `fieldError(key)`; `option-search?type=product_models|order_codes`; `POST master-data/products/upload-images` (Task 5); `files/upload?temporary=1` (field `attachments[]`).
- Produces: event `type-change(typeOption)`.

- [ ] **Step 1: `ProductFormGeneral.vue`** — 3 khối `V2BaseFormSection` (skill form-validate §1c), mỗi hàng đủ 12 cột:
  - *Thông tin hàng hoá*: Tên (col-6, `v-validate="'required|max:255'"`, `data-vv-name="name"`, `data-vv-as="Tên hàng hoá"`, `data-vv-value-path="currentValue"`) · Model (col-3, `V2BaseSelectRemote` `fetchFn` → `option-search?type=product_models&keyword=`, `initialOption` từ `options.product_models`; nút `+` `V2BaseIconButton` chỉ khi `hasAPermission('Quản lý danh mục model')`, mở `AddProductModelModal`, `@created` gán `form.model_id`) · Công ty quản lý (col-3, disabled: tạo = tên công ty đang làm việc, sửa = `owner_company_name`) · Tên thường gọi / Tên tiếng Anh / Barcode (col-4×3) · Ghi chú (col-12 textarea).
  - *Phân loại*: Loại sản phẩm (col-6 `V2BaseSelect` từ `options.product_types`, `keep-locked-options`) · Đặc tính (col-6) · Tính chất / Nhóm chức năng / Nhóm sản phẩm (col-4×3 disabled, đọc `selectedType.path`). Đổi Loại SP: `$emit('type-change', type)`; nếu tab xe đang có dữ liệu (`vehicle_*_ids` hoặc `vehicle_lives` khác rỗng) và loại mới `path.nature_is_auto_parts === false` ⇒ `this.$bvModal.msgBoxConfirm('Dữ liệu Phân loại xe sẽ bị xoá khi Lưu. Tiếp tục đổi Loại sản phẩm?', { title: 'Đổi Loại sản phẩm', okTitle: 'Đổi', cancelTitle: 'Giữ nguyên', okVariant: 'danger' })` — huỷ thì trả giá trị cũ (C8).
  - *Nguồn gốc*: Thương hiệu · Xuất xứ · Hãng SX · Code đặt hàng (col-3×4; 3 ô đầu `V2BaseLabel required` — BE quyết, FE không `required`).
  - `<ProductFormUnitsTable>` · `<ProductFormTechDocs>` · `<ProductFormGallery>` · Video: danh sách `V2BaseInput` + nút thêm/xoá dòng.
  Mọi ô: `:invalid="!!fieldError('brand_id')"` + `<V2BaseError :message="fieldError('brand_id')" />`; KHÔNG prop `trim`.

- [ ] **Step 2: `ProductFormUnitsTable.vue`** — khuôn `WrCostTable.vue` (`V2BaseTableScroll` + `table.v2-table.v2-form-table`). Cột: STT · Đơn vị (`V2BaseSelect`, mọi đơn vị — D4: không xét cờ `can_be_base`, như ERP) · Đơn vị cơ bản (`V2BaseRadio` 1 nhóm, option `{ value: index, label: '' }`) · Hệ số (`V2BaseInput type=number`, dòng cơ bản disabled = 1) · Quy đổi (chữ "Đơn vị cơ bản" / "1 {đơn vị} = {hệ số} {đơn vị cơ bản}") · xoá. **C7**: dòng có `id` ⇒ mọi ô disabled + không nút xoá + icon 🔒 ⓘ "Đơn vị tính đã lưu không sửa/xoá được". Lỗi dòng: `fieldError(\`units.${i}.unit_id\`)`, lỗi bảng `fieldError('units')`; thêm/xoá dòng thì `clearFieldError('units')` (form-validate §3b).

- [ ] **Step 3: `ProductFormTechDocs.vue`** (C6) — bảng dòng: Loại tài liệu (`V2BaseSelect` từ `options.attachment_types`) · Tệp (`V2BaseAttachmentSection` `v-model="paths"` `upload-url="files/upload?temporary=1"` `upload-field="attachments[]"`, map ↔ `row.files` giữ `id` của tệp cũ theo `file_path`) · xoá dòng. Nút "Thêm tài liệu".

- [ ] **Step 4: `ProductFormGallery.vue`** (C5) — `V2BaseFile multiple accept="image/*"` KHÔNG autoUpload; chọn xong gửi `FormData files[]` tới `master-data/products/upload-images`, nối `res.data[].url` vào `form.galleries` (chặn tổng > 10 ở FE + BE); lưới thumbnail (khuôn `ProductTabGeneral.vue:140–151`) ảnh đầu có nhãn "Ảnh đại diện"; kéo thả đổi thứ tự KHÔNG làm (để sau) — nút "Đặt làm ảnh đại diện" đưa ảnh lên đầu mảng; nút xoá.

- [ ] **Step 5: `AddProductModelModal.vue`** — sau `apiPostMethod` (nhánh thêm mới), lấy `const res = await …` và `this.$emit('created', res && res.data)` TRƯỚC `$emit('event')` (đọc response thật của POST model để lấy `id`/`name`).

- [ ] **Step 6: Playwright MCP** — tạo hàng E2EC1 đủ tab 1: đo (a) chọn Loại SP ⇒ 3 input cha có giá trị đúng `path`; bỏ chọn ⇒ trống; (b) bảng ĐVT: 2 radio cơ bản không đồng thời checked; dòng cơ bản ô hệ số `disabled`; (c) upload 2 ảnh ⇒ 2 thumbnail, ảnh đầu có nhãn; (d) "+" Model: tạo model E2EC1 ⇒ ô Model hiện tên mới. Hàng mỗi khối: `offsetWidth` tổng các col trên 1 hàng = 100% (đủ 12 cột).

- [ ] **Step 7: Commit**

```bash
git add components/product/form/ProductFormGeneral.vue components/product/form/ProductFormUnitsTable.vue components/product/form/ProductFormTechDocs.vue components/product/form/ProductFormGallery.vue pages/master-data/product-models/AddProductModelModal.vue
git commit -m "[gop_db] Hàng hoá 2-C1: tab Thông tin chung (ĐVT khoá dòng đã lưu, tài liệu, ảnh, + Model)"
```

---

### Task 13: Tab Thông số kỹ thuật (thuộc tính, rich text, 4 bảng hàng kèm theo, popup chọn hàng)

**Files:**
- Create: `components/product/form/ProductFormSpecs.vue`
- Create: `components/product/form/ProductFormItemsTable.vue`
- Create: `components/product/form/ProductItemPickerModal.vue`

**Interfaces:**
- Consumes: `GET attributes-by-type?product_type_id=` (Task 3), `GET item-search?keyword=&exclude_id=` (Task 3), `options.attribute_units`.
- Produces: `ProductItemPickerModal` (khuôn `V2BaseModal` — skill modal-popup) method `open({ multiple: Boolean, excludeIds: number[] })`, event `pick(rows: [{id, code, name, base_unit_id, base_unit_name, units}])` — dùng lại ở Task 14 (Chọn máy).

- [ ] **Step 1: Bảng thuộc tính (C9)** — watch `form.product_type_id` ⇒ gọi `attributes-by-type`; dựng `rows = union(typeAttrs, form.attributes)` theo `attribute_id`: dòng đã có trong `form.attributes` giữ `value/unittech_id/need_print`, `checked = true`; dòng mới từ loại `checked = false`. Đổi loại: dòng cũ (đã tick) GIỮ, dòng chưa tick không thuộc loại mới bỏ. Cột: Thuộc tính · Giá trị (`V2BaseInput`, lỗi `attributes.${i}.value` — chỉ dòng tick, map index theo thứ tự `toPayload` lọc tick) · Đơn vị (`V2BaseSelect` `attribute_units`) · Dùng (`V2BaseCheckbox`, nhãn cột "Bắt buộc" như ERP + ⓘ "Chỉ dòng được tick mới lưu và phải nhập giá trị") · In tem (`V2BaseCheckbox`). ⚠️ `V2BaseCheckbox` bắn lại `change` khi đổi prop từ code (bẫy 2-C3) — chỉ nghe `@input` từ người dùng.
  > Lỗi BE trả theo index payload đã lọc ⇒ giữ mảng `payloadIndexOf[rowIndex]` để map `attributes.N.value` về đúng dòng hiển thị.
- [ ] **Step 2: Thông số cơ bản + 2 rich text** — Trọng lượng · Kích thước · Định mức công lắp đặt (col-4×3); *Phụ kiện tiêu chuẩn* (`standard_accessories`) + *Đặc điểm* (`product_attributes`) dùng `<ckeditor :editor="ClassicEditor">` như `pages/training/courses/components/CourseForm.vue:2237-2269` (col-6×2).
- [ ] **Step 3: `ProductFormItemsTable.vue`** — props `{ rows: Array, withQty: Boolean, withUnit: Boolean, withMain: Boolean, errorPrefix: String, fieldError: Function, excludeId: Number }`; cột Mã · Tên · ĐVT (withUnit: `V2BaseSelect` từ `row.units`, mặc định `base_unit_id`; recipe: chữ ĐVT cơ bản, không chọn) · Số lượng (withQty) · Thành phần chính (withMain) · xoá; nút header "Chọn hàng hoá" mở picker `multiple`, loại trùng + loại chính nó (`excludeId`). Dùng 4 lần trong `ProductFormSpecs`: Công thức lắp ráp (`recipes`, qty + main), Phụ kiện mua thêm (`accessories`, unit + qty), Vật tư lắp đặt (`install_accessories`, unit + qty), Vật tư sửa chữa – bảo dưỡng (`repair_accessories`).
- [ ] **Step 4: `ProductItemPickerModal.vue`** — ô tìm (debounce 300ms) → `item-search?keyword=&exclude_id=`; bảng `V2BaseDataTable` (slot `#cell-check`, `#cell-code`…) tick nhiều; nút "Chọn" emit `pick`. Footer theo `V2BaseModal`.
- [ ] **Step 5: Playwright MCP** — Loại SP fixture có 2 thuộc tính ⇒ bảng 2 dòng chưa tick; tick 1 không nhập giá trị ⇒ Lưu ⇒ đúng ô đó báo lỗi + chấm đỏ step 2; chọn 2 hàng vào Phụ kiện ⇒ 2 dòng, ô ĐVT có giá trị; picker không trả chính hàng đang sửa.
- [ ] **Step 6: Commit**

```bash
git add components/product/form/ProductFormSpecs.vue components/product/form/ProductFormItemsTable.vue components/product/form/ProductItemPickerModal.vue
git commit -m "[gop_db] Hàng hoá 2-C1: tab Thông số kỹ thuật (thuộc tính theo loại, hàng kèm theo, popup chọn hàng)"
```

---

### Task 14: Tab Mua hàng · Phân loại xe · Nhóm máy

**Files:**
- Create: `components/product/form/ProductFormPurchase.vue`
- Create: `components/product/form/ProductFormVehicles.vue`
- Create: `components/product/form/ProductFormMachines.vue`

**Interfaces:**
- Consumes: `options.tax_rates`, `GET vehicle-options` (lazy, có `vehicle_lives` — Task 3), `options.machine_groups`, `ProductItemPickerModal` (Task 13).

- [ ] **Step 1: Mua hàng** — Tên khai báo hải quan · HS Code (col-6×2) · SL tối thiểu nhập mua · % VAT (`V2BaseLabel required`) · Thuế NK không CO · Thuế NK có CO (col-3×4) · Thuế chống bán phá giá · Hệ số tính thuế BVMT (col-6×2; trống = không chịu thuế BVMT, ⓘ giải thích F7). Không có "% giảm giá thanh lý" (F8).
- [ ] **Step 2: Phân loại xe (G11)** — chỉ render khi `showVehicles`; prop `active` ⇒ lần đầu `true` mới gọi `vehicle-options` (CLAUDE.md: danh mục tab chưa mở thì gọi khi mở). 3 `V2BaseSelect` multiple (Hãng xe không `required`) lọc dây chuyền: đổi Hãng ⇒ bỏ Loại/Model không thuộc; checkbox "Áp dụng tất cả đời xe cho model"; bảng Model × Đời xe: mỗi model đang chọn 1 dòng, cột Đời xe `V2BaseSelect` multiple từ `vehicle_lives` + "Chọn tất cả"; ghi `form.vehicle_lives = [{model_id, life_ids}]`, bỏ model ⇒ bỏ dòng. ⚠️ bẫy `th rowspan` + sticky (SO-CHOT §6): không dùng rowspan ở `thead`.
- [ ] **Step 3: Nhóm máy** — luôn hiện; `V2BaseSelect` multiple `machine_group_ids` (col-12); khối Máy chỉ hiện khi ≥ 1 nhóm: bảng STT · Mã máy · Tên máy · xoá + nút "Chọn máy" (picker, `form.machines` lưu `{id, code, name}`); lỗi `fieldError('machine_ids')` dưới bảng. Bỏ hết nhóm ⇒ xoá `form.machines`.
- [ ] **Step 4: Playwright MCP** — Loại SP có tick ⇒ step *Phân loại xe* hiện (đếm `.fstep` = 5), không tick ⇒ 4; mở tab xe lần đầu mới có request `vehicle-options` (bắt network); chọn 1 model ⇒ bảng đời xe 1 dòng; chọn nhóm máy không chọn máy ⇒ Lưu ⇒ lỗi ở bảng Máy + chấm đỏ step 5.
- [ ] **Step 5: Commit**

```bash
git add components/product/form/ProductFormPurchase.vue components/product/form/ProductFormVehicles.vue components/product/form/ProductFormMachines.vue
git commit -m "[gop_db] Hàng hoá 2-C1: tab Mua hàng, Phân loại xe (G11), Nhóm máy"
```

---

### Task 15: Tab cha Quản trị hàng hoá (4 ô + NCC + Hệ số công nghệ + catalog)

**Files:**
- Create: `components/product/form/ProductFormAdmin.vue`
- Create: `components/product/form/ProductFormCatalogPicker.vue`

**Interfaces:**
- Consumes: `GET catalog-options` (có `parent_id`, `is_locked`), `option-search?type=suppliers`, `options.business_policies`, `form.admin.catalogs` (khi sửa, để hiện nhánh đã lưu kể cả nhánh nay bị khoá).

- [ ] **Step 1: 6 ô** (đủ 12 cột: hàng 1 Nhà cung cấp col-6 + Chính sách kinh doanh col-6; hàng 2 SL tồn kho tối thiểu · Bảo hành · Đơn vị bảo hành (Ngày/Tháng/Năm `V2BaseSelect`, value `ngay|thang|nam`) · Hệ số công nghệ — col-3×4). Nhà cung cấp chọn nhiều tìm server: kiểm `V2BaseSelect` có `extra-settings` ajax multiple; nếu không, dùng `V2BaseSelectRemote` + danh sách chip bên dưới (thêm từng NCC). Hệ số công nghệ ⓘ "Dùng chung mọi công ty, chỉ công ty tạo sửa" (T6).
- [ ] **Step 2: `ProductFormCatalogPicker.vue`** — 4 cột tick có ô tìm (Lĩnh vực · Chương · Mục · Tiểu mục) theo mockup §33; chọn Tiểu mục ⇒ thêm nhánh vào bảng (STT La Mã · 4 cấp · nút Gỡ); chỉ lưu `job_cluster_ids`; nhánh khoá bất kỳ cấp ⇒ 🔒 không tick thêm (B2); nhánh đã lưu nay khoá vẫn hiện trong bảng (gỡ được). Bỏ tick cấp trên ⇒ gỡ nhánh con + toast "Đã gỡ N nhánh". Lỗi `fieldError('admin.job_cluster_ids')`: chữ đỏ dưới khối + viền đỏ cột Tiểu mục. Xem `components/product/catalog/ProductCatalogTree.vue` trước — tái dùng phần lọc cây nếu hợp, KHÔNG sửa popup 2-C3.
- [ ] **Step 3: Playwright MCP** — Lưu thiếu catalog ⇒ tự chuyển tab cha *Quản trị*, `.fstep__err`/chấm đỏ trên tab cha `admin`, chữ "Phải xếp hàng hoá vào ít nhất 1 Tiểu mục…" hiện; chọn 1 Tiểu mục ⇒ bảng 1 dòng; 2 hàng ô đo `offsetTop` cùng hàng.
- [ ] **Step 4: Commit**

```bash
git add components/product/form/ProductFormAdmin.vue components/product/form/ProductFormCatalogPicker.vue
git commit -m "[gop_db] Hàng hoá 2-C1: tab Quản trị hàng hoá (NCC, bảo hành, hệ số công nghệ, catalog)"
```

---

### Task 16: Lối vào — Tạo mới · Sửa ở menu dòng · Sửa ở footer chi tiết (G9a, C12)

**Files:**
- Modify: `components/product/ProductListPage.vue` (`#actions` :113, thêm cột `actions` + `#cell-actions`, computed quyền)
- Modify: `utils/product-list-screens.js` (cờ màn có cột Hành động: `entering`, `company`)
- Modify: `pages/master-data/products/_id/index.vue` (footer :41)

**Interfaces:** Consumes `can_edit` (Task 9).

- [ ] **Step 1: Nút Tạo mới** — trong `#actions`, trước nút cấu hình cột:
```vue
                    <V2BaseButton v-if="canCreate" primary size="sm" class="mr-2 mb-2" @click="$router.push(`/master-data/products/create?from=${encodeURIComponent(screen.path)}`)">
                        <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
                        Tạo mới
                    </V2BaseButton>
```
computed `canCreate() { return this.screen.slug === 'entering' && this.hasAPermission('Xây dựng thông tin hàng hoá') }`. Theo skill button-convention + memory *smartfilterpanel-header-actions*: nếu slot nằm trong `SmartFilterPanel #header-actions` thì bỏ `mr-2 mb-2`, dùng `btn-compact`.
- [ ] **Step 2: Cột Hành động** — `product-list-screens.js`: thêm `rowActions: true` cho `entering`, `company`; `ProductListPage` thêm cột `{ key: 'actions', title: '', … }` cuối khi `screen.rowActions`, slot:
```vue
                <template v-if="screen.rowActions" #cell-actions="{ item }">
                    <V2BaseRowActions :actions="[{ key: 'edit', title: 'Sửa', icon: 'ri-edit-line', visible: !!item.can_edit }]" @action="onRowAction($event, item)" />
                </template>
```
`onRowAction(key, item)`: `key === 'edit'` ⇒ `/master-data/products/${item.id}/edit?from=${encodeURIComponent(this.screen.path)}`. Cột không có dòng nào sửa được vẫn giữ (nhất quán).
- [ ] **Step 3: Footer chi tiết** — `:menu="{ edit: !!product.can_edit }"` + `@edit="$router.push(\`/master-data/products/${productId}/edit?from=${encodeURIComponent(backUrl)}\`)"`.
- [ ] **Step 4: Playwright MCP (có quyền + KHÔNG quyền)** — e2e_assign: màn entering có nút Tạo mới, cột Hành động; hàng E2EC1 menu có "Sửa"; chi tiết footer có Sửa → mở `/edit`, Quay lại về đúng `?from`. Tài khoản nocost + role tạm chỉ 1653 (khuôn spec 2-C3 ca 7): màn company không có Sửa ở menu dòng, chi tiết không có nút Sửa; vào thẳng `/master-data/products/create` ⇒ 404. Đo bằng đếm phần tử, không chỉ ảnh.
- [ ] **Step 5: Commit**

```bash
git add components/product/ProductListPage.vue utils/product-list-screens.js pages/master-data/products/_id/index.vue
git commit -m "[gop_db] Hàng hoá 2-C1: nút Tạo mới, Sửa ở menu dòng và footer chi tiết"
```

---

### Task 17: Spec e2e (viết sẵn, chỉ `--list`) + kiểm tổng bằng Playwright MCP

**Files (HRM/e2e — ngoài git; viết ở bản sao `wt-chuyen-doi-hang-hoa/e2e` rồi chép về `HRM/e2e`):**
- Create: `tests/master-data/products-write.api.spec.ts`
- Create: `tests/master-data/products-form-ui.spec.ts`
- Modify: `tests/master-data/products-read-ui.spec.ts` (footer chi tiết có thể có Sửa; tab xe ẩn/hiện theo G11; cột Hành động ở entering/company)

- [ ] **Step 1: `products-write.api.spec.ts`** — ca: E14 2 token 2 công ty (`PUT` hàng công ty khác ⇒ 403), không 1652 ⇒ `POST`/`PUT` 403, body có `code`/`status`/giá ⇒ bị bỏ qua (đọc lại mã không đổi). Fixture Loại SP qua `runMysql` (`utils/apiDb.ts`) + `flushApiPermissionCache()`; dọn hàng tạo bằng SQL theo tiền tố `E2EC1` (xoá bảng con trước, `products` sau).
- [ ] **Step 2: `products-form-ui.spec.ts`** — ca E1–E13 (bảng mục 7 `c1-khao-sat-fe.md`), mỗi ca đo DOM: footer đúng 2 nút; Lưu trống ⇒ đếm `.v2-error` có chữ ≥ số ô bắt buộc + chấm đỏ đúng tab + chỉ 1 POST; Loại SP điền 3 ô cha; G11 số `.fstep` 4/5; ĐVT 0/2 cơ bản ⇒ lỗi; nhóm máy không máy ⇒ lỗi; catalog thiếu ⇒ tab Quản trị + chữ đỏ; Tạo xong ⇒ chi tiết hàng mới, badge *Đang nhập thông tin*; Sửa hàng trạng thái 1 ⇒ trạng thái giữ; rời form có thay đổi ⇒ popup "Thông tin chưa lưu"; quyền (role tạm 1653) ⇒ không Tạo/Sửa. `serial`; KHÔNG `networkidle`; bấm ô tick không chữ bằng toạ độ input (memory *e2e-viewport-1280-va-o-tick-label-rong*); viewport thật 1280.
- [ ] **Step 3: Kiểm danh sách ca** — `cd …/wt-chuyen-doi-hang-hoa/e2e && BASE_URL=http://127.0.0.1:3031 API_BASE=http://127.0.0.1:8031 npx playwright test products-form-ui products-write --list` → liệt kê đủ ca, không lỗi biên dịch. **Không chạy** (chạy khi user yêu cầu).
- [ ] **Step 4: Playwright MCP tổng** — chạy tay đủ luồng: tạo 1 hàng E2EC1 đủ 6 tab (Loại SP có tick xe) → chi tiết → Sửa (thêm ĐVT, đổi Loại SP sang không tick ⇒ cảnh báo, Lưu ⇒ tab xe biến mất ở chi tiết) → kiểm DB bằng tinker: 6 dòng giá / ĐVT, dòng công ty status 1, `productables` xe = 0. Dọn dữ liệu E2EC1.
- [ ] **Step 5: Chép spec về `HRM/e2e`** (kiểm bản chính chưa bị sửa từ lúc sao: so `ls -la` + `diff`), cập nhật checkpoint `2c-ghi/plan.md` + `SO-CHOT-VA-TON.md`.

**🏁 Kết thúc Pha 3:** báo user kết quả đo MCP + `--list`; xin quyết: chạy e2e? merge `feat/p2c1-tao-sua` → `feat/chuyen-doi-hang-hoa` + push?

---

## Self-Review (đã chạy)

| Yêu cầu spec | Task |
|---|---|
| G1 status 1, H1' Lưu không đổi trạng thái | 7 (`tao_moi_ghi_du_bat_bien_erp`), 8 (`sua_giu_ma_trang_thai_cong_ty`) |
| G2 ĐVT + 6 dòng giá 0 | 7, 8 |
| G3 1 nút Lưu, lỗi đồng thời | 6 (FormRequest gom), 7 (`luu_thieu_moi_thu_bao_loi_dong_thoi`), 11, 17 |
| G4/A2 hàng cũ sinh dòng status 3, upsert | 8 (`sua_hang_cu_…`, `dong_he_so_cu_…`) |
| G5 không ghi kép | 7 (assert `min_stock_qty` chung = 0) |
| G9a/C12 Sửa menu dòng + footer, `can_edit` | 9, 16 |
| G11 cờ + ẩn/hiện tab xe | 1, 10, 11, 14 |
| T6/C3 tech_coefficient | 6, 7, 8 |
| C1 catalog ≥1 | 6, 8 (`thieu_catalog_khi_sua_bi_422`), 15 |
| C2 Loại SP bắt buộc | 6, 8 |
| C4 trùng tên | 6, 7 |
| C5 ảnh, avatar | 5, 7, 12 |
| C6 tài liệu kỹ thuật giữ id | 7, 8, 12 |
| C7 khoá ĐVT đã lưu | 6, 8, 12 |
| C8 xoá dữ liệu xe | 7 (`writeVehicles`), 8, 12 (cảnh báo) |
| C9 thuộc tính | 6, 7, 11 (`toPayload`), 13 |
| C10 VAT tự điền | 11 (`onTypeChange` + bổ sung `vat_percent_tax_rate_id` vào product_types) |
| C11 "+" Model | 12 |
| A1 product_type NULL | 7 |
| Quyền có/không + 2 công ty | 5, 7, 8, 9, 16, 17 |

Placeholder scan: Task 4 bước 1 là "dán nguyên thân hàm đang có" — cố ý (chép code có sẵn, không viết mới). Các "> kiểm …" là bước đối chiếu schema/chữ ký trước khi chạy, không phải chỗ trống.

---

## ✅ Điểm nghi ngờ D1–D4 — user chốt 07/10/2026

| # | Câu | Chốt |
|---|---|---|
| D1 | Chủ sửa hàng CŨ chưa có dòng công ty mà 4 ô quản trị không đổi | **Chỉ sinh dòng khi 1 trong 4 ô (chính sách KD, tồn tối thiểu, bảo hành, đơn vị bảo hành) khác giá trị form đang hiện** (`AdminData::formValues`); NCC + catalog vẫn ghi — đã sửa `writeAdmin` + ca test |
| D2 | Hàng `products.status = 0` | **Không cho sửa** — 403 + `can_edit = false` |
| D3 | Nhánh catalog đã lưu nay bị khoá | **Giữ**, chỉ chặn nhánh THÊM mới; vẫn tính vào ≥ 1 (C1) |
| D4 | Đơn vị cơ bản theo cờ `units.can_be_base` | **Không xét cờ, như ERP** — FE không lọc, BE không chặn |

---

## Chưa làm / hoãn

| Việc | Đợt |
|---|---|
| Lưu nháp | bỏ (G3) |
| Sao chép | sau 2-C (G8) |
| Lấy về 1/nhiều + công ty lấy về chỉ sửa tab Quản trị (`PUT /{id}/admin-data`, dải "Hàng hoá do X tạo") | 2-C2 |
| Xoá / Khoá / Mở khoá | 2-C4 |
| Nút "+" thêm nhanh ngoài Model (Loại SP, Code đặt hàng, Thuế suất) | sau (C11) |
| Excel cột "Phụ tùng ô tô" ở danh mục Tính chất | sau (B4) |
| Kéo thả sắp xếp ảnh | sau |
| Việc ngoài luồng N1–N9 (ERP đọc cột chung, popup ERP không thấy hàng HRM tạo `product_type` NULL…) | trước khi merge prod |

## Checkpoint

- 2026-10-07: plan lập xong, chờ user duyệt + cho phép "làm" Pha 1 (kèm chạy 1 migration vào `hrm_erp`).

### Checkpoint — 2026-10-08 (PHA 1 XONG)
Nhánh `feat/p2c1-tao-sua` (hrm-api, worktree `wt-chuyen-doi-hang-hoa`), 5 commit `36056534d`…`7b799c724` trên base `626113419`; CHƯA push, chưa merge. Migration `is_auto_parts` đã chạy vào `hrm_erp` (đúng 1 file `--path`).
PHPUnit ở HEAD: NatureAutoParts 2 · CodeGenerator 9 · FormOptions 4 · ImageUpload 3 · CatalogApi 6 · ReadApi 8 · CompanyFoundation 5 · ClassificationCatalog 11 — xanh hết.
Mỗi task 1 implementer + 1 reviewer độc lập, cả 5 Approved. Ledger: `hrm-api/.superpowers/sdd/c1-plan/progress.md` (git-ignored).
Ruling mang sang Pha 2: R3 ghi `product_vehicle_model_has_life` phải gán created_at/updated_at (ERP 100% có); R4 `CatalogBranchGuard` chỉ truyền id Tiểu mục MỚI thêm (D3). Trait `actAs` đã cấp quyền qua role tạm theo công ty (R1).
Tiếp: xin "làm" Pha 2 (Task 6–9).

### Checkpoint — 2026-10-08 (PHA 2 XONG)
- hrm-api `feat/p2c1-tao-sua`: 61919fef0 ProductRequest · d00206deb store + POST · b7a4daf27 sửa sau review · 5494e371c edit + PUT + ProductFormResource · 31d89d0b9 sửa sau review · 4fcc7345c can_edit.
- Test: ProductWriteApiTest 26 + toàn bộ Product*Test + BusinessCatalogTreeTest xanh. Smoke curl/tinker của plan BỎ (ghi DB ngoài transaction ngoài phạm vi cho phép).
- Rulings Pha 2 (ledger hrm-api/.superpowers/sdd/c1-plan/progress.md): R5 units sửa `nullable` · R6 authorize gọi assertOwner (403 trước 422) · R7 không nới rule dữ liệu cũ · R8 so D1 giữ nguyên · R9 ảnh: sửa mà danh sách ảnh không đổi ⇒ không đụng ảnh + avatar; form trả `avatar` riêng, không lùi gallery về avatar · R10 id = 0 ⇒ null ở form (ERP coi 0 = rỗng) · R11 tệp tài liệu giữ id dòng `files` · R12 3 hàng >10 ảnh để FE báo lỗi.
- Điểm Pha 3 FE phải nhớ: luôn gửi `is_auto_parts` (Task 10); nạp form bằng `/edit` + `form-options?include_ids=<option_ids>`; hiện `avatar` khi hàng chưa có gallery; gửi lại `files[].id`.

### Checkpoint — 2026-10-08 (PHA 3 + REVIEW CUỐI XONG)
- hrm-api HEAD `5fdc679c8`, hrm-client HEAD `8218f6caa` (nhánh `feat/p2c1-tao-sua`, worktree). Chưa merge `feat/chuyen-doi-hang-hoa`, chưa push.
- Ngoài kế hoạch: `396fdcfd0` khai `intervention/image` (đã có sẵn trong lock qua mews/captcha — vendor local cũ thiếu); `28e4a1684`+`2cc527227` chi tiết ẩn tab xe theo `show_vehicle_tab` (Tính chất phụ tùng HOẶC có dữ liệu xe).
- Review cuối: sửa 1 Critical (xoá dữ liệu xe hàng cũ khi Lưu — nay CHỈ xoá khi ĐỔI Loại SP từ loại thật sang không phụ tùng, R19/R23), IDOR id tài liệu kỹ thuật (R21), quyền ghi theo công ty (R22, PermissionService), giữ đời xe cũ (R20).
- Spec e2e: `products-write.api` (7), `products-form-ui` (18), `products-read-ui` (sửa) — chỉ `--list`, CHƯA chạy; đã chép về `HRM/e2e`.
- Dữ liệu tạm đã dọn hết (DB). Còn 3 ảnh thử trên S3.
- **Việc ngoài luồng thêm:** N10 tick cờ "Phụ tùng ô tô" cho các Tính chất phụ tùng thật TRƯỚC go-live (cờ mặc định 0); N11 nhánh thiếu migration drop `product_types.can_retail` (DB đã chạy từ gop_db) ⇒ entity còn fillable can_retail; N12 tài khoản e2e nocost có sẵn quyền 1652 (role E2E No Cost) ⇒ thiếu tài khoản e2e "chỉ xem"; N13 hiệu năng form sửa hàng cũ nhiều đời xe (7338: mở tab xe 4.5s dev); tồn nhỏ: URL ảnh không kiểm định dạng, hàng kèm theo chọn trúng hàng ERP đã xoá, S3 mồ côi khi rollback, composer.lock đổi định dạng (Composer mới).

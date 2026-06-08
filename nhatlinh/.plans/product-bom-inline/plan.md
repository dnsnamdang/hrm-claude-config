# BOM inline trong Hàng hoá — Implementation Plan

> **Checkpoint 2026-06-06: CODE HOÀN THÀNH** (Phase 1 BE + Phase 2 FE, chạy main chưa commit).
> Thực thi bằng subagent-driven (5 subagent BE + 3 subagent FE). Cổng review:
> - BE gate (smoke-test HTTP 5 kịch bản) PASS: POST tạo SP+BOM nested (code `BOM-<id>`, status theo SP, default_bom_id=bom id, items=1); show trả boms[0].histories + material_name; PUT thêm NVL (items=2, histories=2); NVL=chính SP→422; bom_items rỗng→xoá BOM + default_bom_id=null.
> - FE gate: ProductForm + BomHistoryModal compile sạch; không còn tham chiếu productBoms/productBom/AddBomModal/category/boms; trang boms/index + AddBomModal đã xoá; menu BOM đã gỡ.
> Còn lại: **Task 11 (user test trên trình duyệt)**.

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để chạy từng task. Đánh `[x]` khi xong.

**Goal:** Tạo/sửa BOM ngay trong tab BOM của hàng hoá, lưu nested; bỏ hẳn danh mục BOM riêng + permission BOM.

**Architecture:** BOM trở thành phần phụ của hàng hoá (1 product → ≤1 bom row). Lưu nested trong `ProductService` (cùng `DB::transaction` của ProductController). Mã/Tên BOM tự sinh, status theo hàng hoá. Lịch sử kèm trong API chi tiết hàng hoá. Gỡ toàn bộ API/trang/menu/permission BOM độc lập.

**Tech Stack:** Laravel 8 (PHP 8.1), MySQL, JWT; Nuxt 2 (Vue 2), Bootstrap-Vue. Spec: `docs/superpowers/specs/2026-06-06-product-bom-inline-design.md`.

**Quy ước project (BẮT BUỘC):**
- KHÔNG commit/push git (bỏ mọi bước commit; thay bằng bước verify).
- Không có test suite tự động. **Verify BE** = `php -l` + smoke-test HTTP in-process (mẫu ở Task 6). **Verify FE** = compile bằng `vue-template-compiler` + `@babel/parser` (mẫu ở Task 10).
- Làm trên nhánh hiện tại (không tạo branch nếu chưa yêu cầu).

**File map:**
| File | Việc |
|------|------|
| `nhatlinh-api/Modules/Category/Http/Requests/ProductRequest.php` | + rule `bom_note`/`bom_items` + validate NVL ≠ chính SP |
| `nhatlinh-api/Modules/Category/Services/ProductService.php` | + `syncProductBom()` + inject BomService, gọi trong updateOrCreate/update |
| `nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/ProductController.php` | show: load `boms.histories` |
| `nhatlinh-api/Modules/Category/Transformers/ProductResource/DetailProductResource.php` | boms[] + `histories` |
| `nhatlinh-api/Modules/Category/Routes/api.php` | xoá group `/boms` + import BomController |
| `nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/BomController.php` | XOÁ |
| `nhatlinh-api/Modules/Category/Http/Requests/BomRequest.php` | XOÁ |
| `nhatlinh-api/app/ExcelExport/BomExport.php` | XOÁ |
| `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | xoá dòng 1105/1106 + xoá DB |
| `nhatlinh-client/pages/category/products/components/ProductForm.vue` | tab BOM thành editor + payload + load |
| `nhatlinh-client/pages/category/boms/components/BomHistoryModal.vue` | `open(bom)` nhận `bom.histories` trực tiếp |
| `nhatlinh-client/pages/category/boms/index.vue` | XOÁ |
| `nhatlinh-client/pages/category/boms/AddBomModal.vue` | XOÁ |
| `nhatlinh-client/components/default-menu/category.js` | xoá mục menu BOM |

**GIỮ NGUYÊN:** `Bom.php`, `BomItem.php`, `BomHistory.php`, `BomService.php` (dùng `syncItems`).

---

## Phase 1 — Backend

### Task 1: ProductRequest — rule nested BOM

**Files:** Modify `nhatlinh-api/Modules/Category/Http/Requests/ProductRequest.php`

- [ ] **Step 1: Thêm rule** vào cuối mảng `$rules` (ngay trước `return $rules;`), sau dòng `'images.*.file_path' => ...`:

```php
            'bom_note' => 'nullable|string|max:255',
            'bom_items' => 'nullable|array',
            'bom_items.*.material_product_id' => 'required_with:bom_items|exists:products,id',
            'bom_items.*.unit_id' => 'nullable|exists:units,id',
            'bom_items.*.norm_quantity' => 'required_with:bom_items|integer|min:0',
            'bom_items.*.waste_percent' => 'nullable|integer|min:0|max:100',
            'bom_items.*.note' => 'nullable|max:255',
```

- [ ] **Step 2: Validate NVL ≠ chính sản phẩm** — trong `withValidator($validator)`, bên trong `$validator->after(function ($validator) { ... })`, thêm vào cuối closure (sau khối kiểm tra `units`):

```php
            foreach ($this->input('bom_items', []) as $i => $item) {
                if (
                    !empty($this->id)
                    && isset($item['material_product_id'])
                    && (int) $item['material_product_id'] === (int) $this->id
                ) {
                    $validator->errors()->add(
                        "bom_items.$i.material_product_id",
                        'Nguyên vật liệu không được trùng với chính sản phẩm.'
                    );
                }
            }
```

- [ ] **Step 3: Thêm message** vào mảng `messages()` (trước `]` đóng):

```php
            'bom_items.*.material_product_id.required_with' => 'Vui lòng chọn nguyên vật liệu',
            'bom_items.*.norm_quantity.required_with' => 'Vui lòng nhập định mức',
            'bom_items.*.norm_quantity.integer' => 'Định mức phải là số nguyên',
            'bom_items.*.waste_percent.integer' => 'Hao hụt phải là số nguyên',
```

- [ ] **Step 4: Verify** `php -l Modules/Category/Http/Requests/ProductRequest.php` → "No syntax errors".

### Task 2: ProductService — syncProductBom

**Files:** Modify `nhatlinh-api/Modules/Category/Services/ProductService.php`

- [ ] **Step 1: Thêm import** (cạnh các `use` hiện có ở đầu file):

```php
use Modules\Category\Entities\Bom;
use Modules\Category\Entities\BomHistory;
```

- [ ] **Step 2: Inject BomService** — thêm property + constructor ngay sau dòng `class ProductService extends BaseService\n{`:

```php
    private $bomService;

    public function __construct(BomService $bomService)
    {
        $this->bomService = $bomService;
    }
```

- [ ] **Step 3: Gọi syncProductBom** — trong `updateOrCreate()`, ngay sau dòng `$this->syncImages($product, $request->images ?? []);` (trước `return response()->json(...)`):

```php
        $this->syncProductBom($product, $request);
```

  và y hệt trong `update()` ngay sau `$this->syncImages($product, $request->images ?? []);` (trước `return $product->load(...)`):

```php
        $this->syncProductBom($product, $request);
```

- [ ] **Step 4: Thêm method** `syncProductBom` (đặt sau `update()` hoặc cuối class, trước `}` đóng class):

```php
    /**
     * Đồng bộ BOM nội bộ của hàng hoá (mỗi SP ≤1 BOM).
     * - bom_items rỗng → xoá BOM + default_bom_id=null.
     * - có items → upsert BOM (code/name tự sinh, status theo hàng hoá), ghi lịch sử, set default_bom_id.
     */
    private function syncProductBom(Product $product, ProductRequest $request): void
    {
        $items = collect($request->bom_items ?? [])
            ->filter(fn($it) => !empty($it['material_product_id']))
            ->values()
            ->all();

        $bom = Bom::where('product_id', $product->id)->first();

        if (empty($items)) {
            if ($bom) {
                $bom->histories()->delete();
                $bom->items()->delete();
                $bom->delete();
            }
            if ($product->default_bom_id) {
                $product->default_bom_id = null;
                $product->save();
            }
            return;
        }

        if (!$bom) {
            $bom = new Bom();
            $bom->product_id = $product->id;
            $bom->created_by = auth()->user()->id;
            $bom->part_id = auth()->user()->info->part_id ?? null;
        }
        $bom->code = 'BOM-' . $product->id;
        $bom->name = $product->name;
        $bom->status = $product->status;
        $bom->note = $request->bom_note;
        $bom->is_default = 0;
        $bom->updated_by = auth()->user()->id;
        $bom->save();

        $this->bomService->syncItems($bom, $items);

        BomHistory::create([
            'bom_id' => $bom->id,
            'snapshot' => json_encode([
                'note' => $bom->note,
                'status' => $bom->status,
                'items' => $items,
            ], JSON_UNESCAPED_UNICODE),
            'note' => 'Lưu BOM (từ hàng hoá)',
            'created_by' => auth()->id(),
            'created_at' => now(),
        ]);

        if ($product->default_bom_id != $bom->id) {
            $product->default_bom_id = $bom->id;
            $product->save();
        }
    }
```

- [ ] **Step 5: Verify** `php -l Modules/Category/Services/ProductService.php` → "No syntax errors".

### Task 3: ProductController show + DetailProductResource histories

**Files:** Modify `nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/ProductController.php`, `nhatlinh-api/Modules/Category/Transformers/ProductResource/DetailProductResource.php`

- [ ] **Step 1: Load histories** — trong `show()`, sửa dòng `$product->load([...])` thêm `'boms.histories'`:

```php
        $product->load(['manufacturer', 'countryOfOrigin', 'productType', 'productUnits.unit', 'files', 'supplier', 'defaultBom', 'boms.items.material', 'boms.items.unit', 'boms.histories']);
```

- [ ] **Step 2: Trả histories trong boms[]** — trong `DetailProductResource::toArray`, ở mảng `'boms' => $this->boms->map(function ($bom) { return [ ... ]; })`, thêm field `'histories'` vào trong mảng trả (sau `'items' => ...`):

```php
                    'histories' => $bom->histories->sortBy('id')->values()->map(function ($h) {
                        return [
                            'id' => $h->id,
                            'created_at' => \Modules\Human\Helper\Helper::formatDateTime($h->created_at),
                            'created_by_name' => $h->created_by_name,
                            'note' => $h->note,
                            'snapshot' => json_decode($h->snapshot, true),
                        ];
                    }),
```

  (File đã `use Modules\Human\Helper\Helper;` — có thể dùng `Helper::formatDateTime(...)` thay vì FQN nếu import sẵn.)

- [ ] **Step 3: Verify** `php -l` cả 2 file → "No syntax errors".

### Task 4: Gỡ API BOM độc lập

**Files:** Modify `nhatlinh-api/Modules/Category/Routes/api.php`; Delete `BomController.php`, `BomRequest.php`, `app/ExcelExport/BomExport.php`

- [x] **Step 1: Xoá route group** — trong `Routes/api.php`, xoá nguyên khối `Route::group(['prefix' => '/boms'], function () { ... });` (10 route bên trong) và xoá dòng `use Modules\Category\Http\Controllers\Api\V1\BomController;` ở đầu file.

- [x] **Step 2: Xoá file:**

```bash
rm nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/BomController.php
rm nhatlinh-api/Modules/Category/Http/Requests/BomRequest.php
rm nhatlinh-api/app/ExcelExport/BomExport.php
```

- [x] **Step 3: Kiểm tra không còn tham chiếu** (ngoài entity/service giữ lại):

```bash
grep -rn "BomController\|BomRequest\|BomExport" nhatlinh-api/Modules/Category nhatlinh-api/app
```
Expected: không còn dòng nào trỏ tới các file vừa xoá (BomService/Bom entity được giữ).
→ Kết quả: rỗng (PASS). Bonus: BomService.php đã dùng BomRequest làm type-hint → thay bằng Request chuẩn để không bị autoload lỗi.

- [x] **Step 4: Verify** `php artisan route:list --path=category/boms` → rỗng (không còn route boms). Nếu lỗi cache: `php artisan route:clear` rồi chạy lại.
→ route:clear thành công; route:list lỗi pre-existing (DecisionController chưa tồn tại — không liên quan Task 4). Xác nhận bằng grep api.php: không còn dòng nào về boms/BomController (PASS).

### Task 5: Gỡ permission BOM

**Files:** Modify `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [ ] **Step 1: Xoá 2 dòng seeder** (dòng 1058–1059):

```php
        Permission::create(['id' => 1105, 'guard_name' => 'api', 'name' => 'Quản lý định mức BOM', 'display_name' => 'Quản lý định mức BOM', 'group' => 'Danh mục chung', 'type' => 8]);
        Permission::create(['id' => 1106, 'guard_name' => 'api', 'name' => 'Xem định mức BOM', 'display_name' => 'Xem định mức BOM', 'group' => 'Danh mục chung', 'type' => 8]);
```
  (Nếu có dòng gán 2 permission này cho role trong seeder → xoá luôn.)

- [ ] **Step 2: Xoá khỏi DB** (theo convention: sửa seeder + update DB, KHÔNG tạo migration). Chạy:

```bash
php artisan tinker --execute='
DB::table("role_has_permissions")->whereIn("permission_id",[1105,1106])->delete();
DB::table("permissions")->whereIn("id",[1105,1106])->delete();
echo "removed BOM perms\n";
'
```

- [ ] **Step 3: Verify** `php -l` seeder + kiểm tra DB:

```bash
php artisan tinker --execute='echo DB::table("permissions")->whereIn("id",[1105,1106])->count();'
```
Expected: `0`.

### Task 6: Verify BE end-to-end (smoke test HTTP in-process)

**Files:** tạm `/tmp/bom_inline_test.php` (xoá sau khi chạy)

- [ ] **Step 1: Viết script test** — bootstrap kernel + JWT, chạy các kịch bản:

```php
<?php
require '/Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-api/vendor/autoload.php';
$app = require_once '/Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-api/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$emp = \App\Models\TpEmployee::find(13);
$token = \Tymon\JWTAuth\Facades\JWTAuth::fromUser($emp);
function call($k,$t,$m,$u,$b=null){$r=Illuminate\Http\Request::create($u,$m,[],[],[],['HTTP_AUTHORIZATION'=>'Bearer '.$t,'HTTP_ACCEPT'=>'application/json','CONTENT_TYPE'=>'application/json'],$b!==null?json_encode($b):null);$res=$k->handle($r);return [$res->getStatusCode(),json_decode($res->getContent(),true)];}
use Modules\Category\Entities\Product;use Modules\Category\Entities\Bom;use Modules\Category\Entities\BomItem;use Modules\Category\Entities\ProductUnit;
$sfx = str_pad((string) random_int(1000,9999),4,'0'); $code='BIN'.$sfx;
$base = ['code'=>$code,'name'=>'SP bom inline','product_type_id'=>1,'status'=>1,'product_classification'=>2,'units'=>[['unit_id'=>1,'is_base_unit'=>1,'conversion_rate'=>1,'price_p0'=>1000]]];

// 1) Tạo SP kèm bom_items (nested)
[$st,$d]=call($kernel,$token,'POST','/api/v1/category/products',array_merge($base,['bom_note'=>'note v1','bom_items'=>[['material_product_id'=>1,'unit_id'=>1,'norm_quantity'=>2,'waste_percent'=>5]]]));
$p=Product::where('code',$code)->first();
$bom=Bom::where('product_id',$p->id)->first();
echo "1) POST status=$st; bom_code=".($bom->code)." (expect BOM-{$p->id}); status=".($bom->status)." (expect 1); default_bom_id=".($p->fresh()->default_bom_id)."; items=".BomItem::where('bom_id',$bom->id)->count()." (expect 1)\n";

// 2) GET show có boms[0].histories
[$st,$d]=call($kernel,$token,'GET',"/api/v1/category/products/{$p->id}");
$b0=$d['data']['boms'][0]??null;
echo "2) show histories=".count($b0['histories']??[])." (expect 1); item material_name=".($b0['items'][0]['material_name']??'NULL')."\n";

// 3) PUT thêm 1 NVL nữa (status vẫn 1)
[$st,$d]=call($kernel,$token,'PUT',"/api/v1/category/products/{$p->id}",array_merge($base,['id'=>$p->id,'bom_note'=>'note v2','bom_items'=>[['material_product_id'=>1,'unit_id'=>1,'norm_quantity'=>3,'waste_percent'=>0],['material_product_id'=>1,'unit_id'=>1,'norm_quantity'=>1]]]));
$bom=Bom::where('product_id',$p->id)->first();
echo "3) PUT status=$st; items=".BomItem::where('bom_id',$bom->id)->count()." (expect 2); histories=".$bom->histories()->count()." (expect 2)\n";

// 4) NVL trùng chính SP -> 422
[$st,$d]=call($kernel,$token,'PUT',"/api/v1/category/products/{$p->id}",array_merge($base,['id'=>$p->id,'bom_items'=>[['material_product_id'=>$p->id,'norm_quantity'=>1]]]));
echo "4) NVL=self status=$st (expect 422); err=".json_encode($d['errors']??null,JSON_UNESCAPED_UNICODE)."\n";

// 5) PUT bom_items rỗng -> xoá BOM
[$st,$d]=call($kernel,$token,'PUT',"/api/v1/category/products/{$p->id}",array_merge($base,['id'=>$p->id,'bom_items'=>[]]));
echo "5) empty items status=$st; bom_exists=".(Bom::where('product_id',$p->id)->exists()?'YES(BUG)':'NO'); echo "; default_bom_id=".var_export($p->fresh()->default_bom_id,true)." (expect NULL)\n";

// cleanup
ProductUnit::where('product_id',$p->id)->delete();
Bom::where('product_id',$p->id)->each(function($b){$b->histories()->delete();$b->items()->delete();$b->delete();});
Product::where('id',$p->id)->delete();
echo "cleanup done\n";
```

- [ ] **Step 2: Chạy** `php /tmp/bom_inline_test.php 2>&1 | grep -v "deprecated\|Warning"` rồi `rm /tmp/bom_inline_test.php`.
  Expected: (1) BOM-<id>, status=1, items=1; (2) histories=1, material_name có giá trị; (3) items=2, histories=2; (4) 422; (5) bom_exists=NO, default_bom_id=NULL.

---

## Phase 2 — Frontend

### Task 7: BomHistoryModal nhận histories trực tiếp

**Files:** Modify `nhatlinh-client/pages/category/boms/components/BomHistoryModal.vue`

- [ ] **Step 1: Sửa `open`** — thay phần fetch bằng nhận `bom.histories`:

```js
        async open(bom) {
            this.bomCode = (bom && bom.code) || ''
            this.historyItems = []
            this.$bvModal.show('bom-history-modal')
            this.loading = true
            try {
                await this.loadMaps()
                this.buildHistory(bom && bom.histories ? bom.histories : [])
            } finally {
                this.loading = false
            }
        },
```

- [ ] **Step 2: Đổi `fetchHistory(bomId)` → `buildHistory(histories)`** (bỏ gọi API, nhận mảng):

```js
        buildHistory(histories) {
            const list = (histories || []).slice().sort((a, b) => a.id - b.id)
            const items = []
            let prevSnap = {}
            list.forEach((h, idx) => {
                const snap = h.snapshot || {}
                items.push({
                    created_at: h.created_at,
                    created_by_name: h.created_by_name,
                    isCreate: idx === 0,
                    changes: this.diffSnapshot(prevSnap, snap),
                })
                prevSnap = snap
            })
            this.historyItems = items.reverse()
        },
```

  Giữ nguyên `loadMaps`, `diffSnapshot`, `formatScalar`, `itemLabel`, các const/label. (diffSnapshot vẫn so sánh code/name/status/note + items; snapshot mới chỉ có note/status/items nên code/name không hiện thay đổi — đúng ý đồ.)

- [ ] **Step 3: Verify compile** (mẫu lệnh ở Task 10) cho `BomHistoryModal.vue`.

### Task 8: ProductForm — tab BOM thành editor

**Files:** Modify `nhatlinh-client/pages/category/products/components/ProductForm.vue`

- [ ] **Step 1: Thay template tab BOM** — thay nguyên khối từ `<!-- Tab: BOM -->` đến `<!-- /tab BOM -->` bằng:

```html
                    <!-- Tab: BOM -->
                    <div v-show="activeTab === 'bom'">
                        <div class="d-flex align-items-center justify-content-between mb-3">
                            <h6 class="font-weight-bold mb-0">Định mức nguyên vật liệu (BOM)</h6>
                            <div class="d-flex align-items-center" style="gap: 14px">
                                <a
                                    v-if="productId && productBomHistories.length"
                                    href="#"
                                    class="small"
                                    @click.prevent="openBomHistory"
                                >
                                    <i class="ri-history-line mr-1"></i>Xem lịch sử
                                </a>
                                <V2BaseButton v-if="!isView" secondary size="sm" @click="addBomItem">
                                    <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
                                    Thêm NVL
                                </V2BaseButton>
                            </div>
                        </div>

                        <div class="table-responsive">
                            <table class="table table-bordered table-sm mb-0">
                                <thead class="thead-light">
                                    <tr>
                                        <th style="min-width: 220px">Nguyên vật liệu <span v-if="!isView" class="text-danger">*</span></th>
                                        <th style="width: 150px">ĐVT</th>
                                        <th style="width: 130px">Định mức/1SP <span v-if="!isView" class="text-danger">*</span></th>
                                        <th style="width: 120px">Hao hụt (%)</th>
                                        <th style="min-width: 160px">Ghi chú</th>
                                        <th v-if="!isView" style="width: 44px"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(c, i) in form.bom_items" :key="c._key">
                                        <td>
                                            <V2BaseSelect
                                                v-model="c.material_product_id"
                                                :options="bomMaterialOptions"
                                                :allowClear="true"
                                                placeholder="Chọn NVL"
                                                size="sm"
                                                :disabled="isView"
                                                :class="{ 'is-invalid': bomTouched && !c.material_product_id }"
                                            />
                                            <div v-if="bomTouched && !c.material_product_id" class="invalid-feedback" style="display: block">
                                                Vui lòng chọn NVL
                                            </div>
                                        </td>
                                        <td>
                                            <V2BaseSelect
                                                v-model="c.unit_id"
                                                :options="unitOptions"
                                                :allowClear="true"
                                                placeholder="Chọn ĐVT"
                                                size="sm"
                                                :disabled="isView"
                                            />
                                        </td>
                                        <td>
                                            <V2BaseInput
                                                v-model.number="c.norm_quantity"
                                                type="number"
                                                step="1"
                                                min="0"
                                                size="sm"
                                                :disabled="isView"
                                                :class="{ 'is-invalid': bomTouched && !(c.norm_quantity > 0) }"
                                            />
                                            <div v-if="bomTouched && !(c.norm_quantity > 0)" class="invalid-feedback" style="display: block">
                                                Định mức phải lớn hơn 0
                                            </div>
                                        </td>
                                        <td>
                                            <V2BaseInput
                                                v-model.number="c.waste_percent"
                                                type="number"
                                                step="1"
                                                min="0"
                                                max="100"
                                                size="sm"
                                                :disabled="isView"
                                            />
                                        </td>
                                        <td>
                                            <V2BaseInput v-model="c.note" size="sm" :disabled="isView" />
                                        </td>
                                        <td v-if="!isView" class="text-center align-middle">
                                            <button type="button" class="btn btn-sm btn-link text-danger p-0" title="Xoá" @click="removeBomItem(i)">
                                                <i class="ri-delete-bin-6-line"></i>
                                            </button>
                                        </td>
                                    </tr>
                                    <tr v-if="!form.bom_items.length">
                                        <td :colspan="isView ? 5 : 6" class="text-center">Chưa có định mức. Bấm "Thêm NVL".</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="form-row mt-2">
                            <div class="col-md-12 mb-2">
                                <V2BaseLabel>Ghi chú định mức</V2BaseLabel>
                                <V2BaseInput v-model="form.bom_note" size="sm" placeholder="Nhập ghi chú..." :disabled="isView" />
                            </div>
                        </div>
                    </div>
                    <!-- /tab BOM -->
```

- [ ] **Step 2: data()** — trong object trả về của `data()`: (a) đổi badge tab dùng `form.bom_items.length` thay `productBoms.length`; (b) thêm state. Trong khối `form: { ... }` thêm `bom_items: []`, `bom_note: ''`. Ngoài `form`, cạnh `productBoms: []`, thêm:

```js
            productBomHistories: [],
            bomTouched: false,
            _bomItemKeySeq: 1,
```

  Và ở template nav-tab (dòng ~59) đổi `v-if="productBoms.length"` + `{{ productBoms.length }}` → `form.bom_items.length`.

- [ ] **Step 3: computed** — thêm `bomMaterialOptions` (loại trừ chính sản phẩm đang sửa). `productOptions` lấy từ Step 5. Thêm vào khối `computed`:

```js
        bomMaterialOptions() {
            if (!this.productId) return this.productOptions
            return this.productOptions.filter((p) => String(p.id) !== String(this.productId))
        },
```

  Giữ computed `productBom` (vẫn dùng cho nơi khác? nếu không còn dùng thì xoá). **Lưu ý:** sau Step 1, `productBom` không còn được template dùng → xoá computed `productBom` và biến `productBoms` nếu không nơi nào tham chiếu (kiểm tra bằng grep ở Step 7).

- [ ] **Step 4: methods BOM** — thêm:

```js
        addBomItem() {
            this.form.bom_items.push({
                _key: 'n' + this._bomItemKeySeq++,
                material_product_id: null,
                unit_id: null,
                norm_quantity: 0,
                waste_percent: 0,
                note: '',
            })
        },
        removeBomItem(i) {
            this.form.bom_items.splice(i, 1)
        },
        openBomHistory() {
            this.$refs.bomHistoryModal.open({ code: this.form.code, histories: this.productBomHistories })
        },
```

  (Xoá method `openBomHistory` cũ nếu trùng tên — chỉ giữ bản này.)

- [ ] **Step 5: Load danh sách NVL** — trong `created()` (đang `await Promise.all([this.loadSelectOptions(), this.loadSuppliers()])`) thêm `this.loadMaterials()` vào mảng. Thêm method:

```js
        async loadMaterials() {
            try {
                const res = await this.$store.dispatch('apiGetMethod', 'category/products/getAll')
                this.productOptions = (res.data || []).map((i) => ({ id: i.id, name: `${i.code} - ${i.name}` }))
            } catch (e) {
                this.productOptions = []
            }
        },
```

  Thêm `productOptions: []` vào `data()` (cạnh `unitOptions: []`).

- [ ] **Step 6: loadData + submitForm** — trong `loadData()`, thay dòng `this.productBoms = data.boms || []` bằng map BOM vào form:

```js
                const bom0 = (data.boms && data.boms[0]) || null
                this.form.bom_note = bom0 ? bom0.note || '' : ''
                this.form.bom_items = bom0
                    ? (bom0.items || []).map((it) => ({
                          _key: 'e' + (it.id || this._bomItemKeySeq++),
                          material_product_id: it.material_product_id || null,
                          unit_id: it.unit_id || null,
                          norm_quantity: it.norm_quantity != null ? it.norm_quantity : 0,
                          waste_percent: it.waste_percent != null ? it.waste_percent : 0,
                          note: it.note || '',
                      }))
                    : []
                this.productBomHistories = bom0 ? bom0.histories || [] : []
```

  Trong `submitForm(saveStatus)`: (a) sau `if (!this.validateUnits()) { ... return }` thêm validate BOM:

```js
            this.bomTouched = true
            const bomInvalid = this.form.bom_items.some(
                (c) => !c.material_product_id || !(c.norm_quantity > 0),
            )
            if (bomInvalid) {
                this.activeTab = 'bom'
                this.isSubmitting = false
                this.$toasted?.global?.error?.({ message: 'Định mức (BOM) chưa hợp lệ' })
                return
            }
```

  (b) trong object `payload`, thêm (cạnh `supplier_id`):

```js
                    bom_note: (this.form.bom_note || '').trim(),
                    bom_items: this.form.bom_items.map((c) => ({
                        material_product_id: c.material_product_id,
                        unit_id: c.unit_id || null,
                        norm_quantity: c.norm_quantity || 0,
                        waste_percent: c.waste_percent || 0,
                        note: (c.note || '').trim(),
                    })),
```

- [ ] **Step 7: Dọn tham chiếu cũ** — kiểm tra & xoá nếu còn:

```bash
cd nhatlinh-client && grep -n "productBoms\|productBom\b\|/category/boms" pages/category/products/components/ProductForm.vue
```
  Xoá `productBoms` (data), computed `productBom`, và bất kỳ chỗ nào còn trỏ `/category/boms`. Đảm bảo `BomHistoryModal` vẫn được import + đăng ký + có `<BomHistoryModal ref="bomHistoryModal" />` trong template (đã có sẵn từ trước — giữ nguyên).

- [ ] **Step 8: Verify compile** ProductForm (mẫu Task 10).

### Task 9: Xoá trang BOM + mục menu

**Files:** Delete `pages/category/boms/index.vue`, `pages/category/boms/AddBomModal.vue`; Modify `components/default-menu/category.js`

- [ ] **Step 1: Xoá 2 file FE:**

```bash
rm nhatlinh-client/pages/category/boms/index.vue
rm nhatlinh-client/pages/category/boms/AddBomModal.vue
```
  (GIỮ `pages/category/boms/components/BomHistoryModal.vue`.)

- [ ] **Step 2: Xoá mục menu** — trong `components/default-menu/category.js`, xoá object:

```js
            {
                label: 'BOM',
                link: '/category/boms',
            },
```

- [ ] **Step 3: Kiểm tra không còn link tới trang đã xoá:**

```bash
cd nhatlinh-client && grep -rn "category/boms'" pages/category components/default-menu | grep -v "boms/components"
```
Expected: không còn (trừ import BomHistoryModal trong ProductForm).

### Task 10: Verify FE compile toàn bộ file đụng tới

- [ ] **Step 1: Chạy** (từ `nhatlinh-client`):

```bash
node -e '
const fs=require("fs"),c=require("vue-template-compiler"),b=require("@babel/parser");
for(const f of ["pages/category/products/components/ProductForm.vue","pages/category/boms/components/BomHistoryModal.vue"]){
  const s=c.parseComponent(fs.readFileSync(f,"utf8"));const t=c.compile(s.template.content);
  if(t.errors&&t.errors.length){console.log("TPL ERR",f,t.errors);process.exit(1);}
  b.parse(s.script.content,{sourceType:"module",plugins:["objectRestSpread"]});console.log("OK",f);
}'
```
Expected: `OK ...ProductForm.vue` và `OK ...BomHistoryModal.vue`.

---

## Phase 3 — Kiểm thử tổng hợp (user)

### Task 11: Test thủ công trên trình duyệt
- [ ] Tạo mới hàng hoá sản xuất → tab BOM thêm vài NVL (NVL không có chính nó trong dropdown) → bấm Lưu → DB có BOM `BOM-<id>`, status=1.
- [ ] Tạo Lưu nháp → BOM status=3.
- [ ] Sửa hàng hoá: thêm/xoá NVL, đổi ghi chú → Lưu → đúng; bấm "Xem lịch sử" thấy các mốc thay đổi.
- [ ] Xoá hết NVL → Lưu → BOM bị xoá, default_bom_id null.
- [ ] Menu Danh mục không còn mục "BOM"; gõ `/category/boms` không còn trang.

---

## Self-review (đã rà)
- **Spec coverage:** mô hình/code-name auto (T2), status theo SP (T2), nested save (T1,T2), show histories (T3), bỏ API/route (T4), bỏ permission (T5), tab editor (T8), modal nhận data (T7), xoá trang+menu (T9). Đủ.
- **Type consistency:** payload `bom_note`/`bom_items` khớp giữa ProductRequest (T1), ProductService (T2), ProductForm submit (T8). `boms[0].histories.snapshot` khớp giữa DetailProductResource (T3) và BomHistoryModal.buildHistory/diffSnapshot (T7).
- **No placeholder:** mọi step có code/lệnh cụ thể.

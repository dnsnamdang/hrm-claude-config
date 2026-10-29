# YCXH port đầy đủ từ ERP — Implementation Plan (Phase 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phiếu Yêu cầu xuất hàng (YCXH) HRM lưu nháp chỉ cần Loại, chọn/đổi nguồn khi sửa nháp, hoàn thiện loại 20/21 (HĐ HRM), bảng nhập tay đủ cột như ERP, loại 99 chọn HĐ chi phí, loại 3 hạn mức ngày trả.

**Architecture:** BE giữ 1 controller (`ProductExportRequestController`) + 1 service (`ProductExportRequestService`) trong `Modules/Assign`, thêm 5 endpoint tĩnh trước `/{id}`. FE tách dần 3 component con khỏi `ProductExportRequestForm.vue` (2572 dòng): `SourcePicker.vue`, `ManualLinesTable.vue`, `ContractCostModal.vue`. ERP là nguồn logic, HRM là nguồn UI (skill erp-to-hrm-screen).

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 + BootstrapVue (hrm-client), PHPUnit feature test, Playwright (e2e). ERP: Laravel + Blade/AngularJS (TanPhatDev) — chỉ chạm ở Task 9.

**Spec:** `docs/superpowers/specs/gop-db/2026-10-12-ycxh-port-erp-day-du-design.md` (tóm tắt: `.plans/gop-db/ycxh-port-erp-day-du/design.md`)

## Global Constraints

- Nhánh `gop_db` ở cả `hrm-api`, `hrm-client`, `ERP/TanPhatDev`. **KHÔNG commit / push khi user chưa yêu cầu** — bước "Commit" trong mỗi task chỉ chạy khi user đã bảo commit; nếu chưa, đánh dấu "chờ commit" ở ledger rồi đi tiếp.
- KHÔNG dùng `DB_CONNECTION_SECOND` / connection `mysql2` (chung DB gộp).
- KHÔNG migration, KHÔNG thêm permission mới.
- Hàm dùng chung (`StockService`, `CompanyConfig`, `QuotationProductSearchModal`, `unsavedChangesMixin`, model ERP dùng chung) → **chỉ GỌI, không sửa**. Cần sửa → dừng hỏi user.
- PHP 7.4: không `?->`, không `match`, không named args. Arrow fn `fn()` được.
- Trạng thái: `3` = Đang tạo (nháp), `2` = Chờ duyệt (gửi), `6` = Đã hủy.
- Thông điệp tiếng Việt chép NGUYÊN VĂN:
  - Đổi nguồn: `Đổi nguồn sẽ thay toàn bộ danh sách hàng hoá. Tiếp tục?`
  - HĐ chưa đủ điều kiện: `Hợp đồng chưa đủ điều kiện xuất hàng (chưa có hiệu lực hoặc chưa nhập thời hạn thực hiện).`
  - Vượt còn lại: `Sản phẩm "<tên>" vượt số lượng còn được xuất (<còn lại>).` (key `products.{i}.qty`)
  - Đổi nguồn khi không nháp: `Chỉ được đổi nguồn khi phiếu đang nháp.`
  - Loại 3: `Ngày trả không được quá dd/mm/yyyy (tối đa N ngày).`
- Route mới khai trong group `/assign/product-export-requests` (`Modules/Assign/Routes/api.php:695`), **TRƯỚC** `Route::get('/{id}')`.
- FE: popup dùng `V2BaseModal` + `utils/pickerPagination.js`; xác nhận dùng `this.$confirm`; ghi dữ liệu user chọn sau `await` thì gán `this.unsavedLastActionAt = Date.now()` ngay trước khi ghi (skill unsaved-changes).
- Số hiển thị: `toLocaleString('en-US')` (dấu phẩy ngăn nghìn).
- Cảnh báo tồn < SL: chữ xám/vàng, KHÔNG đỏ, KHÔNG chặn lưu. Đỏ chỉ dành cho lỗi validate.
- Task sửa FE phải kiểm bằng Playwright trước khi báo xong.
- Chạy BE test: `cd HRM/hrm-api && php artisan test --filter=<Tên>`. Đăng nhập test: `$this->actingAs(TpEmployee::find(13), 'api')` (NV 13, công ty 1), kho id 1.
- Chạy e2e: `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/product-export-requests` — cần API :8000 + client :3000 (Nuxt đang chạy nền, ĐỪNG khởi động lại).

## Spec corrections / Rulings (đã kiểm code, plan theo bản ĐÚNG)

| # | Spec ghi | Thực tế | Plan làm |
|---|---|---|---|
| R1 | Dropdown Tạo đã ẩn 4/15/16/17 | `DROPDOWN_TYPE_IDS` (`ProductExportRequest.php:91`) vẫn chứa 4/15/16/17; `getDropdownTypes()` (`:129`) map nguyên mảng | Task 2: lọc `getDropdownTypes()` theo `CREATABLE_TYPE_IDS`, giữ thứ tự ERP |
| R2 | §5.4: loại 99 nguồn = HĐ hãng + HĐ HRM, UNION | ERP loại 1–7 lấy từ `contracts.type` (`App\Contract`); popup ERP `SearchController@searchContract:2186` lọc **1 `contract_type` mỗi lần**; class lưu: `App\Contract`, `App\Model\Sale\ServiceContract`, `App\Model\Sale\ProjectContract`, `App\Model\Accounting\OpeningContract`. ERP `ProductExportRequest::contract_costable()` (`:367`) là morphTo, eager-load ở `:780`, `:1147`, đọc `->link` ở `:1151` → lưu class HRM vào đó ERP **crash** | Endpoint HRM theo đúng mẫu ERP: tham số `contract_type` bắt buộc, 1 nguồn/lần. Nhóm "HĐ HRM" lưu class do user chọn ở **Câu hỏi mở Q-ERP** (A: model ERP mới `App\Model\Hrm\HrmContract`; B: morphMap alias). Task 8 phần lưu HĐ HRM + Task 9 **chờ user chọn** |
| R3 | Đổi nguồn khi phiếu không còn nháp → 422 | `canEdit()` (`ProductExportRequest.php:289`) chỉ cho sửa nháp → đường update không bao giờ tới | Giữ làm guard phòng thủ trong service, test bằng cách gọi service trực tiếp |
| R4 | `except_id` của `getLineStocks` = id YCXH | `except_id` là id ĐNXK | Truyền `null` |
| R5 | Popup HĐ chi phí: phạm vi theo quyền như ERP | ERP lọc theo bộ quyền riêng từng loại HĐ | Phase 1: chỉ HĐ có `company_id` = công ty người đăng nhập. Ghi rõ ở Review Focus, Phase 5 làm theo quyền |
| R6 | ĐVT ở bảng nhập tay lấy từ popup chọn hàng | `QuotationProductSearchModal` là component dùng chung, không trả danh sách ĐVT | Endpoint riêng của YCXH `GET product-units?product_ids[]=` — không sửa modal dùng chung |

### Câu hỏi Q-ERP — ĐÃ CHỐT 2026-10-12: **A** (user "ok" với khuyến nghị) → Task 8b + Task 9 làm theo A

**Q-ERP — Lưu morph HĐ HRM cho loại 99 sao cho ERP không crash?**
- **A (khuyến nghị):** thêm model ERP `App\Model\Hrm\HrmContract` (bảng `hrm_contracts`, `getLinkAttribute()` trỏ màn HRM). HRM lưu `contract_costable_type = 'App\Model\Hrm\HrmContract'`. Không đụng code cũ của ERP, chỉ thêm 1 file.
- **B:** thêm `Relation::morphMap(['hrm_contract' => …])` ở `AppServiceProvider` ERP — ảnh hưởng toàn bộ morph của ERP (morphMap đổi cách lưu class), rủi ro cao hơn.

## Review Focus

1. **Đổi nguồn trên phiếu nháp đã có dòng, rồi bấm "Ở lại"/Hủy ở popup xác nhận** → nguồn cũ và dòng cũ còn nguyên, không gọi API. Test: Task 11 Step 1 (ca hủy confirm).
2. **Sửa nháp 20/21 mà KHÔNG đổi HĐ** → dòng hàng giữ nguyên SL user đã nhập (không bị nạp lại từ HĐ, không reset SL về còn lại). Test: Task 4 `test_sua_nhap_giu_nguon_thi_giu_dong`.
3. **"Còn lại" khi sửa chính phiếu đó** → không tự chặn chính mình: SL của phiếu đang sửa được cộng lại vào còn lại. Test: Task 5 `test_gui_duyet_khi_sua_khong_tu_chan_chinh_minh`.
4. **Bảng nhập tay: đổi ĐVT của dòng** → cột Tồn tính lại theo ĐVT mới (vì `getLineStocks` key theo `product_id`, phải gọi riêng theo `unit_id`). Test: Task 7 `test_ton_theo_tung_don_vi_tinh`.
5. **Loại 99 đổi sang nhóm HĐ khác rồi lưu** → `contract_costable_type` khớp đúng class của nhóm mới; loại khác 99 luôn lưu null. Test: Task 8 `test_loai_khac_99_bo_qua_morph`. Phạm vi HĐ theo công ty (R5) là điểm reviewer cần nhìn kỹ — người khác công ty không được thấy HĐ.

---

## Sơ đồ file

**BE (`HRM/hrm-api/`)**
- Modify `Modules/Assign/Entities/Warehouse/ProductExportRequest.php` — `getDropdownTypes()`.
- Modify `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` — `rulesForType`, `createData`, `editData`, 5 action mới (`hrmContracts`, `stockOfProducts`, `productUnits`, `costContracts`), bỏ `contractProductLines` (chuyển vào service).
- Modify `Modules/Assign/Services/ProductExportRequestService.php` — `createFromRequest`, `updateFromRequest`, `contractRemainingByLine`, `assertContractCanExport`, `assertContractLineQtyWithinRemaining`, `assertReturnDateWithinLimit`, morph loại 99.
- Create `Modules/Assign/Services/ProductExportRequestPickerService.php` — query cho 4 endpoint picker (giữ service chính không phình thêm).
- Modify `Modules/Assign/Routes/api.php:695-750`.
- Create `tests/Feature/ProductExportRequest/ProductExportRequestFixture.php` + 7 file test.

**FE (`HRM/hrm-client/`)**
- Modify `pages/finance/product-export-requests/components/ProductExportRequestForm.vue`.
- Create `pages/finance/product-export-requests/components/SourcePicker.vue`.
- Create `pages/finance/product-export-requests/components/HrmContractSearchModal.vue`.
- Create `pages/finance/product-export-requests/components/ManualLinesTable.vue`.
- Create `pages/finance/product-export-requests/components/StockViewModal.vue`.
- Create `pages/finance/product-export-requests/components/ContractCostModal.vue`.
- Modify trang chi tiết `pages/finance/product-export-requests/_id/index.vue` (hiện Kho xuất 20/21 + HĐ chi phí 99).

**e2e (`HRM/e2e/`)**
- Create `pages/ProductExportRequestPage.ts`, `tests/product-export-requests/{draft,source-change,contract-20-21,manual-lines,type-99,type-3}.spec.ts`.

**ERP (`ERP/TanPhatDev/`)** — chỉ Task 9, chờ Q-ERP.

---

## Task 0: Fixture test dùng chung

**Files:**
- Create: `hrm-api/tests/Feature/ProductExportRequest/ProductExportRequestFixture.php`

**Interfaces:**
- Produces (trait `ProductExportRequestFixture`, dùng ở mọi test BE sau):
  - `loginAs13(): void` — `actingAs(TpEmployee::find(13), 'api')`.
  - `makeHrmContract(array $over = [], array $lines = null): object` — trả `{id, parent_line_id, child_line_id, product_id, unit_id}`; mặc định HĐ **đủ điều kiện xuất** (status 6, có effective_date, execution_deadline_days, execution_end_date) với 1 dòng cha + 1 dòng con, `qty_needed` = 10 mỗi dòng.
  - `postRequest(array $payload): \Illuminate\Testing\TestResponse` — `POST /api/assign/product-export-requests`.
  - `putRequest(int $id, array $payload): \Illuminate\Testing\TestResponse`.
  - `anyProductUnit(): object` — `{product_id, unit_id}` có thật trong `product_units`.

- [x] **Step 1: Kiểm cột NOT NULL của 2 bảng HĐ trước khi viết fixture**

Run:
```bash
cd HRM/hrm-api && php artisan tinker --execute="foreach(['hrm_contracts','hrm_contract_product_prices'] as \$t){echo \$t.': ';foreach(DB::select(\"SHOW COLUMNS FROM \$t\") as \$c){if(\$c->Null==='NO'&&\$c->Default===null&&\$c->Extra!=='auto_increment')echo \$c->Field.' ';}echo PHP_EOL;}"
```
Expected: `hrm_contracts: code customer_id customer_name effective_date project_id quotation_id sign_date …` — nếu có cột NOT NULL khác, thêm vào mảng mặc định ở Step 2.

- [x] **Step 2: Viết fixture**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Support\Facades\DB;
use Modules\Timesheet\Entities\TpEmployee;

trait ProductExportRequestFixture
{
    protected function loginAs13(): void
    {
        $this->actingAs(TpEmployee::find(13), 'api');
    }

    protected function anyProductUnit(): object
    {
        return DB::table('product_units')
            ->whereNotNull('product_id')->whereNotNull('unit_id')
            ->select('product_id', 'unit_id')->first();
    }

    /**
     * HĐ HRM mặc định ĐỦ điều kiện xuất (mirror Contract::getCanExportAttribute):
     * status = 6 (CO_HIEU_LUC), có effective_date, execution_deadline_days, execution_end_date.
     * 1 dòng cha (parent_id null) + 1 dòng con (parent_id = dòng cha), qty_needed 10/dòng.
     */
    protected function makeHrmContract(array $over = [], array $lines = null): object
    {
        $pu = $this->anyProductUnit();
        $id = DB::table('hrm_contracts')->insertGetId(array_merge([
            'code' => 'HD-TEST-' . uniqid(),
            'customer_id' => 1,
            'customer_name' => 'KH test YCXH',
            'project_id' => 0,
            'quotation_id' => 0,
            'sign_date' => now()->toDateString(),
            'effective_date' => now()->toDateString(),
            'execution_deadline_days' => 30,
            'execution_end_date' => now()->addDays(30)->toDateString(),
            'status' => 6,
            'company_id' => 1,
            'created_by' => 13,
            'created_at' => now(),
            'updated_at' => now(),
        ], $over));

        $base = [
            'contract_id' => $id, 'code' => 'SP-TEST', 'name' => 'SP test',
            'erp_product_id' => $pu->product_id, 'unit_id' => $pu->unit_id,
            'qty_needed' => 10, 'quoted_price' => 1000, 'extra_price' => 0,
            'unit_price_after_discount' => 1000, 'vat_percent' => 10, 'sort_order' => 1,
            'created_at' => now(), 'updated_at' => now(),
        ];
        $parentLineId = DB::table('hrm_contract_product_prices')->insertGetId(
            array_merge($base, ['parent_id' => null], $lines[0] ?? [])
        );
        $childLineId = DB::table('hrm_contract_product_prices')->insertGetId(
            array_merge($base, ['parent_id' => $parentLineId, 'sort_order' => 2], $lines[1] ?? [])
        );

        return (object) [
            'id' => $id, 'parent_line_id' => $parentLineId, 'child_line_id' => $childLineId,
            'product_id' => $pu->product_id, 'unit_id' => $pu->unit_id,
        ];
    }

    protected function postRequest(array $payload)
    {
        return $this->postJson('/api/assign/product-export-requests', $payload);
    }

    protected function putRequest(int $id, array $payload)
    {
        return $this->putJson('/api/assign/product-export-requests/' . $id, $payload);
    }
}
```

- [x] **Step 3: Smoke test fixture**

Tạo `tests/Feature/ProductExportRequest/FixtureSmokeTest.php`:
```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\Assign\Entities\Contract\Contract;
use Tests\TestCase;

class FixtureSmokeTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    public function test_hd_mac_dinh_du_dieu_kien_xuat(): void
    {
        $c = $this->makeHrmContract();
        $this->assertTrue(Contract::find($c->id)->can_export);
    }
}
```
Run: `php artisan test --filter=FixtureSmokeTest` — Expected: PASS 1/1. Nếu FAIL vì cột NOT NULL → bổ sung mặc định ở Step 2.

- [ ] **Step 4: Commit (chỉ khi user đã yêu cầu commit)**
```bash
git -C HRM/hrm-api add tests/Feature/ProductExportRequest
git -C HRM/hrm-api commit -m "test(ycxh): fixture HĐ HRM cho test YCXH"
```

---

## Task 1: Validate — nháp chỉ cần Loại, bỏ chặn nguồn khi sửa, kho 20/21

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php:724-855` (`rulesForType`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/DraftRulesTest.php`

**Interfaces:**
- Consumes: fixture Task 0.
- Produces: `rulesForType(int $type, bool $isUpdate, int $status)` — chữ ký giữ nguyên; khi sửa vẫn nhận `emplement_contract_id` (20/21/19), `emplement_contract_type` (19), `firm_contract_id` (14). Task 4 dựa vào các field này có mặt trong `$data` đã validate.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class DraftRulesTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    /** @dataProvider creatableTypes */
    public function test_nhap_chi_can_loai(int $type): void
    {
        $this->postRequest(['type' => $type, 'status' => 3])->assertStatus(200);
    }

    public function creatableTypes(): array
    {
        return [[3], [6], [7], [12], [18], [99], [20], [21], [14], [19]];
    }

    public function test_nhap_thieu_loai_bi_422(): void
    {
        $this->postRequest(['status' => 3])->assertStatus(422)->assertJsonValidationErrors('type');
    }

    public function test_gui_duyet_20_thieu_kho_bi_422(): void
    {
        $c = $this->makeHrmContract();
        $this->postRequest([
            'type' => 20, 'status' => 2, 'emplement_contract_id' => $c->id, 'transition_type' => 1,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => 1]],
        ])->assertStatus(422)->assertJsonValidationErrors('warehouse_id');
    }

    public function test_gui_duyet_20_xuat_thang_khong_can_kho(): void
    {
        $c = $this->makeHrmContract();
        $this->postRequest([
            'type' => 20, 'status' => 2, 'emplement_contract_id' => $c->id, 'is_export_direct' => 1,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => 1]],
        ])->assertStatus(200);
    }

    public function test_sua_nhap_nhan_emplement_contract_id(): void
    {
        $id = $this->postRequest(['type' => 21, 'status' => 3])->json('data.id');
        $c = $this->makeHrmContract();
        $this->putRequest($id, ['status' => 3, 'emplement_contract_id' => $c->id])->assertStatus(200);
        $this->assertDatabaseHas('product_export_requests', ['id' => $id, 'emplement_contract_id' => $c->id]);
    }
}
```
> Nếu response store trả id ở key khác `data.id`, đọc `store()` (`Controller:698-717`) và sửa `json('…')` cho khớp — ghi Ruling.

- [x] **Step 2: Chạy, xác nhận FAIL**

Run: `php artisan test --filter=DraftRulesTest`
Expected: FAIL — `test_gui_duyet_20_thieu_kho_bi_422` (200 thay vì 422), `test_sua_nhap_nhan_emplement_contract_id` (id không đổi). Các ca nháp có thể đã PASS — ghi lại kết quả thật.

- [x] **Step 3: Sửa `rulesForType`**

Ba thay đổi:

(a) bỏ `if (!$isUpdate)` quanh rule nguồn của 20/21, 14, 19:
```php
        if ($isContract) {
            $rules['emplement_contract_id'] = ($isDraft ? 'nullable' : 'required')
                . '|integer|exists:hrm_contracts,id';
            $rules['is_export_direct'] = 'nullable|boolean';
            $rules['need_repair'] = 'nullable|in:0,1';
        }

        if ($isFirmContract) {
            $rules['firm_contract_id'] = ($isDraft ? 'nullable' : 'required') . '|integer|exists:firm_contracts,id';
            $rules['is_export_direct'] = 'nullable|boolean';
            $rules['need_repair'] = $isDraft ? 'nullable|in:0,1' : 'required|in:0,1';
        }
```
```php
        // Loại 19: nguồn chọn/đổi được cả khi sửa nháp (spec §5.1). Bắt buộc khi gửi duyệt.
        if ($type === ProductExportRequest::XUAT_THUC_HIEN_HD) {
```
Sửa comment cũ "Không cho đổi khi sửa." → bỏ.

(b) thêm kho cho 20/21 ở phần gửi duyệt (sau khối `if ($isFirmContract) { … warehouse_id … }`):
```php
        if ($isContract) { // 20/21: kho bắt buộc khi gửi duyệt, trừ xuất thẳng (spec Q5)
            $rules['warehouse_id'] = 'required_unless:is_export_direct,1|nullable|integer|exists:warehouses,id';
        }
```

(c) nháp: thêm `warehouse_id` nullable để giá trị nháp được lưu:
```php
        if ($isDraft) {
            $rules['warehouse_id'] = 'nullable|integer';
            if ($isTransfer) {
```

- [x] **Step 4: Chạy, xác nhận PASS**

Run: `php artisan test --filter=DraftRulesTest` — Expected: PASS 14/14 (10 data provider + 4). `test_sua_nhap_nhan_emplement_contract_id` có thể vẫn FAIL vì service chưa ghi id mới → đó là phạm vi Task 4: đánh `@group pending-task4` cho riêng test đó, chạy `--exclude-group pending-task4`, gỡ group ở Task 4.

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)**
```bash
git -C HRM/hrm-api add Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php tests/Feature/ProductExportRequest/DraftRulesTest.php
git -C HRM/hrm-api commit -m "feat(ycxh): nháp chỉ cần Loại, nhận nguồn khi sửa, kho bắt buộc 20/21"
```

---

## Task 2: Dropdown Tạo chỉ hiện loại đã port (ẩn 4/15/16/17)

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/Warehouse/ProductExportRequest.php:129` (`getDropdownTypes`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/TypeOptionsTest.php`

**Interfaces:**
- Produces: `GET /assign/product-export-requests/type-options` → `selectable_types` chỉ chứa id ∈ `CREATABLE_TYPE_IDS`, theo thứ tự `DROPDOWN_TYPE_IDS`. FE (`ProductExportRequestForm.vue:1419-1424`) không đổi.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class TypeOptionsTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    public function test_dropdown_an_loai_chua_port_va_giu_thu_tu_erp(): void
    {
        $this->loginAs13();
        $ids = collect($this->getJson('/api/assign/product-export-requests/type-options')->json('data.selectable_types'))
            ->pluck('id')->map(fn ($v) => (int) $v)->all();

        $this->assertSame([14, 3, 6, 7, 12, 18, 19, 99, 20, 21], $ids);
    }
}
```
> Nếu payload không bọc trong `data`, đọc `typeOptions()` (`Controller:330`) và sửa đường dẫn JSON — ghi Ruling.

- [x] **Step 2: Chạy, xác nhận FAIL** — `php artisan test --filter=TypeOptionsTest`. Expected: FAIL, mảng thật có thêm 15, 4, 16, 17.

- [x] **Step 3: Sửa `getDropdownTypes()`**

```php
    public static function getDropdownTypes(): array
    {
        // Chỉ loại đã port xong (CREATABLE_TYPE_IDS), giữ thứ tự ERP của DROPDOWN_TYPE_IDS.
        // 4/15/16/17 hiện lại khi phase tương ứng hoàn tất (spec Q3).
        $ids = array_values(array_filter(
            self::DROPDOWN_TYPE_IDS,
            fn ($id) => in_array($id, self::CREATABLE_TYPE_IDS, true)
        ));
        // … phần map id → {id, name} giữ NGUYÊN như code hiện tại, chỉ đổi nguồn mảng sang $ids
    }
```
Đọc thân hàm hiện tại ở `:129` và chỉ thay biến mảng nguồn.

- [x] **Step 4: Chạy, xác nhận PASS** — Expected: PASS 1/1.

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): dropdown Tạo ẩn loại chưa port"`

---

## Task 3: Tạo phiếu không nguồn → chỉ lưu header

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ProductExportRequestService.php:283-308` (`createFromRequest`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/CreateWithoutSourceTest.php`

**Interfaces:**
- Produces: `createFromRequest(array $data): ProductExportRequest` — 20/21 không `emplement_contract_id` → đi `createManual($data + ['products' => []])`, phiếu giữ `type` 20/21, không dòng hàng. 14 không `firm_contract_id` đã có sẵn nhánh trống (`createFromFirmContract:912`). 7 không phiếu chuyển → `createFromTransfer` với mảng rỗng (đã chạy được). 19 → `createManual` (sẵn).

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class CreateWithoutSourceTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    /** @dataProvider sourceTypes */
    public function test_nhap_khong_nguon_luu_header_khong_dong(int $type): void
    {
        $this->loginAs13();
        $id = $this->postRequest(['type' => $type, 'status' => 3])->assertStatus(200)->json('data.id');

        $this->assertDatabaseHas('product_export_requests', ['id' => $id, 'type' => $type, 'status' => 3]);
        $this->assertSame(0, DB::table('product_export_request_details')->where('parent_id', $id)->count());
        $this->assertMatchesRegularExpression('/^PYCXH-\d{5,}$/', DB::table('product_export_requests')->where('id', $id)->value('code'));
    }

    public function sourceTypes(): array
    {
        return [[20], [21], [14], [7], [19]];
    }
}
```

- [x] **Step 2: Chạy, xác nhận FAIL** — Expected: ca 20/21 FAIL (`ModelNotFoundException` → 404/500 từ `Contract::findOrFail(null)`).

- [x] **Step 3: Sửa `createFromRequest`**

Trong nhánh 20/21:
```php
        if (in_array($type, [ProductExportRequest::XUAT_SAN_XUAT_HOP_DONG, ProductExportRequest::XUAT_BAN_HOP_DONG], true)) {
            if (empty($data['emplement_contract_id'])) {
                // Nháp chưa chọn HĐ (spec §5.1): chỉ lưu header, giữ type 20/21; dòng hàng nạp khi chọn HĐ ở màn Sửa.
                $req = $this->createManual(array_merge($data, ['products' => []]));
            } else {
                $contract = Contract::findOrFail((int) $data['emplement_contract_id']);
                $req = $this->createFromContract($contract, $data);
            }
        }
```
Giữ nguyên tên biến/chữ ký `createFromContract` đang dùng ở `:283-308` (đọc trước khi sửa). `createManual` tạo tab "Hàng nhập tay" rỗng — chấp nhận; Task 4 xoá tab khi nạp HĐ (`deleteLines`).

- [x] **Step 4: Chạy, xác nhận PASS** — `php artisan test --filter=CreateWithoutSourceTest` → PASS 5/5. Chạy lại `DraftRulesTest` → vẫn PASS.

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): lưu nháp 20/21 chưa chọn HĐ"`

---

## Task 4: Sửa nháp — chọn/đổi nguồn, nạp lại dòng

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ProductExportRequestService.php:1119-1240` (`updateFromRequest`), `:668` (`updateTransfer`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/SourceChangeTest.php`

**Interfaces:**
- Consumes: `$data` đã validate từ Task 1 (có `emplement_contract_id`, `emplement_contract_type`, `firm_contract_id`, `product_transfer_requests`).
- Produces:
  - `private function applySourceChange(ProductExportRequest $req, array $data, int $statusBefore): bool` — trả `true` nếu nguồn đổi. Ghi `emplement_contract_id/_code/_type` (20/21/19) hoặc `firm_contract_id` (14) + snapshot KH từ nguồn mới. Ném 422 `Chỉ được đổi nguồn khi phiếu đang nháp.` (key `source`) nếu `$statusBefore !== 3` và nguồn đổi.
  - Quy tắc dòng: nguồn đổi → `deleteLines` + ghi dòng từ nguồn mới theo `products[]` FE gửi (FE đã nạp lại từ nguồn mới); nguồn giữ nguyên → hành vi hiện tại (ghi lại từ `products[]`).
  - Loại 7: `updateTransfer` nhận `product_transfer_requests` khi nháp → nếu tập id khác tập đang gắn: gỡ link phiếu cũ (`product_export_request_id = null`, `status = 2`), rồi `syncTransferRequests($req, $newIds)`.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Modules\Assign\Entities\Warehouse\ProductExportRequest;
use Modules\Assign\Services\ProductExportRequestService;
use Tests\TestCase;

class SourceChangeTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    private function draft20WithContract(object $c, float $qty = 2): int
    {
        return $this->postRequest([
            'type' => 20, 'status' => 3, 'emplement_contract_id' => $c->id,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => $qty]],
        ])->assertStatus(200)->json('data.id');
    }

    public function test_chon_hd_lan_dau_tren_nhap_trong(): void
    {
        $id = $this->postRequest(['type' => 20, 'status' => 3])->json('data.id');
        $c = $this->makeHrmContract();

        $this->putRequest($id, ['status' => 3, 'emplement_contract_id' => $c->id,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => 3]]])->assertStatus(200);

        $req = ProductExportRequest::find($id);
        $this->assertSame($c->id, (int) $req->emplement_contract_id);
        $this->assertSame('KH test YCXH', $req->customer_name);
        $this->assertEquals(3, DB::table('product_export_request_tab_products')
            ->where('product_export_request_id', $id)->value('qty'));
    }

    public function test_doi_hd_thay_toan_bo_dong(): void
    {
        $a = $this->makeHrmContract();
        $b = $this->makeHrmContract(['customer_name' => 'KH B']);
        $id = $this->draft20WithContract($a);

        $this->putRequest($id, ['status' => 3, 'emplement_contract_id' => $b->id,
            'products' => [['contract_product_id' => $b->child_line_id, 'qty' => 1]]])->assertStatus(200);

        $lines = DB::table('product_export_request_tab_products')->where('product_export_request_id', $id)->get();
        $this->assertCount(1, $lines);
        $this->assertSame($b->id, (int) $lines[0]->emplement_contract_id);
        $this->assertSame('KH B', ProductExportRequest::find($id)->customer_name);
    }

    public function test_sua_nhap_giu_nguon_thi_giu_dong(): void
    {
        $c = $this->makeHrmContract();
        $id = $this->draft20WithContract($c, 4);

        $this->putRequest($id, ['status' => 3, 'emplement_contract_id' => $c->id, 'note' => 'sửa ghi chú',
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => 4]]])->assertStatus(200);

        $this->assertEquals(4, DB::table('product_export_request_tab_products')
            ->where('product_export_request_id', $id)->value('qty'));
    }

    public function test_doi_hd_hang_loai_14(): void
    {
        $firmIds = DB::table('firm_contracts')->orderByDesc('id')->limit(2)->pluck('id')->all();
        $this->assertCount(2, $firmIds, 'Cần ≥2 HĐ hãng trong DB dev');
        $id = $this->postRequest(['type' => 14, 'status' => 3, 'firm_contract_id' => $firmIds[0]])->json('data.id');

        $this->putRequest($id, ['status' => 3, 'firm_contract_id' => $firmIds[1], 'products' => []])->assertStatus(200);

        $this->assertSame((int) $firmIds[1], (int) ProductExportRequest::find($id)->firm_contract_id);
    }

    public function test_doi_hd_loai_19(): void
    {
        $firmIds = DB::table('firm_contracts')->orderByDesc('id')->limit(2)->pluck('id')->all();
        $id = $this->postRequest(['type' => 19, 'status' => 3, 'emplement_contract_type' => 'firm',
            'emplement_contract_id' => $firmIds[0]])->json('data.id');

        $this->putRequest($id, ['status' => 3, 'emplement_contract_type' => 'firm',
            'emplement_contract_id' => $firmIds[1], 'products' => []])->assertStatus(200);

        $this->assertSame((int) $firmIds[1], (int) ProductExportRequest::find($id)->emplement_contract_id);
    }

    public function test_doi_nguon_khi_khong_con_nhap_bi_chan(): void
    {
        $a = $this->makeHrmContract();
        $b = $this->makeHrmContract();
        $id = $this->draft20WithContract($a);
        DB::table('product_export_requests')->where('id', $id)->update(['status' => 2]);

        $this->expectException(ValidationException::class);
        app(ProductExportRequestService::class)->updateFromRequest(ProductExportRequest::find($id), [
            'status' => 2, 'emplement_contract_id' => $b->id,
            'products' => [['contract_product_id' => $b->child_line_id, 'qty' => 1]],
        ]);
    }
}
```
> Đọc chữ ký thật `updateFromRequest` ở `:1119` (thứ tự tham số `$req, $data`) và sửa lời gọi trong test nếu khác — ghi Ruling.

- [x] **Step 2: Chạy, xác nhận FAIL** — `php artisan test --filter=SourceChangeTest`. Expected: FAIL ở `chon_hd_lan_dau`, `doi_hd_*`, `doi_nguon_khi_khong_con_nhap` (id nguồn không đổi). `giu_nguon_thi_giu_dong` có thể PASS sẵn.

- [x] **Step 3: Thêm `applySourceChange` + gọi trong `updateFromRequest`**

```php
    /**
     * Chọn/đổi nguồn khi sửa nháp (spec §5.1). Trả true nếu nguồn đổi.
     * Nguồn: 20/21 → HĐ HRM; 14 → HĐ hãng; 19 → HĐ bán firm|wr. Loại 7 xử lý riêng ở updateTransfer.
     * Guard phòng thủ: canEdit() đã chỉ cho sửa nháp, nhưng service vẫn chặn đổi nguồn khi không nháp.
     */
    private function applySourceChange(ProductExportRequest $req, array $data, int $statusBefore): bool
    {
        $type = (int) $req->type;
        $isContract = in_array($type, [ProductExportRequest::XUAT_SAN_XUAT_HOP_DONG, ProductExportRequest::XUAT_BAN_HOP_DONG], true);

        if ($isContract || $type === ProductExportRequest::XUAT_THUC_HIEN_HD) {
            if (!array_key_exists('emplement_contract_id', $data)) {
                return false;
            }
            $newId = !empty($data['emplement_contract_id']) ? (int) $data['emplement_contract_id'] : null;
            if ($isContract) {
                $newClass = $newId ? Contract::class : null;
                $source = $newId ? Contract::find($newId) : null;
            } else {
                $isWr = ($data['emplement_contract_type'] ?? null) === 'wr';
                $newClass = $newId ? ($isWr ? WrServiceContract::class : FirmContract::class) : null;
                $source = $newId ? ($isWr ? WrServiceContract::find($newId) : FirmContract::find($newId)) : null;
            }
            $changed = $newId !== ($req->emplement_contract_id ? (int) $req->emplement_contract_id : null)
                || ($newId && $newClass !== $req->emplement_contract_type);
            if (!$changed) {
                return false;
            }
            $this->assertDraftForSourceChange($statusBefore);
            $req->emplement_contract_id = $newId;
            $req->emplement_contract_code = $source->code ?? null;
            $req->emplement_contract_type = $newClass;
            $this->fillCustomerSnapshot($req, $source);
            return true;
        }

        if ($type === ProductExportRequest::XUAT_BAN_HD_HANG) {
            if (!array_key_exists('firm_contract_id', $data)) {
                return false;
            }
            $newId = !empty($data['firm_contract_id']) ? (int) $data['firm_contract_id'] : null;
            if ($newId === ($req->firm_contract_id ? (int) $req->firm_contract_id : null)) {
                return false;
            }
            $this->assertDraftForSourceChange($statusBefore);
            $source = $newId ? FirmContract::find($newId) : null;
            $req->firm_contract_id = $newId;
            $this->fillCustomerSnapshot($req, $source);
            return true;
        }

        return false;
    }

    private function assertDraftForSourceChange(int $statusBefore): void
    {
        if ($statusBefore !== ProductExportRequest::STATUS_DANG_TAO) {
            throw ValidationException::withMessages(['source' => ['Chỉ được đổi nguồn khi phiếu đang nháp.']]);
        }
    }

    /**
     * Snapshot KH từ nguồn — cùng quy tắc đọc cột với createManual (19) / createFromFirmContract (14) /
     * createFromContract (20/21): SĐT firm = customer_contact_phone, wr = customer_contact_phones;
     * MST: HĐ HRM/wr = customer_tax_code, firm = identity_card_number. Nguồn null → xoá snapshot.
     */
    private function fillCustomerSnapshot(ProductExportRequest $req, $source): void
    {
        $phone = $source ? ($source->customer_contact_phone ?? $source->customer_contact_phones ?? null) : null;
        $req->customer_id = $source->customer_id ?? null;
        $req->customer_name = $source->customer_name ?? null;
        $req->customer_address = $source->customer_address ?? null;
        $req->customer_contact_name = $source->customer_contact_name ?? null;
        $req->customer_mobile = $phone;
        $req->customer_contact_phone = $phone;
        $req->identity_card_number = $source ? ($source->customer_tax_code ?? $source->identity_card_number ?? null) : null;
    }
```

Trong `updateFromRequest`, ngay sau khi có `$statusBefore` và TRƯỚC khối cập nhật header theo nhánh:
```php
            $this->applySourceChange($req, $data, $statusBefore);
```
Rồi ở phần ghi lại dòng, đổi điều kiện nhánh để dùng giá trị mới trên `$req` (không phải giá trị cũ):
- nhánh HĐ HRM: `if ($isContract && $req->emplement_contract_id) { $contract = Contract::findOrFail($req->emplement_contract_id); … }` — `$req->emplement_contract_id` rỗng thì chỉ `deleteLines`, không ghi dòng.
- nhánh firm: `if ($req->firm_contract_id) { $firm = FirmContract::findOrFail($req->firm_contract_id); …tab + writeFirmContractLines }`.
- Tab mới đặt `name` = mã nguồn mới, `emplement_contract_id`/`firm_contract_id` = id mới.

Đảm bảo khối "cập nhật header" theo nhánh **không ghi đè lại** snapshot KH bằng giá trị FE gửi cho 20/21/14/19 (KH chỉ đọc ở FE với các loại này).

- [x] **Step 4: Loại 7 — nhận đổi phiếu chuyển khi nháp**

Trong `updateTransfer`, trước `$req->save()`:
```php
        // Nháp được chọn/đổi phiếu chuyển (spec §5.1). Tập khác tập đang gắn → gỡ link cũ rồi gắn lại.
        if ((int) $req->status === ProductExportRequest::STATUS_DANG_TAO && array_key_exists('product_transfer_requests', $data)) {
            $newIds = array_values(array_unique(array_filter(array_map('intval', $data['product_transfer_requests'] ?? []))));
            sort($newIds);
            $oldIds = array_map('intval', $linkedIds);
            sort($oldIds);
            if ($newIds !== $oldIds) {
                $req->export_company_id = !empty($data['export_company_id']) ? (int) $data['export_company_id'] : $req->export_company_id;
                $req->kind_of_import = !empty($data['kind_of_import']) ? (int) $data['kind_of_import'] : $req->kind_of_import;
                $this->assertTransferRequestsSameCreator($newIds, (int) $req->kind_of_import, $isExportDirect);
                ProductTransferRequest::whereIn('id', array_diff($oldIds, $newIds))
                    ->update(['product_export_request_id' => null, 'status' => 2]);
                $this->syncTransferRequests($req, $newIds);
            }
        }
```
⚠️ `$req->status` phải đọc TRƯỚC dòng `$req->status = $data['status'] ?? …`. Đặt khối này ngay sau `assertTransferRequestsSameCreator($linkedIds, …)`.
⚠️ Gỡ link đặt lại `status = 2` (Chờ duyệt) cho phiếu chuyển — **đây là điều kiện hoàn tác, theo ERP CLAUDE.md "Không tự quyết định điều kiện xóa — phải hỏi"**: trước khi viết, đối chiếu ERP `ProductExportRequest::syncProductTransferRequests` (`ERP/TanPhatDev/app/Model/Warehouse/ProductExportRequest.php` ~`:2021`) xem ERP gỡ link trả về status nào. Khớp ERP thì làm; ERP không có nhánh gỡ → **dừng hỏi user**.

Thêm test:
```php
    public function test_loai_7_doi_phieu_chuyen_khi_nhap(): void
    {
        $ids = DB::table('product_transfer_requests')->where('status', 2)->whereNull('product_export_request_id')
            ->orderByDesc('id')->limit(2)->pluck('id')->all();
        if (count($ids) < 2) {
            $this->markTestSkipped('DB dev thiếu 2 phiếu chuyển chờ duyệt chưa gắn');
        }
        $id = $this->postRequest(['type' => 7, 'status' => 3, 'product_transfer_requests' => [$ids[0]]])->json('data.id');

        $this->putRequest($id, ['status' => 3, 'product_transfer_requests' => [$ids[1]]])->assertStatus(200);

        $this->assertNull(DB::table('product_transfer_requests')->where('id', $ids[0])->value('product_export_request_id'));
        $this->assertSame($id, (int) DB::table('product_transfer_requests')->where('id', $ids[1])->value('product_export_request_id'));
    }
```

- [x] **Step 5: Chạy, xác nhận PASS** — `php artisan test --filter='SourceChangeTest|DraftRulesTest|CreateWithoutSourceTest'` (gỡ `@group pending-task4` ở DraftRulesTest). Expected: tất cả PASS (ca loại 7 có thể SKIP nếu thiếu data — ghi lại).

- [x] **Step 6: Kiểm lịch sử** — mở `logCatalogUpdate` đang gọi sau transaction: đổi nguồn phải sinh dòng "Thay đổi thông tin" có `emplement_contract_code`/`customer_name` mới (skill entity-history §3). Nếu `catalogColumns()` của service không có `emplement_contract_code`/`firm_contract_id` → thêm vào, rồi thêm assert:
```php
        $this->assertTrue(DB::table('system_logs')->where('loggable_id', $id)->where('action', 'update')->exists());
```
(đọc tên bảng/cột log thật ở `logCatalogUpdate` trước khi viết assert — sửa cho khớp, ghi Ruling).

- [ ] **Step 7: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): chọn/đổi nguồn khi sửa nháp"`

---

## Task 5: Gửi duyệt 20/21 — HĐ đủ điều kiện + SL ≤ còn lại

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ProductExportRequestService.php` (thêm 3 method; gọi ở `createFromContract` + `updateFromRequest`)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php:427-479` — `contractProductLines` gọi sang service
- Test: `hrm-api/tests/Feature/ProductExportRequest/ContractSubmitTest.php`

**Interfaces:**
- Produces (public trên `ProductExportRequestService`, Task 6 + controller dùng):
  - `contractRemainingByLine(int $contractId, ?int $excludeRequestId = null): array` — nguyên thân `contractProductLines` hiện tại (trả mảng dòng có `id, parent_id, …, remaining_qty`).
  - `assertContractCanExport(?Contract $contract): void` — 422 key `emplement_contract_id`, message HĐ chưa đủ điều kiện.
  - `assertContractLineQtyWithinRemaining(int $contractId, array $products, ?int $excludeRequestId): void` — 422 key `products.{i}.qty`.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class ContractSubmitTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    private function submit20(object $c, float $qty, array $extra = [])
    {
        return $this->postRequest(array_merge([
            'type' => 20, 'status' => 2, 'emplement_contract_id' => $c->id,
            'warehouse_id' => 1, 'transition_type' => 1,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => $qty]],
        ], $extra));
    }

    public function test_hd_chua_hieu_luc_bi_chan(): void
    {
        $c = $this->makeHrmContract(['status' => 1]);
        $this->submit20($c, 1)->assertStatus(422)->assertJsonFragment([
            'emplement_contract_id' => ['Hợp đồng chưa đủ điều kiện xuất hàng (chưa có hiệu lực hoặc chưa nhập thời hạn thực hiện).'],
        ]);
    }

    public function test_hd_thieu_thoi_han_thuc_hien_bi_chan(): void
    {
        $c = $this->makeHrmContract(['execution_end_date' => null]);
        $this->submit20($c, 1)->assertStatus(422)->assertJsonValidationErrors('emplement_contract_id');
    }

    public function test_vuot_con_lai_bi_chan(): void
    {
        $c = $this->makeHrmContract();
        $this->submit20($c, 11)->assertStatus(422)->assertJsonFragment([
            'products.0.qty' => ['Sản phẩm "SP test" vượt số lượng còn được xuất (10).'],
        ]);
    }

    public function test_tru_sl_phieu_khac_chua_huy(): void
    {
        $c = $this->makeHrmContract();
        $this->submit20($c, 7)->assertStatus(200);
        $this->submit20($c, 4)->assertStatus(422)->assertJsonFragment([
            'products.0.qty' => ['Sản phẩm "SP test" vượt số lượng còn được xuất (3).'],
        ]);
    }

    public function test_nhap_khong_kiem_con_lai(): void
    {
        $c = $this->makeHrmContract(['status' => 1]);
        $this->submit20($c, 99, ['status' => 3])->assertStatus(200);
    }

    public function test_gui_duyet_khi_sua_khong_tu_chan_chinh_minh(): void
    {
        $c = $this->makeHrmContract();
        $id = $this->submit20($c, 10, ['status' => 3])->json('data.id');
        $this->putRequest($id, [
            'status' => 2, 'emplement_contract_id' => $c->id, 'warehouse_id' => 1, 'transition_type' => 1,
            'products' => [['contract_product_id' => $c->child_line_id, 'qty' => 10]],
        ])->assertStatus(200);
    }
}
```

- [x] **Step 2: Chạy, xác nhận FAIL** — Expected: `hd_chua_hieu_luc`, `thieu_thoi_han`, `vuot_con_lai`, `tru_sl_phieu_khac` FAIL (200 thay vì 422).

- [x] **Step 3: Chuyển `contractProductLines` vào service + thêm 2 assert**

Service:
```php
    /**
     * Dòng hàng HĐ HRM kèm SL đã xuất (tổng tab_products các phiếu chưa hủy) và còn lại.
     * $excludeRequestId: loại trừ chính phiếu đang sửa để không tự chặn chính mình.
     * (Chuyển nguyên từ ProductExportRequestController::contractProductLines.)
     */
    public function contractRemainingByLine(int $contractId, ?int $excludeRequestId = null): array
    {
        // ← dán NGUYÊN thân contractProductLines (Controller:427-479), không đổi logic
    }

    public function assertContractCanExport(?Contract $contract): void
    {
        if (!$contract || !$contract->can_export) {
            throw ValidationException::withMessages(['emplement_contract_id' => [
                'Hợp đồng chưa đủ điều kiện xuất hàng (chưa có hiệu lực hoặc chưa nhập thời hạn thực hiện).',
            ]]);
        }
    }

    /** Khuôn assertFirmContractLineQtyWithinRemaining (:1076) cho HĐ HRM. */
    public function assertContractLineQtyWithinRemaining(int $contractId, array $products, ?int $excludeRequestId): void
    {
        $lines = collect($this->contractRemainingByLine($contractId, $excludeRequestId))->keyBy('id');
        foreach (array_values($products) as $i => $p) {
            $lineId = (int) ($p['contract_product_id'] ?? 0);
            $qty = (float) ($p['qty'] ?? 0);
            if ($lineId <= 0 || $qty <= 0) {
                continue;
            }
            $line = $lines->get($lineId);
            $remaining = $line ? (float) $line['remaining_qty'] : 0.0;
            if ($qty > $remaining) {
                $name = $line['name'] ?? '';
                $shown = rtrim(rtrim(number_format($remaining, 2, '.', ''), '0'), '.');
                throw ValidationException::withMessages(["products.$i.qty" => [
                    "Sản phẩm \"{$name}\" vượt số lượng còn được xuất ({$shown}).",
                ]]);
            }
        }
    }
```
Controller: `contractProductLines(...)` → `return $this->service->contractRemainingByLine($contractId, $excludeRequestId);` (đọc tên thuộc tính service đang inject trong controller; mọi chỗ gọi cũ giữ nguyên).

Gọi assert khi `status === 2`:
- `createFromContract`: TRƯỚC khi tạo phiếu → `$this->assertContractCanExport($contract); $this->assertContractLineQtyWithinRemaining($contract->id, $data['products'] ?? [], null);`
- `updateFromRequest` nhánh HĐ HRM: TRƯỚC `deleteLines` → cùng 2 lời gọi, `$excludeRequestId = (int) $req->id`.
- `createFromRequest` khi 20/21 gửi duyệt mà thiếu HĐ: rule `required` (Task 1) đã chặn — không cần thêm.

- [x] **Step 4: Chạy, xác nhận PASS** — `php artisan test --filter=ProductExportRequest` (cả thư mục) → PASS hết.

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): 20/21 gửi duyệt kiểm HĐ đủ điều kiện + SL còn lại"`

---

## Task 6: Endpoint `GET hrm-contracts` (popup chọn HĐ 20/21)

**Files:**
- Create: `hrm-api/Modules/Assign/Services/ProductExportRequestPickerService.php`
- Modify: Controller (action `hrmContracts`), `Modules/Assign/Routes/api.php` (sau dòng `emplement-contracts`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/HrmContractPickerTest.php`

**Interfaces:**
- Produces: `GET /api/assign/product-export-requests/hrm-contracts?type=20|21&search=&customer_id=&page=&per_page=` → `{data: [{id, code, customer_id, customer_name, sign_date, effective_date, execution_end_date, remaining_lines}], meta: {current_page, last_page, total, per_page}}`. Chỉ HĐ: `status=6`, `effective_date`, `execution_deadline_days`, `execution_end_date` NOT NULL, `company_id` = công ty người đăng nhập, và ≥1 dòng đúng loại (20: `parent_id` NOT NULL; 21: `parent_id` NULL) có `qty_needed > SL đã xuất (phiếu chưa hủy)`.
- `ProductExportRequestPickerService::hrmContracts(int $type, array $filters, int $companyId): LengthAwarePaginator`.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class HrmContractPickerTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    private function ids(int $type, string $search): array
    {
        return collect($this->getJson("/api/assign/product-export-requests/hrm-contracts?type={$type}&search={$search}&per_page=50")
            ->assertStatus(200)->json('data'))->pluck('id')->map(fn ($v) => (int) $v)->all();
    }

    public function test_chi_hien_hd_xuat_duoc(): void
    {
        $this->loginAs13();
        $ok = $this->makeHrmContract(['code' => 'HDPICK-OK']);
        $this->makeHrmContract(['code' => 'HDPICK-NOEFF', 'status' => 1]);
        $this->makeHrmContract(['code' => 'HDPICK-NOEND', 'execution_end_date' => null]);
        $this->makeHrmContract(['code' => 'HDPICK-OTHERCO', 'company_id' => 999999]);

        $this->assertSame([$ok->id], $this->ids(20, 'HDPICK'));
    }

    public function test_het_con_lai_dung_loai_thi_an(): void
    {
        $this->loginAs13();
        // Dòng con đã xuất hết (qty_needed 0) → ẩn ở loại 20, vẫn hiện ở loại 21 (dòng cha còn 10).
        $c = $this->makeHrmContract(['code' => 'HDPICK-CHILD0'], [[], ['qty_needed' => 0]]);

        $this->assertSame([], $this->ids(20, 'HDPICK-CHILD0'));
        $this->assertSame([$c->id], $this->ids(21, 'HDPICK-CHILD0'));
    }

    public function test_thieu_type_bi_422(): void
    {
        $this->loginAs13();
        $this->getJson('/api/assign/product-export-requests/hrm-contracts')->assertStatus(422);
    }
}
```

- [x] **Step 2: Chạy, xác nhận FAIL** — Expected: 404 (route chưa có).

- [x] **Step 3: Viết picker service + action + route**

```php
<?php

namespace Modules\Assign\Services;

use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Contract\Contract;
use Modules\Assign\Entities\Warehouse\ProductExportRequest;

/**
 * Query cho các popup chọn nguồn của YCXH (HĐ HRM 20/21, HĐ chi phí 99, ĐVT, tồn).
 * Tách khỏi ProductExportRequestService để service chính không phình thêm.
 */
class ProductExportRequestPickerService
{
    /** Mirror Contract::getCanExportAttribute + còn ≥1 dòng đúng loại chưa xuất hết. */
    public function hrmContracts(int $type, array $filters, int $companyId): LengthAwarePaginator
    {
        $exported = DB::table('product_export_request_tab_products as tp')
            ->join('product_export_requests as r', 'r.id', '=', 'tp.product_export_request_id')
            ->where('r.status', '!=', ProductExportRequest::STATUS_DA_HUY_PHIEU)
            ->whereNotNull('tp.contract_product_id')
            ->groupBy('tp.contract_product_id')
            ->select('tp.contract_product_id', DB::raw('SUM(tp.qty) as qty'));

        $remainingLines = DB::table('hrm_contract_product_prices as cpp')
            ->leftJoinSub($exported, 'ex', 'ex.contract_product_id', '=', 'cpp.id')
            ->whereColumn('cpp.contract_id', 'c.id')
            ->whereRaw('cpp.qty_needed > COALESCE(ex.qty, 0)');
        $type === ProductExportRequest::XUAT_SAN_XUAT_HOP_DONG
            ? $remainingLines->whereNotNull('cpp.parent_id')
            : $remainingLines->whereNull('cpp.parent_id');

        $q = DB::table('hrm_contracts as c')
            ->where('c.company_id', $companyId)
            ->where('c.status', Contract::STATUS_CO_HIEU_LUC)
            ->whereNotNull('c.effective_date')
            ->whereNotNull('c.execution_deadline_days')
            ->whereNotNull('c.execution_end_date')
            ->whereExists($remainingLines->select(DB::raw(1)))
            ->when(!empty($filters['customer_id']), fn ($q) => $q->where('c.customer_id', (int) $filters['customer_id']))
            ->when(!empty($filters['search']), function ($q) use ($filters) {
                $s = '%' . $filters['search'] . '%';
                $q->where(fn ($w) => $w->where('c.code', 'like', $s)->orWhere('c.customer_name', 'like', $s));
            })
            ->orderByDesc('c.id')
            ->select('c.id', 'c.code', 'c.customer_id', 'c.customer_name', 'c.sign_date',
                'c.effective_date', 'c.execution_end_date');

        return $q->paginate((int) ($filters['per_page'] ?? 20), ['*'], 'page', (int) ($filters['page'] ?? 1));
    }
}
```
> Hằng trạng thái hiệu lực trên `Contract` là `STATUS_CO_HIEU_LUC` (`Contract.php:56` dùng `self::STATUS_CO_HIEU_LUC`). Kiểm `execution_deadline_days` = 0 có bị coi là "chưa nhập" ở `can_export` (truthy) → thêm `->where('c.execution_deadline_days', '>', 0)` cho khớp.

Controller:
```php
    /** Loại 20/21: HĐ HRM đủ điều kiện xuất cho popup chọn HĐ (spec §5.2). Route tĩnh, TRƯỚC /{id}. */
    public function hrmContracts(Request $request)
    {
        $request->validate([
            'type' => 'required|in:20,21',
            'customer_id' => 'nullable|integer',
            'search' => 'nullable|string|max:100',
            'page' => 'nullable|integer|min:1',
            'per_page' => 'nullable|integer|min:1|max:100',
        ]);
        $companyId = (int) (auth()->user()->info->company_id ?? 0);
        $page = app(ProductExportRequestPickerService::class)
            ->hrmContracts((int) $request->type, $request->only('search', 'customer_id', 'page', 'per_page'), $companyId);

        return $this->paginatedResponse($page);
    }
```
Dùng đúng hàm/format phân trang mà `firmContracts()` (`Controller:552`) đang trả — đọc nó và bắt chước (nếu không có helper `paginatedResponse`, trả `['data' => $page->items(), 'meta' => [...]]` y như `firmContracts`), để `utils/pickerPagination.js` ăn được.

Route (sau dòng `emplement-contracts`):
```php
        // Loại 20/21: HĐ HRM đủ điều kiện xuất (popup chọn HĐ) — route TĨNH, TRƯỚC /{id}
        Route::get('/hrm-contracts', [ProductExportRequestController::class, 'hrmContracts']);
```

- [x] **Step 4: Chạy, xác nhận PASS** — `php artisan test --filter=HrmContractPickerTest` → PASS 3/3.

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): endpoint HĐ HRM đủ điều kiện xuất"`

---

## Task 7: Endpoint tồn kho + ĐVT cho bảng nhập tay

**Files:**
- Modify: `ProductExportRequestPickerService.php` (`stockOfProducts`, `productUnits`), Controller (2 action), Routes
- Test: `hrm-api/tests/Feature/ProductExportRequest/StockAndUnitTest.php`

**Interfaces:**
- Produces:
  - `POST /api/assign/product-export-requests/stock-of-products` body `{warehouse_id (required), products: [{product_id, unit_id}], product_export_request_id?, customer_id?}` → `{data: {"<product_id>-<unit_id>": {available_export_qty, in_stock}}}`.
  - `GET /api/assign/product-export-requests/product-units?product_ids[]=` → `{data: {"<product_id>": [{unit_id, unit_name, coefficient}]}}`.
- Gọi `StockService::getLineStocks(int $warehouseId, array $lines, array $ctx)` **không sửa**: kết quả key theo `product_id` → nhóm request theo `unit_id`, gọi 1 lần/nhóm, ghép key `product_id-unit_id`. `ctx` truyền `except_id => null` (R4), `customer_id`, `product_export_request_id` nếu có.

- [x] **Step 1: Đọc chữ ký thật** — `grep -n "function getLineStocks" -A30 hrm-api/app/Services/StockService.php` (hoặc nơi khai báo thật: `grep -rn "function getLineStocks" hrm-api/app hrm-api/Modules`). Ghi lại khoá dòng (`product_id`, `unit_id`?) và khoá `ctx` mà hàm đọc. Nếu khác plan → ghi Ruling, giữ nguyên hợp đồng response ở trên.

- [x] **Step 2: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class StockAndUnitTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    public function test_ton_theo_tung_don_vi_tinh(): void
    {
        $row = DB::table('product_units')->select('product_id')->groupBy('product_id')
            ->havingRaw('COUNT(*) >= 2')->first();
        if (!$row) {
            $this->markTestSkipped('DB dev không có SP nhiều ĐVT');
        }
        $units = DB::table('product_units')->where('product_id', $row->product_id)->limit(2)->pluck('unit_id')->all();

        $data = $this->postJson('/api/assign/product-export-requests/stock-of-products', [
            'warehouse_id' => 1,
            'products' => [
                ['product_id' => $row->product_id, 'unit_id' => $units[0]],
                ['product_id' => $row->product_id, 'unit_id' => $units[1]],
            ],
        ])->assertStatus(200)->json('data');

        $this->assertArrayHasKey($row->product_id . '-' . $units[0], $data);
        $this->assertArrayHasKey($row->product_id . '-' . $units[1], $data);
        $this->assertArrayHasKey('available_export_qty', $data[$row->product_id . '-' . $units[0]]);
    }

    public function test_thieu_kho_bi_422(): void
    {
        $this->postJson('/api/assign/product-export-requests/stock-of-products', ['products' => []])
            ->assertStatus(422)->assertJsonValidationErrors('warehouse_id');
    }

    public function test_don_vi_tinh_theo_san_pham(): void
    {
        $pu = $this->anyProductUnit();
        $data = $this->getJson('/api/assign/product-export-requests/product-units?product_ids[]=' . $pu->product_id)
            ->assertStatus(200)->json('data');

        $this->assertContains((int) $pu->unit_id, collect($data[$pu->product_id])->pluck('unit_id')->map(fn ($v) => (int) $v)->all());
    }
}
```

- [x] **Step 3: Chạy, xác nhận FAIL** — Expected: 404.

- [x] **Step 4: Viết service + action + route**

```php
    /** Tồn theo (product_id, unit_id). getLineStocks key theo product_id → gọi riêng mỗi nhóm unit_id. */
    public function stockOfProducts(int $warehouseId, array $products, array $ctx): array
    {
        $out = [];
        $byUnit = collect($products)
            ->filter(fn ($p) => !empty($p['product_id']) && !empty($p['unit_id']))
            ->groupBy(fn ($p) => (int) $p['unit_id']);
        foreach ($byUnit as $unitId => $lines) {
            $stocks = app(StockService::class)->getLineStocks($warehouseId, $lines->values()->all(), array_merge($ctx, ['except_id' => null]));
            foreach ($lines as $p) {
                $s = $stocks[(int) $p['product_id']] ?? [];
                $out[(int) $p['product_id'] . '-' . (int) $unitId] = [
                    'available_export_qty' => (float) ($s['available_export_qty'] ?? 0),
                    'in_stock' => (float) ($s['in_stock'] ?? 0),
                ];
            }
        }
        return $out;
    }

    public function productUnits(array $productIds): array
    {
        return DB::table('product_units as pu')
            ->join('units as u', 'u.id', '=', 'pu.unit_id')
            ->whereIn('pu.product_id', array_map('intval', $productIds))
            ->orderBy('pu.id')
            ->get(['pu.product_id', 'pu.unit_id', 'u.name as unit_name', 'pu.coefficient'])
            ->groupBy('product_id')
            ->map(fn ($rows) => $rows->map(fn ($r) => [
                'unit_id' => (int) $r->unit_id, 'unit_name' => $r->unit_name, 'coefficient' => (float) $r->coefficient,
            ])->values())
            ->toArray();
    }
```
> Tên cột hệ số trên `product_units` có thể là `coefficient` / `conversion_rate` — kiểm `SHOW COLUMNS FROM product_units` trước, sửa cho khớp. `use` đúng namespace `StockService` tìm ở Step 1.

Controller:
```php
    public function stockOfProducts(Request $request)
    {
        $request->validate([
            'warehouse_id' => 'required|integer|exists:warehouses,id',
            'products' => 'nullable|array|max:500',
            'products.*.product_id' => 'required|integer',
            'products.*.unit_id' => 'required|integer',
            'product_export_request_id' => 'nullable|integer',
            'customer_id' => 'nullable|integer',
        ]);
        return $this->responseSuccess(app(ProductExportRequestPickerService::class)->stockOfProducts(
            (int) $request->warehouse_id, $request->input('products', []),
            array_filter($request->only('product_export_request_id', 'customer_id'))
        ));
    }

    public function productUnits(Request $request)
    {
        $request->validate(['product_ids' => 'required|array|max:500', 'product_ids.*' => 'integer']);
        return $this->responseSuccess(app(ProductExportRequestPickerService::class)->productUnits($request->product_ids));
    }
```
(Dùng đúng helper response mà controller đang dùng — đọc `createData()` để bắt chước; nếu không phải `responseSuccess`, đổi cho khớp.)

Routes:
```php
        // Bảng nhập tay: tồn theo SP+ĐVT, danh sách ĐVT theo SP — route TĨNH, TRƯỚC /{id}
        Route::post('/stock-of-products', [ProductExportRequestController::class, 'stockOfProducts']);
        Route::get('/product-units', [ProductExportRequestController::class, 'productUnits']);
```

- [x] **Step 5: Chạy, xác nhận PASS** — `php artisan test --filter=StockAndUnitTest` → PASS 3/3 (ca nhiều ĐVT có thể SKIP — ghi lại).

- [ ] **Step 6: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): endpoint tồn kho + ĐVT cho bảng nhập tay"`

---

## Task 8: Loại 99 — endpoint HĐ chi phí + lưu morph

**Files:**
- Modify: `ProductExportRequestPickerService.php` (`costContracts`), Controller (action + rule), Service (`createManual`, `updateFromRequest`), Routes
- Test: `hrm-api/tests/Feature/ProductExportRequest/CostContractTest.php`

**Interfaces:**
- Produces:
  - `GET /api/assign/product-export-requests/cost-contracts?contract_type=<key>&search=&customer_id=&page=` → `{data: [{id, code, customer_name, contract_costable_type}], meta}`.
  - Bảng nhóm (hằng `ProductExportRequestPickerService::COST_CONTRACT_SOURCES`), khoá = `contract_type` FE gửi:

    | key | Nhãn | Bảng | Điều kiện | class lưu |
    |---|---|---|---|---|
    | `1`…`7` | đọc nhãn từ ERP `App\Contract` const loại HĐ | `contracts` | `type = key` | `App\Contract` |
    | `service` | HĐ dịch vụ | `service_contracts` | — | `App\Model\Sale\ServiceContract` |
    | `project` | HĐ dự án | `project_contracts` | — | `App\Model\Sale\ProjectContract` |
    | `opening` | HĐ đầu kỳ | `opening_contracts` | — | `App\Model\Accounting\OpeningContract` |
    | `hrm` | HĐ HRM | `hrm_contracts` | — | **theo Q-ERP** (8b) |

    Đọc ERP `SearchController@searchContract` (`ERP/TanPhatDev/app/Http/Controllers/Common/SearchController.php:2186`) để chép **đúng** danh sách key, tên bảng, cột `code`/`customer_name` và nhãn nhóm; bảng trên là khung, ERP là nguồn. Lệch → theo ERP, ghi Ruling.
  - Payload lưu: `contract_costable_id`, `contract_costable_type` (= class lấy từ bảng nhóm phía BE theo `contract_costable_key`, FE KHÔNG gửi class). Chỉ lưu khi `type = 99`; loại khác → `null` cả 2.

### 8a — làm ngay (nhóm ERP)

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class CostContractTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    public function test_tim_hd_ban_theo_loai(): void
    {
        $row = DB::table('contracts')->where('company_id', 1)->whereNotNull('type')->orderByDesc('id')->first();
        if (!$row) {
            $this->markTestSkipped('Không có contracts công ty 1');
        }
        $ids = collect($this->getJson('/api/assign/product-export-requests/cost-contracts?contract_type=' . $row->type . '&search=' . urlencode($row->code))
            ->assertStatus(200)->json('data'))->pluck('id')->all();
        $this->assertContains($row->id, $ids);
    }

    public function test_luu_morph_loai_99(): void
    {
        $row = DB::table('contracts')->where('company_id', 1)->orderByDesc('id')->first();
        $id = $this->postRequest(['type' => 99, 'status' => 3,
            'contract_costable_id' => $row->id, 'contract_costable_key' => (string) $row->type])->json('data.id');

        $this->assertDatabaseHas('product_export_requests', [
            'id' => $id, 'contract_costable_id' => $row->id, 'contract_costable_type' => 'App\\Contract',
        ]);
    }

    public function test_loai_khac_99_bo_qua_morph(): void
    {
        $row = DB::table('contracts')->orderByDesc('id')->first();
        $id = $this->postRequest(['type' => 18, 'status' => 3,
            'contract_costable_id' => $row->id, 'contract_costable_key' => (string) $row->type])->json('data.id');

        $this->assertDatabaseHas('product_export_requests', ['id' => $id, 'contract_costable_id' => null, 'contract_costable_type' => null]);
    }

    public function test_doi_nhom_hd_khi_sua(): void
    {
        $a = DB::table('contracts')->orderByDesc('id')->first();
        $p = DB::table('project_contracts')->orderByDesc('id')->first();
        if (!$p) {
            $this->markTestSkipped('Không có project_contracts');
        }
        $id = $this->postRequest(['type' => 99, 'status' => 3, 'contract_costable_id' => $a->id,
            'contract_costable_key' => (string) $a->type])->json('data.id');

        $this->putRequest($id, ['status' => 3, 'contract_costable_id' => $p->id, 'contract_costable_key' => 'project'])->assertStatus(200);

        $this->assertDatabaseHas('product_export_requests', [
            'id' => $id, 'contract_costable_id' => $p->id, 'contract_costable_type' => 'App\\Model\\Sale\\ProjectContract',
        ]);
    }

    public function test_key_la_bi_422(): void
    {
        $this->postRequest(['type' => 99, 'status' => 3, 'contract_costable_id' => 1, 'contract_costable_key' => 'xyz'])
            ->assertStatus(422)->assertJsonValidationErrors('contract_costable_key');
    }
}
```

- [x] **Step 2: Chạy, xác nhận FAIL** — Expected: 404 ở endpoint, cột morph null ở ca lưu.

- [x] **Step 3: Viết `COST_CONTRACT_SOURCES` + `costContracts` + `costableClassOf`**

```php
    /** Nguồn HĐ chi phí cho loại 99 — chép theo ERP SearchController@searchContract. key → [table, where, class, label]. */
    public const COST_CONTRACT_SOURCES = [
        // '1' … '7' → ['table' => 'contracts', 'type' => 1, 'class' => 'App\Contract', 'label' => '<nhãn ERP>'],
        'service' => ['table' => 'service_contracts', 'class' => 'App\Model\Sale\ServiceContract', 'label' => 'Hợp đồng dịch vụ'],
        'project' => ['table' => 'project_contracts', 'class' => 'App\Model\Sale\ProjectContract', 'label' => 'Hợp đồng dự án'],
        'opening' => ['table' => 'opening_contracts', 'class' => 'App\Model\Accounting\OpeningContract', 'label' => 'Hợp đồng đầu kỳ'],
        // 'hrm' thêm ở 8b sau khi user chọn Q-ERP
    ];

    public static function costableClassOf(?string $key): ?string
    {
        return $key !== null ? (self::COST_CONTRACT_SOURCES[$key]['class'] ?? null) : null;
    }

    /** R5: Phase 1 lọc theo công ty người đăng nhập (ERP lọc theo quyền — để Phase 5). */
    public function costContracts(string $key, array $filters, int $companyId): LengthAwarePaginator
    {
        $src = self::COST_CONTRACT_SOURCES[$key];
        return DB::table($src['table'] . ' as c')
            ->when(isset($src['type']), fn ($q) => $q->where('c.type', $src['type']))
            ->where('c.company_id', $companyId)
            ->when(!empty($filters['customer_id']), fn ($q) => $q->where('c.customer_id', (int) $filters['customer_id']))
            ->when(!empty($filters['search']), function ($q) use ($filters) {
                $s = '%' . $filters['search'] . '%';
                $q->where(fn ($w) => $w->where('c.code', 'like', $s)->orWhere('c.customer_name', 'like', $s));
            })
            ->orderByDesc('c.id')
            ->select('c.id', 'c.code', 'c.customer_name')
            ->paginate((int) ($filters['per_page'] ?? 20), ['*'], 'page', (int) ($filters['page'] ?? 1));
    }
```
Kiểm từng bảng có cột `company_id`/`customer_name`/`code` (`SHOW COLUMNS`); bảng thiếu thì chép cách ERP lấy (join `customers`) — ghi Ruling.

Controller: action `costContracts` (validate `contract_type` `required|in:` + `implode(',', array_keys(COST_CONTRACT_SOURCES))`), route `Route::get('/cost-contracts', …)` trước `/{id}`. Thêm `cost_contract_sources` (`[{key, label}]`) vào payload `createData`/`editData` cho FE dựng select nhóm.

Rule (mọi trạng thái, mọi loại — BE tự bỏ khi không phải 99):
```php
        $rules['contract_costable_id'] = 'nullable|integer|required_with:contract_costable_key';
        $rules['contract_costable_key'] = 'nullable|string|in:' . implode(',', array_keys(ProductExportRequestPickerService::COST_CONTRACT_SOURCES));
```
Gửi duyệt loại 99: theo ERP (`ProductExportRequestsController:826-829` lưu khi type 99) kiểm ERP có `required` HĐ chi phí khi gửi không — có thì thêm `required`, không thì giữ nullable.

Service — cả `createManual` (fill) và `updateFromRequest` (nhánh manual):
```php
                'contract_costable_id' => $type === 99 ? ($data['contract_costable_id'] ?? null) : null,
                'contract_costable_type' => $type === 99
                    ? ProductExportRequestPickerService::costableClassOf($data['contract_costable_key'] ?? null) : null,
```
(Kiểm 2 cột có trong `$fillable` của entity HRM; chưa có thì thêm.)

`editData`/`show`: trả `contract_costable_key` (suy ngược từ class + `contracts.type`) và `contract_costable_code` để FE hiện. Viết `costableKeyOf(?string $class, ?int $id): ?string` trong picker service.

- [x] **Step 4: Chạy, xác nhận PASS** — `php artisan test --filter=CostContractTest` → PASS (ca thiếu data SKIP).

- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): loại 99 chọn HĐ chi phí (nguồn ERP)"`

### 8b — CHỜ Q-ERP: nhóm "HĐ HRM"

- [x] **Step 6:** Sau khi user chọn: thêm `'hrm' => ['table' => 'hrm_contracts', 'class' => <A: 'App\Model\Hrm\HrmContract' | B: alias morphMap>, 'label' => 'Hợp đồng HRM']`. Test:
```php
    public function test_luu_morph_hd_hrm(): void
    {
        $c = $this->makeHrmContract();
        $id = $this->postRequest(['type' => 99, 'status' => 3, 'contract_costable_id' => $c->id, 'contract_costable_key' => 'hrm'])->json('data.id');
        $this->assertDatabaseHas('product_export_requests', [
            'id' => $id, 'contract_costable_type' => ProductExportRequestPickerService::costableClassOf('hrm'),
        ]);
    }
```
RED → thêm dòng hằng → GREEN.

---

## Task 9: ERP — đọc được morph HĐ HRM (CHỜ Q-ERP, phương án A)

**Files (A):**
- Create: `ERP/TanPhatDev/app/Model/Hrm/HrmContract.php`
- Test: kiểm tay qua tinker (ERP không có bộ test cho model này).

**Interfaces:**
- Consumes: `contract_costable_type = 'App\Model\Hrm\HrmContract'` do Task 8b ghi.
- Produces: `HrmContract::find($id)->link` → URL màn HĐ HRM; eager-load `contract_costable` ở ERP `ProductExportRequest.php:780/1147` không lỗi.

- [x] **Step 1: Chứng minh lỗi hiện tại (RED)** — ERP `.env` đọc `grep DB_ ERP/TanPhatDev/.env` trước (memory: target DB đổi theo lúc). Trong transaction tinker:
```php
DB::beginTransaction();
$r = \App\Model\Warehouse\ProductExportRequest::where('type', 99)->first();
$r->contract_costable_type = 'App\Model\Hrm\HrmContract'; $r->contract_costable_id = DB::table('hrm_contracts')->value('id'); $r->save();
\App\Model\Warehouse\ProductExportRequest::with('contract_costable')->find($r->id)->contract_costable->link;
DB::rollBack();
```
Expected: `Class "App\Model\Hrm\HrmContract" not found`.

- [x] **Step 2: Tạo model (Laravel 6/8 — không dùng cú pháp PHP 8)**

```php
<?php

namespace App\Model\Hrm;

use Illuminate\Database\Eloquent\Model;

/**
 * Hợp đồng HRM (bảng hrm_contracts, chung DB gộp). CHỈ ĐỌC từ ERP — dùng làm đích morph
 * `contract_costable` của YCXH loại 99 do HRM lập. Không ghi từ ERP.
 */
class HrmContract extends Model
{
    protected $table = 'hrm_contracts';
    protected $guarded = ['*'];

    public function getLinkAttribute()
    {
        $base = rtrim(env('HRM_URL', ''), '/');
        return '<a target="_blank" href="' . $base . '/assign/contracts/' . $this->id . '">' . e($this->code) . '</a>';
    }
}
```
> Đọc `getLinkAttribute` của `App\Model\Sale\ProjectContract` (ERP) để chép đúng định dạng `link` (thẻ `<a>` hay URL thuần) — ERP `:1151` đọc `->link` theo cách nào thì trả đúng cách đó. Tên biến env URL HRM: grep `HRM_` trong `ERP/TanPhatDev/.env.example`/`config/` (memory có `HRM_API_BASE_URL` — đó là API, cần URL màn hình; không có → hỏi user).

- [x] **Step 3: Chạy lại Step 1 (GREEN)** — Expected: in ra link, không exception.
- [x] **Step 4: Kiểm màn ERP** — mở chi tiết + danh sách YCXH ERP của phiếu loại 99 do HRM lập (Playwright hoặc trình duyệt) → cột HĐ hiện mã HĐ HRM, không trắng màn.
- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C ERP/TanPhatDev add app/Model/Hrm/HrmContract.php && git -C ERP/TanPhatDev commit -m "feat(ycxh): model đọc HĐ HRM cho morph contract_costable"`

---

## Task 10: Loại 3 — ngày trả ≤ hôm nay + `max_borrow_date`

**Files:**
- Modify: Service (`assertReturnDateWithinLimit` + gọi ở create/update), Controller (`createData`, `editData`)
- Test: `hrm-api/tests/Feature/ProductExportRequest/BorrowReturnDateTest.php`

**Interfaces:**
- Produces: `createData`/`editData` thêm `max_borrow_date` (int, số ngày; null nếu chưa cấu hình). Task 15 FE đọc khoá này.
- `assertReturnDateWithinLimit(?string $returnDate): void` — khuôn `BorrowExtendRequestService.php:300`: `$days = (int) ((CompanyConfig::value('max_borrow_date') ?? 0) ?: 0)`; `$days <= 0` → bỏ qua; `return_date > today + days` → 422 key `return_date`.

- [x] **Step 1: Viết test fail**

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use App\Support\CompanyConfig;
use Carbon\Carbon;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class BorrowReturnDateTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    private function submit3(string $returnDate)
    {
        $pu = $this->anyProductUnit();
        return $this->postRequest([
            'type' => 3, 'status' => 2, 'warehouse_id' => 1, 'transition_type' => 1,
            'expected_borrow_date' => Carbon::today()->toDateString(), 'return_date' => $returnDate,
            'products' => [['product_id' => $pu->product_id, 'unit_id' => $pu->unit_id, 'qty' => 1]],
        ]);
    }

    public function test_qua_han_muc_bi_chan(): void
    {
        $this->loginAs13();
        $days = (int) (CompanyConfig::value('max_borrow_date') ?: 0);
        if ($days <= 0) {
            $this->markTestSkipped('Công ty 1 chưa cấu hình max_borrow_date');
        }
        $limit = Carbon::today()->addDays($days);
        $this->submit3($limit->copy()->addDay()->toDateString())->assertStatus(422)->assertJsonFragment([
            'return_date' => ['Ngày trả không được quá ' . $limit->format('d/m/Y') . " (tối đa {$days} ngày)."],
        ]);
    }

    public function test_dung_han_muc_qua(): void
    {
        $this->loginAs13();
        $days = (int) (CompanyConfig::value('max_borrow_date') ?: 0);
        if ($days <= 0) {
            $this->markTestSkipped('Công ty 1 chưa cấu hình max_borrow_date');
        }
        $this->submit3(Carbon::today()->addDays($days)->toDateString())->assertStatus(200);
    }

    public function test_create_data_tra_max_borrow_date(): void
    {
        $this->loginAs13();
        $this->getJson('/api/assign/product-export-requests/create-data?type=3')
            ->assertStatus(200)->assertJsonStructure(['data' => ['max_borrow_date']]);
    }
}
```
> Đọc `createData()` (`Controller:345`) để biết tham số query và lớp bọc `data` — sửa test cho khớp, ghi Ruling. Nếu công ty 1 chưa cấu hình, chạy lại với cấu hình tạm trong transaction (`DB::table('configs')->where('company_id',1)->update(['max_borrow_date'=>30])` — đọc tên cột thật ở `CompanyConfig`) để 2 ca đầu không SKIP.

- [x] **Step 2: Chạy, xác nhận FAIL.**

- [x] **Step 3: Viết code**

```php
    /** Loại 3: ngày trả ≤ hôm nay + max_borrow_date (cấu hình công ty). Khuôn BorrowExtendRequestService:300. */
    private function assertReturnDateWithinLimit(?string $returnDate): void
    {
        $days = (int) ((CompanyConfig::value('max_borrow_date') ?? 0) ?: 0);
        if ($days <= 0 || !$returnDate) {
            return;
        }
        $limit = Carbon::today()->addDays($days);
        if (Carbon::parse($returnDate)->startOfDay()->gt($limit)) {
            throw ValidationException::withMessages(['return_date' => [
                'Ngày trả không được quá ' . $limit->format('d/m/Y') . " (tối đa {$days} ngày).",
            ]]);
        }
    }
```
Gọi khi `type === 3 && status === 2`: trong `createManual` trước `$req->save()` và trong `updateFromRequest` nhánh manual trước `$req->save()`.
Controller `createData` + `editData`: thêm `'max_borrow_date' => (int) ((CompanyConfig::value('max_borrow_date') ?? 0) ?: 0) ?: null`.

- [x] **Step 4: Chạy, xác nhận PASS** — rồi chạy cả thư mục `--filter=ProductExportRequest`.
- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-api commit -am "feat(ycxh): loại 3 giới hạn ngày trả theo max_borrow_date"`

---

## Task 11: FE `SourcePicker.vue` — chọn/đổi nguồn ở màn Sửa nháp

**Files:**
- Create: `hrm-client/pages/finance/product-export-requests/components/SourcePicker.vue`
- Modify: `ProductExportRequestForm.vue` — khối header nguồn (`:31-53` 20/21, `:57` 14, `:85` 19, `:111/125` 7), modal `:615-660` (bỏ `&& !isEdit`)
- Create: `HRM/e2e/pages/ProductExportRequestPage.ts`, `HRM/e2e/tests/product-export-requests/source-change.spec.ts`

**Interfaces:**
- Consumes: BE Task 1/4 (PUT nhận nguồn khi nháp), Task 6 (`hrm-contracts`).
- Produces: `<SourcePicker :type="form.type" :value="sourceValue" :has-lines="hasLines" :disabled="!canChangeSource" @change="onSourceChange" />`
  - `sourceValue`: `{id, code, kind}` (`kind` = `'hrm'|'firm'|'wr'|'transfer'`; loại 7 `id` là mảng id phiếu chuyển).
  - `@change(payload)` chỉ phát SAU khi user xác nhận (hoặc khi chưa có dòng). Form nghe `onSourceChange(payload)`: gán `this.unsavedLastActionAt = Date.now()`, ghi id nguồn vào form, gọi lại hàm nạp dòng hiện có (20/21: `contract_lines` từ `create-data`; 14: firm lines; 7: transfer products; 19: giữ dòng nhập tay — **19 đổi HĐ KHÔNG xoá dòng** vì dòng nhập tay không phụ thuộc HĐ, khớp ERP).
  - `canChangeSource` = `!isEdit || form.status === 3`.
  - SourcePicker tự mở modal tương ứng loại (dùng lại các modal đang có trong Form; 20/21 dùng `HrmContractSearchModal` của Task 12).

- [x] **Step 1: Viết e2e fail**

`HRM/e2e/pages/ProductExportRequestPage.ts`:
```ts
import { Page, expect } from '@playwright/test';

export class ProductExportRequestPage {
  constructor(private readonly page: Page) {}

  async gotoCreate() {
    await this.page.goto('/finance/product-export-requests/add', { waitUntil: 'domcontentloaded' });
    await expect(this.page.getByText('Loại', { exact: true }).first()).toBeVisible({ timeout: 20000 });
  }

  async gotoEdit(id: number) {
    await this.page.goto(`/finance/product-export-requests/${id}/edit`, { waitUntil: 'domcontentloaded' });
    await expect(this.page.getByRole('button', { name: 'Lưu nháp' })).toBeVisible({ timeout: 20000 });
  }

  async chooseType(label: string) {
    await this.page.locator('[data-test="ycxh-type"]').click();
    await this.page.getByRole('option', { name: label }).click();
  }

  async saveDraft(): Promise<number> {
    const resp = this.page.waitForResponse((r) => /\/assign\/product-export-requests(\/\d+)?$/.test(r.url()) && ['POST', 'PUT'].includes(r.request().method()));
    await this.page.getByRole('button', { name: 'Lưu nháp' }).click();
    const r = await resp;
    expect(r.status()).toBe(200);
    return (await r.json()).data?.id;
  }

  async openSourcePicker() {
    await this.page.locator('[data-test="ycxh-source-picker"]').click();
    await expect(this.page.locator('.modal.show')).toBeVisible();
  }

  async pickFirstSourceRow() {
    await this.page.locator('.modal.show tbody tr').first().click();
    await this.page.locator('.modal.show').getByRole('button', { name: /Chọn|Xác nhận/ }).click();
  }
}
```
> Đọc route trang tạo/sửa thật (`ls hrm-client/pages/finance/product-export-requests`) và nhãn nút thật ở footer (`ProductExportRequestForm.vue:608-612`); thêm `data-test` vào select Loại và nút chọn nguồn ở Step 3.

`HRM/e2e/tests/product-export-requests/source-change.spec.ts`:
```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

test.describe('YCXH — chọn/đổi nguồn khi sửa nháp', () => {
  test('nháp 21 chưa có HĐ → màn Sửa chọn được HĐ, nạp dòng', async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType('Xuất bán hợp đồng');
    const id = await p.saveDraft();

    await p.gotoEdit(id);
    await p.openSourcePicker();
    await p.pickFirstSourceRow();
    await expect(page.locator('[data-test="ycxh-lines"] tbody tr').first()).toBeVisible();
  });

  test('đổi HĐ khi đã có dòng → hỏi xác nhận; Hủy thì giữ nguyên', async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType('Xuất bán hợp đồng');
    await p.openSourcePicker();
    await p.pickFirstSourceRow();
    const id = await p.saveDraft();

    await p.gotoEdit(id);
    const before = await page.locator('[data-test="ycxh-source-code"]').innerText();
    await p.openSourcePicker();
    await page.locator('.modal.show tbody tr').nth(1).click();
    await page.locator('.modal.show').getByRole('button', { name: /Chọn|Xác nhận/ }).click();
    await expect(page.getByText('Đổi nguồn sẽ thay toàn bộ danh sách hàng hoá. Tiếp tục?')).toBeVisible();
    await page.getByRole('button', { name: /Hủy|Không/ }).click();
    await expect(page.locator('[data-test="ycxh-source-code"]')).toHaveText(before);
  });
});
```
> Nhãn loại 21 lấy từ `getDropdownTypes()` thật — chạy `curl` type-options hoặc đọc `ProductExportRequest.php` để chép đúng chữ. Ca 2 cần ≥2 HĐ đủ điều kiện ở công ty của user e2e; thiếu → tạo dữ liệu bằng tinker trước khi chạy (ghi vào ledger, xoá sau).

- [x] **Step 2: Chạy, xác nhận FAIL** — `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/product-export-requests/source-change.spec.ts`. Expected: FAIL — không có nút chọn nguồn ở màn Sửa (modal `v-if … && !isEdit`).

- [x] **Step 3: Viết `SourcePicker.vue`**

```vue
<template>
  <div class="d-flex align-items-center">
    <span data-test="ycxh-source-code" class="mr-2">{{ value && value.code ? value.code : '—' }}</span>
    <b-button
      v-if="!disabled"
      data-test="ycxh-source-picker"
      size="sm"
      variant="outline-primary"
      @click="$emit('open')"
    >
      {{ value && value.id ? 'Đổi' : 'Chọn' }}
    </b-button>
  </div>
</template>

<script>
// Nút chọn/đổi nguồn của YCXH (HĐ HRM 20/21, HĐ hãng 14, HĐ bán 19, phiếu chuyển 7).
// Không tự gọi API: Form mở modal tương ứng, modal trả lựa chọn qua confirmChange().
export default {
  name: 'SourcePicker',
  props: {
    value: { type: Object, default: null },
    hasLines: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
  methods: {
    /** Gọi từ Form khi modal trả nguồn mới. Có dòng + nguồn khác → hỏi trước. */
    async confirmChange(next) {
      const same = this.value && next && String(this.value.id) === String(next.id) && this.value.kind === next.kind
      if (same) return
      if (this.hasLines) {
        const ok = await this.$confirm('Đổi nguồn sẽ thay toàn bộ danh sách hàng hoá. Tiếp tục?', {
          title: 'Đổi nguồn',
          okTitle: 'Tiếp tục',
          cancelTitle: 'Hủy',
        })
        if (!ok) return
      }
      this.$emit('change', next)
    },
  },
}
</script>
```
> Đọc chữ ký `this.$confirm` thật (grep `$confirm(` trong hrm-client, lấy 1 chỗ đang dùng) — chép đúng tham số/giá trị trả về.

Trong Form:
- Thay hiển thị mã nguồn ở 4 khối header bằng `<SourcePicker ref="sourcePicker" :value="sourceValue" :has-lines="hasLines" :disabled="!canChangeSource" @open="openSourceModal" @change="onSourceChange" />`.
- Modal `:615-660`: đổi `v-if="… && !isEdit"` → `v-if="… && canChangeSource"`; sự kiện chọn của modal (`@apply`/`@select`) gọi `this.$refs.sourcePicker.confirmChange(next)` thay vì ghi thẳng.
- Computed:
```js
    canChangeSource() {
      return !this.isEdit || Number(this.form.status) === 3
    },
    hasLines() {
      return (this.contractLines || []).some((l) => Number(l.qty) > 0) || (this.form.products || []).length > 0
    },
```
(đọc tên biến dòng thật trong `data()` `:1048-1105` và sửa cho khớp.)
- `onSourceChange(next)`:
```js
    async onSourceChange(next) {
      this.unsavedLastActionAt = Date.now()
      this.applySourceToForm(next)          // ghi emplement_contract_id / firm_contract_id / product_transfer_requests
      await this.reloadLinesFromSource()    // hàm nạp dòng đang có của từng loại, tách ra nếu đang inline
      this.unsavedLastActionAt = Date.now() // dữ liệu về sau await — đánh dấu là do user
    },
```
- Gửi lên PUT: payload sửa phải chứa field nguồn (trước đây bị bỏ khi `isEdit`) — tìm chỗ dựng payload (`onSubmitClick :2065`) và bỏ điều kiện `!isEdit`.
- Thêm `data-test="ycxh-type"` vào select Loại, `data-test="ycxh-lines"` vào bảng dòng.

- [x] **Step 4: Chạy e2e, xác nhận PASS** — cùng lệnh Step 2 → PASS 2/2.
- [x] **Step 5: Kiểm unsaved** — chọn nguồn ở màn Sửa rồi bấm Quay lại → phải hiện popup "Thông tin chưa lưu" (thêm case vào spec):
```ts
  test('chọn nguồn xong thoát → hỏi chưa lưu', async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType('Xuất bán hợp đồng');
    const id = await p.saveDraft();
    await p.gotoEdit(id);
    await p.openSourcePicker();
    await p.pickFirstSourceRow();
    await page.getByRole('button', { name: 'Quay lại' }).click();
    await expect(page.getByText('Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?')).toBeVisible();
  });
```
- [ ] **Step 6: Commit (chỉ khi user đã yêu cầu)** — `git -C HRM/hrm-client add -A pages/finance/product-export-requests && git -C HRM/hrm-client commit -m "feat(ycxh): chọn/đổi nguồn khi sửa nháp"` + e2e trong repo HRM tương ứng.

---

## Task 12: FE popup HĐ 20/21 + cột Còn lại/Tồn kho + Kho bắt buộc + Kho trên chi tiết

**Files:**
- Create: `hrm-client/pages/finance/product-export-requests/components/HrmContractSearchModal.vue`
- Modify: `ProductExportRequestForm.vue` (bảng HĐ `:314`, khối kho, `validateForm`), `pages/finance/product-export-requests/_id/index.vue`
- Create: `HRM/e2e/tests/product-export-requests/contract-20-21.spec.ts`

**Interfaces:**
- Consumes: Task 6 (`GET hrm-contracts`), Task 7 (`POST stock-of-products`), Task 5 (422 `products.{i}.qty`).
- Produces: `<HrmContractSearchModal ref="hrmContractModal" :type="form.type" :customer-id="form.customer_id" @select="(c) => $refs.sourcePicker.confirmChange({ id: c.id, code: c.code, kind: 'hrm' })" />`, method `show()`.

- [x] **Step 1: Viết e2e fail**

```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

test.describe('YCXH 20/21 — HĐ HRM', () => {
  test('popup HĐ có phân trang + tìm kiếm; bảng có Còn lại + Tồn kho; Kho có *', async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType('Xuất sản xuất hợp đồng');
    await p.openSourcePicker();
    const modal = page.locator('.modal.show');
    await expect(modal.getByPlaceholder(/Tìm/)).toBeVisible();
    await expect(modal.locator('.pagination, [data-test="picker-pagination"]')).toBeVisible();
    await p.pickFirstSourceRow();

    const head = page.locator('[data-test="ycxh-lines"] thead');
    await expect(head.getByText('Còn lại', { exact: true })).toBeVisible();
    await expect(head.getByText('Tồn kho', { exact: true })).toBeVisible();
    await expect(page.locator('label:has-text("Kho xuất")')).toContainText('*');
  });

  test('gửi duyệt vượt còn lại → lỗi tại dòng', async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType('Xuất sản xuất hợp đồng');
    await p.openSourcePicker();
    await p.pickFirstSourceRow();
    const qty = page.locator('[data-test="ycxh-lines"] tbody tr').first().locator('input[type="number"], input.qty').first();
    await qty.fill('999999');
    await page.getByRole('button', { name: /Gửi|Lưu và gửi/ }).click();
    await expect(page.getByText(/vượt số lượng còn được xuất/)).toBeVisible();
  });
});
```

- [x] **Step 2: Chạy, xác nhận FAIL.**

- [x] **Step 3: Viết `HrmContractSearchModal.vue`** — khuôn: mở 1 modal đang dùng `V2BaseModal` + `utils/pickerPagination.js` trong hrm-client (`grep -rln "pickerPagination" hrm-client/pages hrm-client/components | head -3`) và chép cấu trúc. Cột: Mã HĐ · Khách hàng · Ngày ký · Ngày hiệu lực · Hạn thực hiện. Tìm kiếm debounce 300ms. Gọi `GET /assign/product-export-requests/hrm-contracts` với `type`, `customer_id`, `search`, `page`, `per_page`. Chọn 1 dòng → `$emit('select', row)` + `hide()`.

```vue
<template>
  <V2BaseModal ref="modal" title="Chọn hợp đồng" size="xl">
    <b-form-input v-model="search" placeholder="Tìm theo mã HĐ, khách hàng" class="mb-2" />
    <V2BaseTableScroll>
      <table class="table table-hover">
        <thead>
          <tr><th>Mã HĐ</th><th>Khách hàng</th><th>Ngày ký</th><th>Ngày hiệu lực</th><th>Hạn thực hiện</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in rows" :key="c.id" :class="{ 'table-active': selected && selected.id === c.id }" @click="selected = c">
            <td>{{ c.code }}</td><td>{{ c.customer_name }}</td>
            <td>{{ c.sign_date | date }}</td><td>{{ c.effective_date | date }}</td><td>{{ c.execution_end_date | date }}</td>
          </tr>
          <tr v-if="!rows.length && !loading"><td colspan="5" class="text-center text-muted">Không có hợp đồng đủ điều kiện xuất</td></tr>
        </tbody>
      </table>
    </V2BaseTableScroll>
    <!-- phân trang: dùng đúng component/markup mà modal mẫu dùng cùng pickerPagination -->
    <template #footer>
      <b-button variant="secondary" @click="hide">Hủy</b-button>
      <b-button variant="primary" :disabled="!selected" @click="confirm">Chọn</b-button>
    </template>
  </V2BaseModal>
</template>
```
(Script: `data(){ return { rows: [], selected: null, search: '', loading: false, ...pagination state } }`, `watch.search` debounce 300ms → `page = 1; load()`, `show(){ this.selected = null; this.load(); this.$refs.modal.show() }`, `confirm(){ this.$emit('select', this.selected); this.hide() }`. Filter ngày: dùng filter/mixin định dạng ngày đang có trong project — grep `| date` hoặc `formatDate`.)

Thay modal HĐ cũ (`:615-660`, mở cho 20/21) bằng component này.

- [x] **Step 4: Bảng HĐ (`:314`)** — thêm 2 cột sau "SL HĐ": **Còn lại** (`line.remaining_qty`) và **Tồn kho** (`stockOf(line)`). Tồn: khi có `form.warehouse_id` + danh sách dòng → gọi `POST stock-of-products` (debounce 300ms, gọi lại khi đổi kho hoặc đổi HĐ), lưu `stocks` map `"<product_id>-<unit_id>"`. Tồn < SL yêu cầu → `<span class="text-warning">` + tooltip "Tồn kho không đủ" — không chặn. Số: `toLocaleString('en-US')`.

- [x] **Step 5: Kho bắt buộc 20/21** — label "Kho xuất" thêm `<span class="text-danger">*</span>` khi `isContractType && !form.is_export_direct`; `validateForm` (`~1963-2063`) thêm lỗi `warehouse_id` khi gửi duyệt (status 2) thiếu kho, hiển thị inline `is-invalid` + `invalid-feedback`. Lỗi 422 `products.{i}.qty` từ BE: map vào dòng `i` (đọc cách Form đang map lỗi 422 cho loại 14 và dùng y vậy).

- [x] **Step 6: Chi tiết** — `_id/index.vue`: với type 20/21 hiện trường "Kho xuất" (`warehouse.name` hoặc `warehouse_name` — xem `show()` trả gì; thiếu thì thêm vào resource `show` ở BE kèm test assertJsonPath).

- [x] **Step 7: Chạy e2e, xác nhận PASS.**
- [ ] **Step 8: Commit (chỉ khi user đã yêu cầu).**

---

## Task 13: FE `ManualLinesTable.vue` — bảng nhập tay đủ cột ERP

**Files:**
- Create: `hrm-client/pages/finance/product-export-requests/components/ManualLinesTable.vue`, `StockViewModal.vue`
- Modify: `ProductExportRequestForm.vue:499-555` (thay bảng nhập tay)
- Create: `HRM/e2e/tests/product-export-requests/manual-lines.spec.ts`

**Interfaces:**
- Consumes: Task 7 (`stock-of-products`, `product-units`); `QuotationProductSearchModal` (dùng chung, **không sửa**) emit `@apply="onProductsApply"` trả item có `id/product_id`, `name`, `code`, `model_name`, `brand_name`, `unit_id`, `unit_name`, `price`, `avatar_url` (đọc payload thật trong `onProductsApply` hiện tại).
- Produces: `<ManualLinesTable v-model="form.products" :warehouse-id="form.warehouse_id" :customer-id="form.customer_id" :request-id="form.id" :readonly="false" @add="openProductSearch" />`. Mỗi dòng: `{product_id, code, name, model_name, brand_name, unit_id, unit_name, qty, price, total_amount, avatar_url}`. Cột theo spec §5.3: **STT · Tên · Model · Mã · Thương hiệu · Tồn · Yêu cầu xuất\* · ĐVT (select) · Đơn giá · Thành tiền · Hình ảnh · +/−**.

- [x] **Step 1: Viết e2e fail**

```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

test('bảng nhập tay đủ cột ERP + Xem tồn + cảnh báo không chặn', async ({ page }) => {
  const p = new ProductExportRequestPage(page);
  await p.gotoCreate();
  await p.chooseType('Xuất hàng gửi');
  const head = page.locator('[data-test="ycxh-manual-lines"] thead');
  for (const col of ['STT', 'Tên', 'Model', 'Mã', 'Thương hiệu', 'Tồn', 'Yêu cầu xuất', 'ĐVT', 'Đơn giá', 'Thành tiền', 'Hình ảnh']) {
    await expect(head.getByText(col, { exact: false }).first()).toBeVisible();
  }
  await expect(page.getByRole('button', { name: 'Xem tồn' })).toBeVisible();

  await page.locator('[data-test="ycxh-add-product"]').click();
  await page.locator('.modal.show tbody tr').first().locator('input[type="checkbox"]').check();
  await page.locator('.modal.show').getByRole('button', { name: /Chọn|Áp dụng/ }).click();

  const row = page.locator('[data-test="ycxh-manual-lines"] tbody tr').first();
  await expect(row.locator('select')).toBeVisible();          // ĐVT là select
  await row.locator('input.qty, input[type="number"]').first().fill('999999');
  await expect(row.locator('.text-warning')).toBeVisible();   // cảnh báo tồn, không đỏ
  await expect(row.locator('.text-danger')).toHaveCount(0);
});
```

- [x] **Step 2: Chạy, xác nhận FAIL.**

- [x] **Step 3: Viết `ManualLinesTable.vue`**

```vue
<template>
  <div>
    <div class="d-flex justify-content-end mb-2">
      <b-button size="sm" variant="outline-secondary" class="mr-2" :disabled="!warehouseId || !value.length" @click="$refs.stockView.show()">Xem tồn</b-button>
      <b-button data-test="ycxh-add-product" size="sm" variant="primary" @click="$emit('add')">+ Thêm hàng</b-button>
    </div>
    <V2BaseTableScroll>
      <table data-test="ycxh-manual-lines" class="table table-bordered">
        <thead>
          <tr>
            <th>STT</th><th>Tên</th><th>Model</th><th>Mã</th><th>Thương hiệu</th><th>Tồn</th>
            <th>Yêu cầu xuất <span class="text-danger">*</span></th><th>ĐVT</th><th>Đơn giá</th>
            <th>Thành tiền</th><th>Hình ảnh</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in value" :key="row._key">
            <td>{{ i + 1 }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.model_name }}</td>
            <td>{{ row.code }}</td>
            <td>{{ row.brand_name }}</td>
            <td class="text-right">{{ stockText(row) }}</td>
            <td>
              <input v-model.number="row.qty" type="number" min="0" class="form-control form-control-sm qty" @input="touch(row)" />
              <small v-if="isShort(row)" class="text-warning">Tồn kho không đủ</small>
            </td>
            <td>
              <select v-model.number="row.unit_id" class="form-control form-control-sm" @change="onUnitChange(row)">
                <option v-for="u in unitsOf(row)" :key="u.unit_id" :value="u.unit_id">{{ u.unit_name }}</option>
              </select>
            </td>
            <td class="text-right">{{ fmt(row.price) }}</td>
            <td class="text-right">{{ fmt((Number(row.qty) || 0) * (Number(row.price) || 0)) }}</td>
            <td><img v-if="row.avatar_url" :src="row.avatar_url" class="ycxh-thumb" @click="preview(row.avatar_url)" /></td>
            <td class="text-nowrap">
              <b-button size="sm" variant="link" @click="$emit('add')">+</b-button>
              <b-button size="sm" variant="link" class="text-secondary" @click="remove(i)">−</b-button>
            </td>
          </tr>
        </tbody>
      </table>
    </V2BaseTableScroll>
    <StockViewModal ref="stockView" :rows="value" :stocks="stocks" />
    <FilePreviewModal ref="preview" />
  </div>
</template>

<script>
import StockViewModal from './StockViewModal.vue'

const BASE = '/assign/product-export-requests'

export default {
  name: 'ManualLinesTable',
  components: { StockViewModal },
  props: {
    value: { type: Array, default: () => [] },
    warehouseId: { type: [Number, String], default: null },
    customerId: { type: [Number, String], default: null },
    requestId: { type: [Number, String], default: null },
  },
  data() {
    return { stocks: {}, unitsByProduct: {}, stockTimer: null }
  },
  watch: {
    warehouseId() { this.scheduleStock() },
    value: { handler() { this.loadUnits(); this.scheduleStock() }, deep: false },
  },
  methods: {
    key(row) { return `${row.product_id}-${row.unit_id}` },
    stockOf(row) { const s = this.stocks[this.key(row)]; return s ? Number(s.available_export_qty) : null },
    stockText(row) { const s = this.stockOf(row); return s === null ? '—' : this.fmt(s) },
    isShort(row) { const s = this.stockOf(row); return s !== null && Number(row.qty) > s },
    fmt(n) { return Number(n || 0).toLocaleString('en-US') },
    unitsOf(row) {
      const list = this.unitsByProduct[row.product_id] || []
      return list.length ? list : [{ unit_id: row.unit_id, unit_name: row.unit_name }]
    },
    touch() { this.$emit('input', this.value) },
    onUnitChange(row) {
      const u = this.unitsOf(row).find((x) => x.unit_id === row.unit_id)
      row.unit_name = u ? u.unit_name : row.unit_name
      this.touch()
      this.scheduleStock()
    },
    remove(i) {
      const next = this.value.slice()
      next.splice(i, 1)
      this.$emit('input', next)
    },
    preview(url) { this.$refs.preview.show(url) },
    async loadUnits() {
      const ids = [...new Set(this.value.map((r) => r.product_id))].filter((id) => !this.unitsByProduct[id])
      if (!ids.length) return
      const { data } = await this.$axios.get(`${BASE}/product-units`, { params: { product_ids: ids } })
      this.unitsByProduct = { ...this.unitsByProduct, ...(data.data || data) }
    },
    scheduleStock() {
      clearTimeout(this.stockTimer)
      this.stockTimer = setTimeout(this.loadStock, 300)
    },
    async loadStock() {
      if (!this.warehouseId || !this.value.length) { this.stocks = {}; return }
      const { data } = await this.$axios.post(`${BASE}/stock-of-products`, {
        warehouse_id: this.warehouseId,
        products: this.value.map((r) => ({ product_id: r.product_id, unit_id: r.unit_id })),
        product_export_request_id: this.requestId || undefined,
        customer_id: this.customerId || undefined,
      })
      this.stocks = data.data || data
    },
  },
}
</script>
```
> Kiểm lại: cách project gọi API (`this.$axios` hay `this.$store.dispatch('apiGetMethod')`) — grep trong Form và dùng cùng kiểu; cách gọi `FilePreviewModal` (tên method mở, đã đăng ký global chưa); quy ước `params` mảng của axios (`product_ids[]`) — nếu BE nhận sai, thêm `paramsSerializer` như chỗ khác trong project. `_key` cho `:key`: gán khi `onProductsApply` (`Date.now() + i`).

`StockViewModal.vue`: `V2BaseModal` liệt kê Tên · Mã · ĐVT · Tồn khả dụng · Yêu cầu xuất cho mọi dòng từ `rows` + `stocks` (props), không gọi API.

Form: thay bảng `:499-555` bằng `<ManualLinesTable v-model="form.products" …/>`; `onProductsApply` map item → dòng (gồm `avatar_url`, `unit_id`, `unit_name`, `_key`) rồi gán `this.unsavedLastActionAt = Date.now()` trước khi push.

- [x] **Step 4: Chạy e2e, xác nhận PASS.**
- [x] **Step 5: Kiểm hồi quy** — tạo nháp loại 12, 18, 6 có dòng → Sửa → dòng nạp lại đúng ĐVT/SL (editData trả đủ `unit_id`, `avatar_url`; thiếu `avatar_url` thì bổ sung ở `editData` BE kèm assert test).
- [ ] **Step 6: Commit (chỉ khi user đã yêu cầu).**

---

## Task 14: FE `ContractCostModal.vue` + hiển thị loại 99

**Files:**
- Create: `hrm-client/pages/finance/product-export-requests/components/ContractCostModal.vue`
- Modify: `ProductExportRequestForm.vue` (khối loại 99), `_id/index.vue`
- Create: `HRM/e2e/tests/product-export-requests/type-99.spec.ts`

**Interfaces:**
- Consumes: Task 8 (`GET cost-contracts`, `cost_contract_sources` trong `createData`, lưu `contract_costable_id` + `contract_costable_key`; `editData`/`show` trả `contract_costable_key`, `contract_costable_code`).
- Produces: `<ContractCostModal ref="costModal" :sources="costContractSources" :customer-id="form.customer_id" @select="onCostContractSelect" />` — `@select({ id, code, key })`. Form ghi `form.contract_costable_id`, `form.contract_costable_key`, `costContractCode`; gán `unsavedLastActionAt` trước khi ghi.

- [x] **Step 1: Viết e2e fail**

```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

test('loại 99: chọn nhóm HĐ → tìm → chọn → lưu nháp → mở lại thấy mã HĐ', async ({ page }) => {
  const p = new ProductExportRequestPage(page);
  await p.gotoCreate();
  await p.chooseType('Ghi nhận chi phí hợp đồng');
  await page.locator('[data-test="ycxh-cost-contract"]').click();
  const modal = page.locator('.modal.show');
  await modal.locator('select').first().selectOption({ index: 1 });
  await modal.locator('tbody tr').first().click();
  const code = (await modal.locator('tbody tr').first().locator('td').first().innerText()).trim();
  await modal.getByRole('button', { name: 'Chọn' }).click();
  const id = await p.saveDraft();

  await page.goto(`/finance/product-export-requests/${id}`);
  await expect(page.getByText(code)).toBeVisible();
});
```

- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Viết `ContractCostModal.vue`** — cùng khung `HrmContractSearchModal` (Task 12 Step 3: `V2BaseModal` + `pickerPagination` + tìm kiếm debounce 300ms) thêm 1 `<select>` "Loại hợp đồng" ở đầu (options = `sources` `{key, label}`), đổi nhóm → reset trang + tải lại; gọi `GET cost-contracts` với `contract_type=key`. Cột: Mã HĐ · Khách hàng. Chọn → `$emit('select', { id, code, key })`.
- [x] **Step 4: Form + chi tiết** — khối loại 99 hiện ô chỉ đọc "Hợp đồng chi phí" (`data-test="ycxh-cost-contract"`, click mở modal, có nút × xoá chọn). Payload gửi `contract_costable_id`, `contract_costable_key` chỉ khi type 99. Chi tiết hiện "Hợp đồng chi phí: <mã>" khi type 99.
- [x] **Step 5: Chạy e2e, xác nhận PASS.**
- [ ] **Step 6: Commit (chỉ khi user đã yêu cầu).**

---

## Task 15: FE loại 3 + `validateForm` nháp chỉ cần Loại

**Files:**
- Modify: `ProductExportRequestForm.vue` (`validateForm ~1963-2063`, khối ngày loại 3)
- Create: `HRM/e2e/tests/product-export-requests/draft.spec.ts`, `type-3.spec.ts`

**Interfaces:**
- Consumes: Task 10 (`max_borrow_date` trong `createData`/`editData`, 422 `return_date`), Task 1 (nháp chỉ cần `type`).

- [x] **Step 1: Viết e2e fail**

`draft.spec.ts`:
```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

const TYPES = ['Xuất bán hàng', 'Xuất mượn', 'Điều chuyển kho nội bộ', 'Điều chuyển kho chi nhánh', 'Xuất hàng gửi',
  'Xuất thực hiện hợp đồng', 'Ghi nhận chi phí hợp đồng', 'Xuất sản xuất hợp đồng', 'Xuất bán hợp đồng'];

for (const label of TYPES) {
  test(`lưu nháp chỉ chọn Loại: ${label}`, async ({ page }) => {
    const p = new ProductExportRequestPage(page);
    await p.gotoCreate();
    await p.chooseType(label);
    const id = await p.saveDraft();
    expect(id).toBeGreaterThan(0);
    await expect(page.locator('.is-invalid')).toHaveCount(0);
  });
}
```
> Chép nhãn loại NGUYÊN VĂN từ `getDropdownTypes()` (curl `type-options`) — mảng trên là nhãn dự kiến, sửa cho khớp. Thêm loại 18 với nhãn thật.

`type-3.spec.ts`:
```ts
import { test, expect } from '@playwright/test';
import { ProductExportRequestPage } from '../../pages/ProductExportRequestPage';

test('loại 3: ngày trả vượt hạn mức → lỗi inline tại Ngày trả', async ({ page }) => {
  const p = new ProductExportRequestPage(page);
  await p.gotoCreate();
  await p.chooseType('Xuất mượn');
  const far = new Date(); far.setFullYear(far.getFullYear() + 5);
  await page.locator('[data-test="ycxh-return-date"] input').fill(far.toISOString().slice(0, 10));
  await page.getByRole('button', { name: /Gửi|Lưu và gửi/ }).click();
  await expect(page.locator('[data-test="ycxh-return-date"]').getByText(/Ngày trả không được quá/)).toBeVisible();
});
```
> Datepicker của project có thể không nhận `fill` — đọc component ngày đang dùng và dùng đúng cách nhập (vd gõ `dd/mm/yyyy`).

- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Sửa `validateForm`**

```js
    validateForm(status) {
      this.errors = {}
      if (!this.form.type) this.errors.type = ['Vui lòng chọn Loại']
      // Lưu nháp (status 3): chỉ cần Loại (spec §5.1) — mọi kiểm khác chỉ chạy khi gửi duyệt.
      if (Number(status) === 3) return Object.keys(this.errors).length === 0
      // … khối kiểm gửi duyệt hiện có giữ nguyên …
      if (Number(this.form.type) === 3 && this.maxBorrowDate && this.form.return_date) {
        const limit = this.$moment().startOf('day').add(this.maxBorrowDate, 'days')
        if (this.$moment(this.form.return_date).isAfter(limit)) {
          this.errors.return_date = [`Ngày trả không được quá ${limit.format('DD/MM/YYYY')} (tối đa ${this.maxBorrowDate} ngày).`]
        }
      }
      return Object.keys(this.errors).length === 0
    },
```
Đọc chữ ký `validateForm` + `onSubmitClick(status)` thật (`:2065`) và cách Form lưu lỗi (`errors` / toast) — Global Constraints Q4: giữ cơ chế thủ công + toast hiện tại, chỉ thêm inline `is-invalid` cho `return_date`, `warehouse_id`. `maxBorrowDate` nạp từ `createData`/`editData` (`max_borrow_date`). Kiểm `this.$moment` có sẵn (grep); không có thì dùng `dayjs`/hàm ngày project đang dùng. Datepicker Ngày trả thêm `:max-date` = limit nếu component hỗ trợ.
Thêm `data-test="ycxh-return-date"` cho khối Ngày trả.

- [x] **Step 4: Chạy e2e, xác nhận PASS** — cả `draft.spec.ts` + `type-3.spec.ts`.
- [ ] **Step 5: Commit (chỉ khi user đã yêu cầu).**

---

## Task 16: Hồi quy toàn bộ + đối chiếu ERP

**Files:** không sửa code (chỉ sửa nếu phát hiện lỗi — mỗi lỗi: test RED → sửa → GREEN, ghi ledger).

- [x] **Step 1: BE toàn thư mục** — `cd HRM/hrm-api && php artisan test tests/Feature/ProductExportRequest > $SCRATCH/be.log 2>&1; tail -20 $SCRATCH/be.log` → Expected: 0 failure (SKIP liệt kê kèm lý do).
- [x] **Step 2: e2e toàn thư mục** — `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/product-export-requests` → Expected: PASS hết.
- [x] **Step 3: Downstream** (spec §7) — với 1 phiếu 20 và 1 phiếu 12 vừa gửi duyệt: lập ĐNXK từ YCXH (`/{id}/warehouse-export-data` + POST) chạy được; phiếu 20 xuất thẳng lập được Phiếu xuất hàng (`/{id}/product-export-data`). Mở cả 2 phiếu trên màn ERP YCXH (danh sách + chi tiết) → không lỗi, hiện đúng kho/HĐ.
- [x] **Step 4: Đối chiếu ERP từng loại** (skill erp-to-hrm-screen) — với mỗi loại 3/6/7/12/14/18/19/99/20/21: mở màn Tạo ERP + HRM cạnh nhau, đánh dấu bảng: trường header · cột bảng hàng · popup · ràng buộc gửi duyệt. Ghi bảng vào `.plans/gop-db/ycxh-port-erp-day-du/design.md` mục "Đối chiếu Phase 1". Lệch nằm trong phạm vi Phase 1 → sửa (RED/GREEN); ngoài phạm vi → ghi sang Phase 2+.
- [x] **Step 5: Cập nhật tài liệu** — `plan.md` đánh `[x]`, checkpoint; `STATUS.md`.

---

### Checkpoint — 2026-10-12
Vừa hoàn thành: brainstorm + spec Phase 1 + plan Phase 1 (17 task, 0–16)
Đang làm dở: —
Bước tiếp theo: user review plan, chọn cách thực thi (Subagent-driven / Native), trả lời Q-ERP (A/B)
Blocked: Task 8b + Task 9 chờ Q-ERP

### Checkpoint — 2026-10-12 (2)
Vừa hoàn thành: user duyệt plan; chọn Subagent-driven; Q-ERP = A
Đang làm dở: bắt đầu thực thi Task 0 (ledger SDD ở scratchpad phiên, không commit — review theo snapshot working tree)
Bước tiếp theo: Task 0 → 16 tuần tự
Blocked: —

### Checkpoint — 2026-10-12 (3) — tạm dừng (user gập máy)
Vừa hoàn thành: Task 0–12 xong (review đạt, e2e tests/product-export-requests 10/10, BE tests/Feature/ProductExportRequest 75). Task 13 (ManualLinesTable + StockViewModal) đã làm + review: Spec ✅, còn I1 (đổi ĐVT phải đổi đơn giá theo product_unit_prices price_type_id=1) và I2 (ô SL câu lỗi inline sau submit; gửi duyệt chặn dòng SL rỗng/≤0; nháp không được mất dòng).
Đang làm dở: Task 13 fix round 1 bị dừng giữa chừng — phần BE (giá theo ĐVT ở endpoint product-units, avatar lấy từ products.avatar, rule nháp) đã sửa; phần FE CHƯA: I1 FE + I2 + xoá method thừa removeManualRow/manualRowAmount/manualTotals + ẩn nút Xem tồn khi chưa có kho + min 0 ô SL + mr-2 nút +/- + e2e tương ứng.
Bước tiếp theo: kiểm git diff BE của fix round 1 + chạy BE test → làm nốt FE → e2e cả bộ → re-review → Task 14, 15, 16 → final review (opus). Chưa commit gì.
Ledger SDD + review/rulings: bản sao bền ở ~/.claude/projects/-Users-nguyentrancu-DEV-code-ERP-HRM/ycxh-sdd-backup/ (progress.md, task-13-review.md, briefs).
Blocked: —

### Checkpoint — 2026-10-12 (4) — Phase 1 xong code, CHỜ USER
Vừa hoàn thành: Task 13–16 + review toàn nhánh (opus) + 1 lượt sửa cuối: I1 nháp loại 7 chưa gắn phiếu chuyển → màn Sửa mở ô phiếu chuyển, đã gắn giữ F9=(a), gửi duyệt thiếu phiếu chuyển → 422; I2 insertManualLines BE tự tra giá (product_unit_prices price_type_id=1) + tên/mã/model/hãng/ĐVT, bỏ qua payload. BE ProductExportRequest 93/93; e2e 24/26 + 2 ca page.goto timeout 30s (Nuxt dev) chạy lại riêng PASS.
Đang làm dở: không
Bước tiếp theo: user trả lời L1/L2 (giới hạn kho theo công ty), L3 (sửa hiển thị loại 20/21 bên ERP), L5 (thêm StockService::getCompanyLineStocks public), xoá 2 modal không dùng (WarehouseExportRequestModal, ContractSearchModal), và có commit không (nhớ ERP App/Model/Hrm/HrmContract.php untracked + server cần HRM_URL_FE).
Blocked: L5 chờ user cho sửa hàm dùng chung StockService

### Lượt G — làm theo ERP + dọn code (user 2026-10-12)
- [x] L1/L2 kho theo công ty người lập (accounting_warehouses) + loại 6 chặn kho khác công ty
- [x] L5 StockService::getCompanyLineStocks (hàm mới) — cột Tồn loại 7 theo ERP
- [x] L6 emplement_contract_type loại 19 lưu mã ERP ('1'/'2'/'4', WR '3'), đọc được class cũ
- [x] L3 ERP hiển thị HĐ HRM cho 20/21 (YCXH list/chi tiết, PXH list/excel/chi tiết, ĐNXK chi tiết)
- [x] Xoá WarehouseExportRequestModal.vue, ContractSearchModal.vue (YCXH), field thừa payload dòng nhập tay
- [x] Commit+push 13/10: api 82e179d7b, client ed8f003fd, ERP 32e217df48, e2e 33feff1 (local)

### Checkpoint — 2026-10-13
Vừa hoàn thành: Lượt G (BE 110 pass, e2e YCXH 28 pass, ERP php -l)
Đang làm dở: —
Bước tiếp theo: user kiểm tay ERP 3 màn loại 20/21 rồi bảo commit
Blocked: —

## Bugfix list — gỡ "Hủy" thừa khỏi cột Hành động (2026-10-14)
- [x] **Phiếu "Đang tạo" (nháp) thừa hành động "Hủy"** (user báo kèm ảnh). ERP `canCancel()` = nháp + người tạo, **trùng khít** `canDelete()`, và ERP **không** render Hủy trên danh sách — nháp chỉ có "Xóa" (route `productExportRequest.cancel` tồn tại nhưng mồ côi, không view nào gọi). Port HRM lỡ thêm Hủy vào `getRowActions` (commit 51a3187c7). FIX **chỉ FE** `pages/finance/product-export-requests/index.vue`: gỡ action `key:'cancel'` + case `'cancel'` + method `cancelRow()`, thêm comment chặn thêm lại. BE `canCancel()`/endpoint `/cancel` GIỮ NGUYÊN (ERP parity — route mồ côi). **Verify Playwright** (PYCXH-39303, Đang tạo, user 13): menu Hành động khác = In yêu cầu · In biên bản giao nhận - bàn giao · Xuất excel danh sách hàng · Lịch sử — KHÔNG còn Hủy; nút ngoài vẫn Sửa + Xóa. CHƯA commit.

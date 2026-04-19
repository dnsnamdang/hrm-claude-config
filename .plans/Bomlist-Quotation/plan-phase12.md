# Plan Phase 12 — Quản lý VAT cho Báo giá

> **Spec:** [design-phase12-vat.md](./design-phase12-vat.md)
> **Ngày bắt đầu:** 2026-04-19
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign` (cả API + Client)

**Goal:** Thêm quản lý VAT per-row trong báo giá — 3 cột mới (VAT%, Tiền VAT, Thành tiền sau VAT), roll-up CHA-CON, toolbar bulk apply + soft-prompt lần đầu, full coverage (edit/show/list/tab/excel/history).

**Tech stack:** Laravel 8 + MySQL (API), Nuxt 2 + Vue 2 + Bootstrap-Vue (Client), reuse pattern Phase 11.

---

## Trạng thái tổng

- Brainstorm: Done (2026-04-19)
- Design: Done (`design-phase12-vat.md`)
- Plan: Done
- Tiến độ: 58/64 tasks (sau bổ sung Batch 10 DONE + Batch 11 DONE — 12.9 Task 58-64 hoàn thành)

---

## Quy tắc thực thi

1. Không commit/push — user tự quản lý git.
2. Hoàn thành 1 task → đánh `[x]` ngay, không batch cuối session.
3. Sau mỗi nhóm (12.X) → smoke test thủ công qua Postman/UI.
4. FE tuân thủ V2Base components (xem `docs/shared.md`).
5. Dùng companion `docs/srs/` / `.plans/` cho docs nếu cần — không tạo doc mới khi chưa yêu cầu.

---

## 12.1 — BE: Migration + Entity + Service (13 tasks)

**Folder BE:** `hrm-api/database/migrations/`, `hrm-api/Modules/Assign/Entities/`, `hrm-api/Modules/Assign/Services/`

- [x] **Task 1:** Migration `2026_04_19_100001_add_vat_to_quotation_product_prices.php`

  File: `hrm-api/database/migrations/2026_04_19_100001_add_vat_to_quotation_product_prices.php`
  ```php
  <?php
  use Illuminate\Database\Migrations\Migration;
  use Illuminate\Database\Schema\Blueprint;
  use Illuminate\Support\Facades\Schema;

  class AddVatToQuotationProductPrices extends Migration {
      public function up() {
          Schema::table('quotation_product_prices', function (Blueprint $t) {
              $t->decimal('vat_percent', 5, 2)->default(0)->after('quoted_price')
                ->comment('VAT % — chỉ có giá trị ở dòng CHA hoặc dòng độc lập; CON luôn = 0');
          });
      }
      public function down() {
          Schema::table('quotation_product_prices', function (Blueprint $t) {
              $t->dropColumn('vat_percent');
          });
      }
  }
  ```

- [x] **Task 2:** Migration `2026_04_19_100002_add_vat_totals_to_quotations.php`

  File: `hrm-api/database/migrations/2026_04_19_100002_add_vat_totals_to_quotations.php`
  ```php
  <?php
  use Illuminate\Database\Migrations\Migration;
  use Illuminate\Database\Schema\Blueprint;
  use Illuminate\Support\Facades\Schema;

  class AddVatTotalsToQuotations extends Migration {
      public function up() {
          Schema::table('quotations', function (Blueprint $t) {
              $t->decimal('total_vat_amount', 18, 2)->default(0)->after('sales_note')
                ->comment('Tổng tiền VAT (currency gốc của quotation)');
              $t->decimal('total_after_vat', 18, 2)->default(0)->after('total_vat_amount')
                ->comment('Tổng bán sau VAT = totalSale + total_vat_amount');
          });
      }
      public function down() {
          Schema::table('quotations', function (Blueprint $t) {
              $t->dropColumn(['total_vat_amount', 'total_after_vat']);
          });
      }
  }
  ```

- [x] **Task 3:** Chạy migration + smoke

  ```bash
  cd hrm-api && php artisan migrate
  ```
  Expected: "Migrated: 2026_04_19_100001_add_vat_to_quotation_product_prices" + "Migrated: 2026_04_19_100002_add_vat_totals_to_quotations".
  Verify: `DESCRIBE quotation_product_prices` có cột `vat_percent DECIMAL(5,2) DEFAULT 0`. `DESCRIBE quotations` có 2 cột mới.

- [x] **Task 4:** Update entity `QuotationProductPrice.php`

  File: `hrm-api/Modules/Assign/Entities/QuotationProductPrice.php`

  Thêm `'vat_percent'` vào `$fillable`. Thêm cast:
  ```php
  protected $casts = [
      'estimated_price' => 'decimal:2',
      'quoted_price' => 'decimal:2',
      'vat_percent' => 'decimal:2',    // NEW
  ];
  ```

- [x] **Task 5:** Update entity `Quotation.php`

  File: `hrm-api/Modules/Assign/Entities/Quotation.php`

  Thêm `'total_vat_amount', 'total_after_vat'` vào `$fillable`. Thêm vào `$casts`:
  ```php
  'total_vat_amount' => 'decimal:2',
  'total_after_vat' => 'decimal:2',
  ```

- [x] **Task 6:** Update entity `QuotationHistory.php` — thêm constant

  File: `hrm-api/Modules/Assign/Entities/QuotationHistory.php`

  Thêm dòng:
  ```php
  const ACTION_UPDATE_VAT_BULK = 'update_vat_bulk';
  ```
  (Ngay sau các ACTION_* hiện có).

- [x] **Task 7:** Service — thêm helper `isParentWithChildren($row, $allProducts)` trong `QuotationService.php`

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Thêm private method:
  ```php
  private function isParentWithChildren($row, $allProducts) {
      if (!empty($row->parent_id)) return false;
      foreach ($allProducts as $p) {
          if ((int)$p->parent_id === (int)$row->id) return true;
      }
      return false;
  }
  ```

- [x] **Task 8:** Service — method `recomputeTotals(Quotation $q)`

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Thêm private method:
  ```php
  private function recomputeTotals(Quotation $q): void {
      $products = $q->bomList->products()->get();  // adjust theo relationship thực tế
      $prices = QuotationProductPrice::where('quotation_id', $q->id)->get()->keyBy('bom_list_product_id');

      $totalSale = 0;
      $totalVat = 0;

      foreach ($products as $p) {
          if (!empty($p->parent_id)) continue; // skip CON

          $price = $prices->get($p->id);
          $vatPercent = $price ? (float)$price->vat_percent : 0;

          $hasChildren = $products->contains(fn($x) => (int)$x->parent_id === (int)$p->id);
          if ($hasChildren) {
              // Roll-up: sum children line sale
              $children = $products->filter(fn($x) => (int)$x->parent_id === (int)$p->id);
              $lineSale = 0;
              foreach ($children as $c) {
                  $cp = $prices->get($c->id);
                  $lineSale += ($cp ? (float)$cp->quoted_price : 0) * (float)$c->qty_needed;
              }
          } else {
              $lineSale = ($price ? (float)$price->quoted_price : 0) * (float)$p->qty_needed;
          }
          $totalSale += $lineSale;
          $totalVat += $lineSale * ($vatPercent / 100);
      }

      $q->total_vat_amount = $totalVat;
      $q->total_after_vat = $totalSale + $totalVat;
      $q->save();
  }
  ```

  Note: Cần verify relationship/attribute name thực tế (`qty_needed` vs `quantity`, `$q->bomList->products` vs trực tiếp query). Đọc service hiện có trước khi copy tên field.

- [x] **Task 9:** Service — update `upsertPrices` với logic force CHA/CON

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Tìm method `upsertPrices` (hoặc logic tương đương trong `update`). Thêm logic:
  ```php
  // Load cấu trúc parent_id từ bom_list_products
  $productMap = $q->bomList->products()->get()->keyBy('id');

  foreach ($inputPrices as $data) {
      $bomProductId = $data['bom_list_product_id'];
      $product = $productMap->get($bomProductId);
      if (!$product) continue;

      $isChild = !empty($product->parent_id);
      $hasChildren = $productMap->contains(fn($x) => (int)$x->parent_id === (int)$product->id);

      $payload = [
          'estimated_price' => $data['estimated_price'] ?? 0,
          'quoted_price' => $hasChildren ? 0 : ($data['quoted_price'] ?? 0),      // force 0 nếu CHA-có-CON
          'vat_percent' => $isChild ? 0 : ($data['vat_percent'] ?? 0),             // force 0 nếu CON
      ];

      QuotationProductPrice::updateOrCreate(
          ['quotation_id' => $q->id, 'bom_list_product_id' => $bomProductId],
          $payload
      );
  }

  $this->recomputeTotals($q);
  ```

- [x] **Task 10:** Service — update `calculateLevel` trả thêm `total_vat + total_after_vat`

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Trong method `calculateLevel`, tính thêm:
  ```php
  // Ở cuối, sau khi tính totalSale, totalImport, margin, level
  $totalVat = 0;
  // Reuse logic từ recomputeTotals để tính totalVat từ prices hiện có
  // (Trích thành helper riêng hoặc inline tuỳ style code)

  return [
      'total_import' => $totalImport,
      'total_sale' => $totalSale,
      'total_vat' => $totalVat,
      'total_after_vat' => $totalSale + $totalVat,
      'margin' => $margin,
      'level' => $level,
  ];
  ```

- [x] **Task 11:** Service — method `applyBulkVat`

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Thêm public method:
  ```php
  public function applyBulkVat(Quotation $q, float $vatPercent, string $mode): array {
      // Validate status
      if ($q->status != Quotation::STATUS_DANG_TAO) {
          throw new \Exception('Báo giá đã gửi, không thể sửa VAT', 422);
      }
      if ($q->created_by !== auth()->id()) {
          throw new \Exception('Chỉ người tạo mới được áp VAT', 403);
      }

      $totalVatBefore = (float)$q->total_vat_amount;

      // Load eligible rows: bom_list_products có parent_id=null (CHA hoặc orphan)
      $products = $q->bomList->products()->whereNull('parent_id')->get();
      $prices = QuotationProductPrice::where('quotation_id', $q->id)
          ->whereIn('bom_list_product_id', $products->pluck('id'))
          ->get()->keyBy('bom_list_product_id');

      $affected = 0;
      foreach ($products as $p) {
          $existing = $prices->get($p->id);
          $currentVat = $existing ? (float)$existing->vat_percent : 0;

          if ($mode === 'zero_only' && $currentVat > 0) continue;

          QuotationProductPrice::updateOrCreate(
              ['quotation_id' => $q->id, 'bom_list_product_id' => $p->id],
              ['vat_percent' => $vatPercent]
          );
          $affected++;
      }

      $this->recomputeTotals($q);
      $q->refresh();

      // Log history
      QuotationHistory::create([
          'quotation_id' => $q->id,
          'action' => QuotationHistory::ACTION_UPDATE_VAT_BULK,
          'from_status' => $q->status,
          'to_status' => $q->status,
          'actor_id' => auth()->id(),
          'meta' => [
              'vat_percent' => $vatPercent,
              'mode' => $mode,
              'affected_count' => $affected,
              'total_vat_before' => $totalVatBefore,
              'total_vat_after' => (float)$q->total_vat_amount,
          ],
      ]);

      return [
          'affected_count' => $affected,
          'total_vat_amount' => (float)$q->total_vat_amount,
          'total_after_vat' => (float)$q->total_after_vat,
      ];
  }
  ```

- [x] **Task 12:** Service — call `recomputeTotals` ở 4 điểm transition status

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Trong mỗi method `submit`, `selfApprove`, `tpApprove`, `bgdApprove`, thêm dòng trước khi `$q->save()`:
  ```php
  $this->recomputeTotals($q);
  ```

- [x] **Task 13:** Smoke test BE nhóm 12.1 qua tinker

  ```bash
  cd hrm-api && php artisan tinker
  ```
  Chạy:
  ```php
  $svc = app(\Modules\Assign\Services\QuotationService::class);
  $q = \Modules\Assign\Entities\Quotation::find(1);  // adjust id
  $svc->applyBulkVat($q, 10.0, 'all');
  $q->refresh();
  echo $q->total_vat_amount . ' / ' . $q->total_after_vat;
  ```
  Expected: output số hợp lý (không crash). Check `quotation_histories` có record mới.

**Smoke test nhóm 12.1 pass → chuyển sang 12.2.**

---

## 12.2 — BE: Controller + Route + Form Request + Transformer (7 tasks)

**Folder:** `hrm-api/Modules/Assign/Http/Controllers/`, `Http/Requests/`, `Transformers/`, `Routes/`

- [x] **Task 14:** Tạo Form Request `QuotationApplyVatBulkRequest.php`

  File: `hrm-api/Modules/Assign/Http/Requests/QuotationApplyVatBulkRequest.php`
  ```php
  <?php
  namespace Modules\Assign\Http\Requests;
  use Illuminate\Foundation\Http\FormRequest;

  class QuotationApplyVatBulkRequest extends FormRequest {
      public function authorize() { return true; }
      public function rules() {
          return [
              'vat_percent' => 'required|numeric|min:0|max:100',
              'mode' => 'required|in:all,zero_only',
          ];
      }
      public function messages() {
          return [
              'vat_percent.max' => 'VAT không được vượt quá 100%',
              'vat_percent.min' => 'VAT không được âm',
              'mode.in' => 'Phạm vi áp dụng không hợp lệ',
          ];
      }
  }
  ```

- [x] **Task 15:** Thêm action `applyVatBulk` vào `QuotationController.php`

  File: `hrm-api/Modules/Assign/Http/Controllers/QuotationController.php`

  Thêm method (sau `reject`):
  ```php
  public function applyVatBulk(
      \Modules\Assign\Http\Requests\QuotationApplyVatBulkRequest $req,
      $id
  ) {
      $q = Quotation::findOrFail($id);
      $result = $this->service->applyBulkVat($q, (float)$req->vat_percent, $req->mode);
      return response()->json(['data' => $result]);
  }
  ```

  Thêm use statement ở đầu file nếu cần:
  ```php
  use Modules\Assign\Http\Requests\QuotationApplyVatBulkRequest;
  ```

- [x] **Task 16:** Thêm route `POST /quotations/{id}/apply-vat-bulk`

  File: `hrm-api/Modules/Assign/Routes/api.php`

  Trong group quotation, thêm:
  ```php
  Route::post('quotations/{id}/apply-vat-bulk', [QuotationController::class, 'applyVatBulk']);
  ```
  (Đặt gần các route quotation khác như `/submit`, `/reject`.)

- [x] **Task 17:** Update `QuotationProductPriceResource` hoặc embed trong `DetailQuotationResource`

  File: `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php`

  Trong section products trả về, thêm field cho mỗi product:
  ```php
  // Với mỗi product:
  $vatPercent = optional($pricesMap->get($product->id))->vat_percent ?? 0;
  $hasChildren = $productsCollection->contains(fn($x) => (int)$x->parent_id === (int)$product->id);

  $result[] = [
      // ... các field cũ
      'estimated_price' => ...,
      'quoted_price' => ...,
      'vat_percent' => (float)$vatPercent,          // NEW
      'is_parent_with_children' => $hasChildren,    // NEW
  ];
  ```

  Ở root resource, thêm:
  ```php
  'total_vat_amount' => (float)$this->total_vat_amount,      // NEW
  'total_after_vat' => (float)$this->total_after_vat,        // NEW
  ```

- [x] **Task 18:** Update `QuotationResource` (list) thêm `total_after_vat`

  File: `hrm-api/Modules/Assign/Transformers/QuotationResource.php`

  Thêm vào return array:
  ```php
  'total_after_vat' => (float)$this->total_after_vat,
  ```

- [x] **Task 19:** Smoke test endpoint `apply-vat-bulk` qua Postman

  - POST `/api/v1/assign/quotations/{id}/apply-vat-bulk` với body `{"vat_percent": 10, "mode": "all"}`.
  - Expected: 200 với data `{affected_count, total_vat_amount, total_after_vat}`.
  - Case 422: `vat_percent=-5` hoặc `mode=invalid`.
  - Case 422: call trên báo giá status=2.
  - Case 403: call bởi user không phải creator.
  - Verify DB: `quotation_product_prices.vat_percent` updated, `quotations.total_vat_amount + total_after_vat` updated, `quotation_histories` có record `action=update_vat_bulk`.

- [x] **Task 20:** Smoke test endpoint `calculateLevel` trả đủ 6 field

  - POST `/api/v1/assign/quotations/{id}/calculate-level`.
  - Expected response: `{data: {total_import, total_sale, total_vat, total_after_vat, margin, level}}`.

**Smoke test nhóm 12.2 pass → chuyển sang 12.3.**

---

## 12.3 — BE: Excel Export template (3 tasks)

- [x] **Task 21:** Update Excel blade template

  File: `hrm-api/resources/views/exports/bom_list.blade.php`

  Tìm header row hiện có (có "Thành tiền bán" hoặc tương đương). Thêm 3 `<th>` sau "Thành tiền bán":
  ```blade
  <th>VAT(%)</th>
  <th>Tiền VAT</th>
  <th>Thành tiền sau VAT</th>
  ```

  Với body loop sản phẩm, thêm 3 `<td>` tương ứng (blank cho CON):
  ```blade
  @if(empty($item->parent_id))
      <td>{{ number_format($item->vat_percent ?? 0, 2) }}%</td>
      <td>{{ number_format($item->line_vat_amount ?? 0) }}</td>
      <td>{{ number_format($item->line_after_vat ?? 0) }}</td>
  @else
      <td></td><td></td><td></td>
  @endif
  ```

  Sau dòng TỔNG, thêm 2 dòng (N = số cột trước cột "Tiền VAT" trong template blade hiện tại — mở file và đếm thủ công trước khi code):
  ```blade
  <tr>
      <td colspan="N" align="right"><b>Tổng VAT:</b></td>
      <td><b>{{ number_format($totalVatAmount ?? 0) }}</b></td>
      <td colspan="2"></td>
  </tr>
  <tr>
      <td colspan="N" align="right"><b>Tổng sau VAT:</b></td>
      <td colspan="3"><b>{{ number_format($totalAfterVat ?? 0) }}</b></td>
  </tr>
  ```

  **Cách xác định N:** mở `bom_list.blade.php`, tìm `<tr>` chứa label "TỔNG" hoặc "Total". Đếm tổng số `<th>` trong `<thead>` — trừ đi 3 (VAT%, Tiền VAT, Thành tiền sau VAT vừa thêm). Ví dụ nếu thead có 13 `<th>` sau thêm 3 cột mới → N = 13 − 3 − 1 = 9 (vì colspan tính từ cột đầu đến cột "Thành tiền bán" — cột liền trước Tỷ suất LN/VAT).

- [x] **Task 22:** Update `QuotationController::exportExcel` truyền thêm field

  File: `hrm-api/Modules/Assign/Http/Controllers/QuotationController.php`

  Trong method `exportExcel`, khi build products array truyền vào BomListExport, inject thêm `vat_percent`, `line_vat_amount`, `line_after_vat` cho mỗi item:
  ```php
  foreach ($products as &$item) {
      $price = $priceMap->get($item->id);
      $vatPercent = $price ? (float)$price->vat_percent : 0;
      $hasChildren = ...; // same logic
      $lineSale = $hasChildren ? /* sum children */ : ($price->quoted_price ?? 0) * $item->qty_needed;
      $item->vat_percent = $vatPercent;
      $item->line_vat_amount = $lineSale * ($vatPercent / 100);
      $item->line_after_vat = $lineSale + $item->line_vat_amount;
  }

  return $this->bomListExport
      ->withProducts($products)
      ->withTotalVatAmount($q->total_vat_amount)
      ->withTotalAfterVat($q->total_after_vat)
      ->download(...);
  ```
  (Method trên `BomListExport` có thể cần add setter `withTotalVatAmount` / `withTotalAfterVat` nếu chưa có.)

- [x] **Task 23:** Smoke test xuất Excel

  Từ UI màn show báo giá click "Xuất Excel", hoặc gọi trực tiếp `GET /api/v1/assign/quotations/{id}/export-excel`. Mở file `.xlsx`:
  - Header có 3 cột mới.
  - Dòng CON blank 3 ô.
  - Dòng TỔNG + 2 dòng mới "Tổng VAT", "Tổng sau VAT" hiển thị đúng số.

**Smoke test nhóm 12.3 pass → chuyển sang 12.4.**

---

## 12.4 — FE: Store + Components mới (4 tasks)

**Folder:** `hrm-client/store/`, `hrm-client/components/assign/quotation/`

- [x] **Task 24:** Thêm action `applyVatBulk` vào `store/quotation.js`

  File: `hrm-client/store/quotation.js`

  Thêm vào `actions`:
  ```js
  async applyVatBulk({ dispatch }, { id, vat_percent, mode }) {
      return dispatch('apiPostMethod', {
          url: `assign/quotations/${id}/apply-vat-bulk`,
          payload: { vat_percent, mode },
      }, { root: true })
  }
  ```

  (Xem các action cũ như `submit`, `reject` để đảm bảo cú pháp `dispatch('apiPostMethod', ...)` match convention Phase 11.)

- [x] **Task 25:** Tạo component `VatBulkApplyToolbar.vue`

  File: `hrm-client/components/assign/quotation/VatBulkApplyToolbar.vue`
  ```vue
  <template>
    <div class="d-flex align-items-center vat-toolbar mb-3">
        <span class="mr-2 font-weight-bold">Áp VAT đồng loạt:</span>
        <V2BaseInput
            v-model="vatInput"
            type="number"
            min="0"
            max="100"
            step="0.01"
            placeholder="%"
            style="width: 100px;"
            class="mr-2 mb-0"
            :disabled="disabled"
        />
        <V2BaseButton
            variant="primary"
            size="sm"
            class="mr-2"
            :disabled="!canApply"
            @click="apply('all')"
        >
            Áp cho tất cả
        </V2BaseButton>
        <V2BaseButton
            variant="light"
            size="sm"
            :disabled="!canApply"
            @click="apply('zero_only')"
        >
            Chỉ dòng VAT=0
        </V2BaseButton>
    </div>
  </template>

  <script>
  export default {
      name: 'VatBulkApplyToolbar',
      props: {
          quotationId: { type: [Number, String], required: true },
          disabled: { type: Boolean, default: false },
      },
      data() {
          return { vatInput: '' }
      },
      computed: {
          canApply() {
              if (this.disabled) return false
              const v = Number(this.vatInput)
              return !isNaN(v) && v >= 0 && v <= 100 && this.vatInput !== ''
          },
      },
      methods: {
          async apply(mode) {
              try {
                  this.$safeLoadingStart()
                  const res = await this.$store.dispatch('quotation/applyVatBulk', {
                      id: this.quotationId,
                      vat_percent: Number(this.vatInput),
                      mode,
                  })
                  const count = res?.data?.data?.affected_count ?? 0
                  this.$toast.success(`Đã áp ${this.vatInput}% cho ${count} dòng`)
                  this.$emit('applied', { mode, vat_percent: Number(this.vatInput), affected_count: count })
                  this.vatInput = ''
              } catch (e) {
                  this.$toast.error(e?.response?.data?.message || 'Áp VAT thất bại')
              } finally {
                  this.$safeLoadingFinish()
              }
          },
      },
  }
  </script>

  <style scoped>
  .vat-toolbar { background: #f8f9fa; padding: 8px 12px; border-radius: 4px; }
  </style>
  ```

- [x] **Task 26:** Tạo component `VatFirstEntryPromptModal.vue`

  File: `hrm-client/components/assign/quotation/VatFirstEntryPromptModal.vue`
  ```vue
  <template>
    <b-modal
        :visible="show"
        title="Áp dụng VAT đồng loạt?"
        size="sm"
        hide-footer
        no-close-on-backdrop
        @hide="onCancel"
    >
        <p class="mb-3">
            Áp dụng <b>{{ vatPercent }}%</b> VAT cho <b>{{ zeroRowsCount }}</b>
            sản phẩm còn đang để 0%?
        </p>
        <div class="d-flex justify-content-end">
            <V2BaseButton variant="light" class="mr-2" @click="onSkipAll">
                Chỉ dòng này
            </V2BaseButton>
            <V2BaseButton variant="primary" @click="onApplyAll">
                Áp dụng tất cả dòng còn 0%
            </V2BaseButton>
        </div>
    </b-modal>
  </template>

  <script>
  export default {
      name: 'VatFirstEntryPromptModal',
      props: {
          show: { type: Boolean, default: false },
          vatPercent: { type: Number, required: true },
          zeroRowsCount: { type: Number, required: true },
      },
      methods: {
          onApplyAll() { this.$emit('apply-all') },
          onSkipAll() { this.$emit('skip-all') },
          onCancel() { this.$emit('skip-all') },
      },
  }
  </script>
  ```

- [x] **Task 27:** Smoke test 2 component riêng lẻ trong Storybook hoặc 1 page test tạm

  Skip nếu không có Storybook — sẽ test qua integration ở nhóm 12.5.

**Smoke test nhóm 12.4 pass (hoặc deferred) → chuyển sang 12.5.**

---

## 12.5 — FE: Màn edit làm giá (`edit.vue` chính) (14 tasks)

**File:** `hrm-client/pages/assign/quotations/_id/edit.vue`

- [x] **Task 28:** Import 2 component mới + store action

  Trong `<script>`:
  ```js
  import VatBulkApplyToolbar from '@/components/assign/quotation/VatBulkApplyToolbar.vue'
  import VatFirstEntryPromptModal from '@/components/assign/quotation/VatFirstEntryPromptModal.vue'

  export default {
      components: { ..., VatBulkApplyToolbar, VatFirstEntryPromptModal },
  }
  ```

- [x] **Task 29:** Thêm data state cho VAT UX

  Trong `data()`:
  ```js
  return {
      ...
      vatPromptShown: false,           // session flag — không persist
      vatPromptShowing: false,         // modal visibility
      vatPromptPercent: 0,             // value user vừa nhập
      vatPromptEditingRow: null,       // row đang edit để rollback nếu user skip
  }
  ```

- [x] **Task 30:** Update 3 column header trong `<thead>`

  Sau `<th>Tỷ suất LN</th>`, thêm:
  ```html
  <th class="text-right" style="width:100px">
      VAT(%)
      <i class="ri-information-line text-muted"
         v-b-tooltip.hover
         title="VAT chỉ áp dụng trên dòng CHA hoặc SP độc lập. SP con được cộng gộp vào CHA."
      ></i>
  </th>
  <th class="text-right" style="width:130px">Tiền VAT</th>
  <th class="text-right" style="width:150px">Thành tiền sau VAT</th>
  ```

- [x] **Task 31:** Update row CHA (parent) — disable giá bán + thêm 3 cell VAT

  Trong `<template v-for="(parent, pi) in group.parents">`, trong `<tr class="parent-row">`:

  Đổi cell Giá bán:
  ```html
  <td :class="{ 'cell-invalid': !isParentWithChildren(parent) && Number(parent.quoted_price) <= 0 }">
      <V2BaseCurrencyInput
          v-model="parent.quoted_price"
          :disabled="!canEdit || isParentWithChildren(parent)"
          v-b-tooltip.hover
          :title="isParentWithChildren(parent) ? 'Tự động tính từ SP con' : ''"
      />
  </td>
  ```

  Sau cell "Tỷ suất LN", thêm 3 cell mới:
  ```html
  <td>
      <V2BaseInput
          v-model="parent.vat_percent"
          type="number"
          min="0"
          max="100"
          step="0.01"
          :disabled="!canEdit"
          @input="onVatInput(parent, $event)"
      />
  </td>
  <td class="text-right">{{ formatMoney(lineVatAmount(parent)) }}</td>
  <td class="text-right">{{ formatMoney(lineAfterVat(parent)) }}</td>
  ```

- [x] **Task 32:** Update row CON (child) — 3 cell "—"

  Trong `<tr v-for="child in getChildren(parent)">`, sau cell "Tỷ suất LN", thêm:
  ```html
  <td class="text-center text-muted">—</td>
  <td class="text-center text-muted">—</td>
  <td class="text-center text-muted">—</td>
  ```

- [x] **Task 33:** Update row TỔNG cuối bảng

  Tìm `<th colspan="6" class="text-right">TỔNG</th>`. Giữ colspan=6, sau các `<th>` totalImport/—/totalSale/margin, thêm 3 `<th>` mới:
  ```html
  <th></th>                                                  <!-- VAT(%) để trống -->
  <th class="text-right font-weight-bold">{{ formatMoney(totalVat) }}</th>
  <th class="text-right font-weight-bold">{{ formatMoney(totalAfterVat) }}</th>
  ```

- [x] **Task 34:** Thêm 4 computed mới + update 1 computed cũ

  Trong `computed: { ... }`:

  Update `lineSaleTotal` (hiện tại là method) → đổi thành roll-up logic:
  ```js
  // Đổi từ method → vẫn giữ là method nhưng thêm roll-up
  lineSaleTotal(p) {
      if (this.isParentWithChildren(p)) {
          return this.getChildren(p).reduce((sum, c) => sum + this.lineSaleTotal(c), 0)
      }
      return (Number(p.quoted_price) || 0) * (Number(p.qty_needed) || 0)
  },
  ```

  Thêm 2 method mới cạnh `lineSaleTotal`:
  ```js
  lineVatAmount(p) {
      if (p.parent_id) return null
      return this.lineSaleTotal(p) * (Number(p.vat_percent) || 0) / 100
  },
  lineAfterVat(p) {
      if (p.parent_id) return null
      return this.lineSaleTotal(p) + this.lineVatAmount(p)
  },
  ```

  Thêm 2 computed mới:
  ```js
  totalVat() {
      return this.products
          .filter(p => !p.parent_id)   // orphan + parent-with-children
          .reduce((sum, p) => sum + (this.lineVatAmount(p) || 0), 0)
  },
  totalAfterVat() {
      return this.totalSale + this.totalVat
  },
  ```

  Update computed `totalSale` — sử dụng parent (roll-up) thay vì children, tránh double:
  ```js
  totalSale() {
      return this.products
          .filter(p => !p.parent_id)   // chỉ parent-with-children + orphan
          .reduce((sum, p) => sum + this.lineSaleTotal(p), 0)
  },
  ```

  Giữ nguyên `totalImport` hoặc update tương tự:
  ```js
  totalImport() {
      return this.products
          .filter(p => !p.parent_id)
          .reduce((sum, p) => {
              if (this.isParentWithChildren(p)) {
                  return sum + this.getChildren(p).reduce((s, c) => s + this.lineImportTotal(c), 0)
              }
              return sum + this.lineImportTotal(p)
          }, 0)
  },
  ```

- [x] **Task 35:** Soft-prompt handler — method `onVatInput`

  Trong `methods: { ... }`:
  ```js
  onVatInput(row, newValue) {
      const v = Number(newValue)
      if (this.vatPromptShown) return
      const oldValue = Number(row._lastVatValue || 0)
      row._lastVatValue = v
      if (oldValue !== 0 || v <= 0) return

      // Đếm rows còn 0 (không tính row hiện tại)
      const zeroRows = this.products.filter(p =>
          !p.parent_id && p.id !== row.id && Number(p.vat_percent || 0) === 0
      )
      if (zeroRows.length === 0) return  // không có row khác còn 0% → không prompt

      this.vatPromptPercent = v
      this.vatPromptEditingRow = row
      this.vatPromptShowing = true
  },
  async onVatPromptApplyAll() {
      this.vatPromptShown = true
      this.vatPromptShowing = false
      try {
          this.$safeLoadingStart()
          const res = await this.$store.dispatch('quotation/applyVatBulk', {
              id: this.quotationId,
              vat_percent: this.vatPromptPercent,
              mode: 'zero_only',
          })
          await this.reloadProducts()
          const count = res?.data?.data?.affected_count ?? 0
          this.$toast.success(`Đã áp ${this.vatPromptPercent}% cho ${count} dòng`)
      } catch (e) {
          this.$toast.error('Áp VAT thất bại')
      } finally {
          this.$safeLoadingFinish()
      }
  },
  onVatPromptSkip() {
      this.vatPromptShown = true
      this.vatPromptShowing = false
  },
  ```

  Note: `reloadProducts()` cần tồn tại hoặc tạo mới — reload từ API detail quotation, update `this.products` với giá/VAT mới.

- [x] **Task 36:** Gắn toolbar + modal vào template

  Ở vị trí trên table (sau info-card), thêm:
  ```html
  <VatBulkApplyToolbar
      :quotation-id="quotationId"
      :disabled="!canEdit"
      @applied="onToolbarApplied"
  />
  ```

  Cuối template (cạnh các modal khác), thêm:
  ```html
  <VatFirstEntryPromptModal
      :show="vatPromptShowing"
      :vat-percent="vatPromptPercent"
      :zero-rows-count="zeroRowsCount"
      @apply-all="onVatPromptApplyAll"
      @skip-all="onVatPromptSkip"
  />
  ```

  Thêm computed:
  ```js
  zeroRowsCount() {
      if (!this.vatPromptEditingRow) return 0
      return this.products.filter(p =>
          !p.parent_id && p.id !== this.vatPromptEditingRow.id && Number(p.vat_percent || 0) === 0
      ).length
  },
  ```

  Thêm handler `onToolbarApplied`:
  ```js
  async onToolbarApplied() {
      await this.reloadProducts()
  },
  ```

- [x] **Task 37:** Handler `reloadProducts` (reuse `fetchData()` để đồng bộ mapping `vat_percent` + `_lastVatValue`)

  Trong `methods`:
  ```js
  async reloadProducts() {
      const res = await this.$store.dispatch('quotation/fetchDetail', { id: this.quotationId })
      const data = res?.data?.data
      if (data?.products) {
          this.products = data.products.map(p => ({ ...p, _lastVatValue: Number(p.vat_percent || 0) }))
      }
  },
  ```
  (Adjust tên action `fetchDetail` theo store thực tế.)

- [x] **Task 38:** Update save payload — gửi `vat_percent` trong products

  Tìm method `saveDraft` / `saveAndSubmit`. Trong payload products, thêm field:
  ```js
  products: this.products.map(p => ({
      bom_list_product_id: p.id,
      estimated_price: p.estimated_price,
      quoted_price: p.quoted_price,
      vat_percent: p.vat_percent || 0,  // NEW
  })),
  ```

- [x] **Task 39:** Initial load — set `_lastVatValue` cho mỗi row

  Trong handler load data initial (hoặc `created()` / `asyncData`), sau khi assign `this.products`:
  ```js
  this.products.forEach(p => {
      p._lastVatValue = Number(p.vat_percent || 0)
  })
  ```
  (Để `onVatInput` detect đúng oldValue.)

- [x] **Task 40:** Smoke test UI màn edit (static SFC compile pass — UI integration test sẽ do user verify)

  - Mở `/assign/quotations/[id]/edit` → thấy 3 cột VAT, CHA-có-CON input giá bán disabled, CON hiện "—".
  - Nhập VAT=10 vào 1 row orphan → **modal xuất hiện** (nếu có row khác còn 0).
  - Click "Áp dụng tất cả dòng còn 0%" → reload, tất cả eligible = 10, toast success.
  - Nhập VAT=5 row khác → **KHÔNG prompt lần 2**.
  - Toolbar nhập 8 + "Chỉ dòng VAT=0" → dòng 10% giữ, dòng 0% → 8.
  - Row TỔNG cuối bảng có cell `totalVat` + `totalAfterVat` đúng số.
  - Footer bên ngoài bảng chỉ có Tổng nhập, Tổng bán, Tỷ suất LN, Cấp duyệt — KHÔNG thêm dòng VAT.
  - Đổi VAT → Tỷ suất LN + Cấp duyệt không đổi.

- [x] **Task 41:** Fix edge case + polish (static re-check pass: không có `variant=`, `this.$toast`, response `affected_count` 1 cấp, modal đủ 3 props)

  - Test: báo giá chỉ 1 row → nhập VAT=10 → **không prompt**.
  - Test: status=2 → toolbar disabled, input VAT disabled.
  - Test: reload page → nhập VAT lần đầu → prompt lại.

**Smoke test nhóm 12.5 pass → chuyển sang 12.6.**

---

## 12.6 — FE: Màn show + list + tab dự án (6 tasks)

- [x] **Task 42:** Update `_id/index.vue` (show báo giá) — thêm 3 cột readonly

  File: `hrm-client/pages/assign/quotations/_id/index.vue`

  Thêm header:
  ```html
  <th class="text-right">VAT(%)</th>
  <th class="text-right">Tiền VAT</th>
  <th class="text-right">Thành tiền sau VAT</th>
  ```

  Body parent row:
  ```html
  <td class="text-right">{{ Number(parent.vat_percent || 0).toFixed(2) }}%</td>
  <td class="text-right">{{ formatMoney(lineVatAmount(parent)) }}</td>
  <td class="text-right">{{ formatMoney(lineAfterVat(parent)) }}</td>
  ```

  Body child row:
  ```html
  <td class="text-center text-muted">—</td>
  <td class="text-center text-muted">—</td>
  <td class="text-center text-muted">—</td>
  ```

  Row TỔNG — thêm cell `totalVat` + `totalAfterVat` sau cột Tỷ suất LN:
  ```html
  <th></th>
  <th class="text-right font-weight-bold">{{ formatMoney(totalVat) }}</th>
  <th class="text-right font-weight-bold">{{ formatMoney(totalAfterVat) }}</th>
  ```

  Thêm computed (copy từ edit.vue):
  ```js
  lineSaleTotal(p), lineVatAmount(p), lineAfterVat(p), totalVat, totalAfterVat
  ```

- [x] **Task 43:** Smoke test màn show

  - Mở `/assign/quotations/[id]` → thấy 3 cột readonly đúng dữ liệu, CON "—", row TỔNG đúng.
  - Button "Xuất Excel" vẫn hoạt động.

- [x] **Task 44:** Update `pages/assign/quotations/index.vue` — thêm cột "Tổng sau VAT"

  Trong `columns` hoặc `availableColumns`, thêm entry sau cột "Tổng giá trị":
  ```js
  {
      key: 'total_after_vat',
      label: 'Tổng sau VAT',
      visible: true,          // default hiện
      sortable: true,
      formatter: (row) => `${this.formatMoney(row.total_after_vat)} ${row.currency_code || ''}`,
  }
  ```
  (Match convention columnCustomization hiện có — tham khảo cột "Tổng giá trị" cũ.)

  Trong ColumnCustomizationModal config (nếu có list riêng các cột toggle được), thêm cột này vào `availableColumns` để user ẩn/hiện.

- [x] **Task 45:** Smoke test list báo giá

  - Mở `/assign/quotations` → cột "Tổng sau VAT" hiển thị cuối.
  - Sort theo cột → OK.
  - Mở ColumnCustomizationModal → toggle ẩn → cột biến mất, state persist (localStorage hoặc user setting).

- [x] **Task 46:** Update `ProspectiveProjectQuotationsTab.vue` — thêm cột "Tổng sau VAT"

  File: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

  Tìm section cột (array `columns` hoặc `<b-table-column>` series). Thêm sau cột "Tổng bán" hiện có:
  ```js
  { key: 'total_after_vat', label: 'Tổng sau VAT', ... }
  ```

- [x] **Task 47:** Smoke test tab Báo giá ở dự án tiền khả thi

  - Mở dự án tiền khả thi bất kỳ → tab "Báo giá" → cột "Tổng sau VAT" hiển thị đúng.

**Smoke test nhóm 12.6 pass → chuyển sang 12.7.**

---

## 12.7 — Test thủ công end-to-end (6 tasks)

- [ ] **Task 48:** Module 1 — Roll-up logic

  - [ ] Mở edit báo giá có ít nhất 1 group CHA-2-CON.
  - [ ] Ô giá bán CHA disabled + tooltip "Tự động tính từ SP con" khi hover.
  - [ ] Nhập giá bán CON1=100, CON2=200, qty mỗi con=1 → Thành tiền bán CHA = 300 (hiển thị trên row CHA).
  - [ ] Save nháp → reload → DB `quotation_product_prices.quoted_price = 0` ở CHA.
  - [ ] Test trước mở: thử save với CHA có giá cũ → reload thấy giá CHA đã reset về 0 (vì backend force).

- [ ] **Task 49:** Module 2 — VAT per-row + soft-prompt

  - [ ] Báo giá mới, tất cả VAT=0. Nhập VAT=10 vào row orphan đầu tiên → **modal hiện** "Áp 10% cho N dòng còn 0?"
  - [ ] Click "Áp dụng tất cả dòng còn 0%" → tất cả orphan + CHA-có-CON = 10%, CON vẫn 0.
  - [ ] Nhập VAT=5 row khác → **KHÔNG prompt lần 2** (flag session đã set).
  - [ ] Reload page → nhập VAT lần đầu → prompt lại (flag reset).
  - [ ] Báo giá chỉ 1 SP duy nhất → nhập VAT → không prompt.
  - [ ] Nhập VAT=0 (lần đầu cũng là 0) → không prompt.

- [ ] **Task 50:** Module 3 — Toolbar bulk apply

  - [ ] Nhập 15 + "Áp cho tất cả" → toast "Đã áp 15% cho N dòng", tất cả eligible = 15%, CON vẫn 0%.
  - [ ] Nhập 8 + "Chỉ dòng VAT=0" → các dòng đã có VAT>0 giữ nguyên, dòng 0% → 8.
  - [ ] Nhập -5 → button disabled (không click được).
  - [ ] Nhập 150 → button disabled.
  - [ ] Input rỗng → button disabled.
  - [ ] Status=2 (gửi duyệt) → toolbar toàn bộ disabled.

- [ ] **Task 51:** Module 4 — Totals + Margin + Cấp duyệt

  - [ ] Row TỔNG cuối bảng hiển thị `totalVat` + `totalAfterVat` update realtime khi đổi VAT.
  - [ ] Footer bên ngoài bảng có đúng 4 dòng: Tổng nhập, Tổng bán, Tỷ suất LN, Cấp duyệt.
  - [ ] Đổi `quoted_price` 1 row → Tỷ suất LN + Cấp duyệt update.
  - [ ] Đổi `vat_percent` 1 row → Tỷ suất LN + Cấp duyệt **KHÔNG đổi**. Row TỔNG Tiền VAT + Thành tiền sau VAT update.
  - [ ] Scenario: totalSale=100M VND, margin=30% → Cấp duyệt = C2. Đổi VAT=10% → vẫn C2, Tỷ suất LN vẫn 30%.

- [ ] **Task 52:** Module 5 — Show báo giá + Export + List + Tab

  - [ ] Show báo giá: 3 cột readonly + row TỔNG đủ 2 cell mới + footer ngoài không thêm gì.
  - [ ] Xuất Excel: 3 cột mới + 2 dòng footer "Tổng VAT"/"Tổng sau VAT" + CON blank.
  - [ ] List báo giá: cột "Tổng sau VAT" = `total_sale + total_vat`. Column customization toggle OK.
  - [ ] Tab "Báo giá" dự án: cột "Tổng sau VAT" đúng.

- [ ] **Task 53:** Module 6 — History + Edge cases

  - [ ] Sau mỗi lần bulk apply (toolbar hoặc soft-prompt), mở QuotationHistoryModal → thấy entry `action=update_vat_bulk` với meta đủ 5 key.
  - [ ] User quyền "Xây dựng giá" nhưng không phải creator → mở edit → toolbar + input disabled.
  - [ ] User NV KD (`can_view_import_price=false`) → mở show báo giá → vẫn thấy VAT%, Tiền VAT, Thành tiền sau VAT (không gate).
  - [ ] Báo giá không có dòng nào (edge case rỗng) → không crash.
  - [ ] Báo giá toàn CHA-có-CON: totalSale từ CHA roll-up, VAT áp CHA đúng, CON luôn VAT=0.

**Tất cả module pass → Phase 12 Done. Wrap up + cập nhật STATUS.**

---

## 12.9 — Cấu hình Tỷ suất lợi nhuận mức sàn + cảnh báo màu (Batch 11) (6 tasks)

**Yêu cầu bổ sung (2026-04-19):** Thêm cấu hình "Tỷ suất lợi nhuận mức sàn: %" tại Cấu hình > Cấu hình chung > Tab "Quản lý dự án" (panel bên phải, bên trái là priority card). Tại màn báo giá (edit + show): nếu margin per-row hoặc margin tổng < mức sàn → text đỏ; ≥ mức sàn → text xanh. Bỏ tier vàng hiện có.

- [x] **Task 58:** BE migration `2026_04_19_100003_add_profit_margin_threshold_to_general_regulations.php`
  ```php
  Schema::table('general_regulations', function (Blueprint $t) {
      $t->decimal('profit_margin_threshold', 5, 2)->default(0)->nullable()
        ->after('map_provider_type')
        ->comment('Tỷ suất lợi nhuận mức sàn (%) — dưới mức này cảnh báo đỏ trên báo giá');
  });
  ```
  Chạy `php artisan migrate`, verify schema.

- [x] **Task 59:** BE update entity + service/controller `GeneralRegulation`:
  - Đọc file `Modules/Timesheet/Entities/GeneralRegulation.php` (hoặc grep để xác định đúng module).
  - Thêm cast `'profit_margin_threshold' => 'decimal:2'` (giữ `$guarded=[]` nếu có).
  - Update controller endpoint `POST /api/v1/general-regulations/` accept field `profit_margin_threshold`.
  - Transformer / response trả field này.

- [x] **Task 60:** FE config `pages/assign/settings/index.vue` — thêm panel bên phải:
  - Trong tab `b-tab title="Cấu hình mức độ ưu tiên"` (dòng ~771), bên trong `<div class="row">`, đổi `col-9` hiện có thành `col-9` giữ nguyên, thêm `<div class="col-3">` bên phải:
    ```html
    <div class="col-3">
        <div class="card">
            <div class="card-body p-3">
                <V2BaseChip>
                    <i class="ri-percent-line"></i>
                    Tỷ suất lợi nhuận mức sàn
                </V2BaseChip>
                <div class="mt-3">
                    <V2BaseLabel>Tỷ suất lợi nhuận mức sàn (%)</V2BaseLabel>
                    <V2BaseInput
                        v-model="profitMarginThreshold"
                        type="number"
                        min="0"
                        max="100"
                        step="0.01"
                        placeholder="VD: 15"
                    />
                    <small class="help-text">Dưới mức này, báo giá sẽ hiện cảnh báo đỏ.</small>
                </div>
                <V2BaseButton primary size="sm" class="mt-3" @click="saveProfitMarginThreshold">
                    Lưu
                </V2BaseButton>
            </div>
        </div>
    </div>
    ```
  - Data: `profitMarginThreshold: 0`.
  - `mounted`: load từ `GET /api/v1/general-regulations/` → set `this.profitMarginThreshold = res.data.data?.profit_margin_threshold ?? 0`.
  - `saveProfitMarginThreshold()`: `POST /api/v1/general-regulations/` với body `{ profit_margin_threshold: this.profitMarginThreshold }` + toast success.

- [x] **Task 61:** FE `store/actions.js` — load threshold vào vuex khi nuxtClientInit:
  - Trong block `/api/v1/general-regulations/` (đã có sẵn load `map_provider_type`), thêm commit:
    ```js
    commit(SET_STATE, {
        key: 'profit_margin_threshold',
        value: Number(res.data.data?.profit_margin_threshold ?? 0),
    })
    ```
  - Trong `store/state.js`, thêm `profit_margin_threshold: 0`.

- [x] **Task 62:** FE `pages/assign/quotations/_id/edit.vue` — update `marginColorClass`:
  ```js
  marginColorClass(m) {
      if (m === null || m === undefined) return 'text-muted'
      const threshold = Number(this.$store.state.profit_margin_threshold || 0)
      return Number(m) < threshold ? 'text-danger' : 'text-success'
  },
  ```
  Bỏ tier `text-warning` (user spec chỉ 2 màu: đỏ / xanh).

- [x] **Task 63:** FE `pages/assign/quotations/_id/index.vue` (show) — update `marginColorClass` tương tự Task 62.

- [x] **Task 64:** Smoke test compile + verify logic:
  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && node -e "\
  const c=require('vue-template-compiler'),fs=require('fs');\
  for (const f of [\
    'pages/assign/settings/index.vue',\
    'pages/assign/quotations/_id/edit.vue',\
    'pages/assign/quotations/_id/index.vue']) {\
    const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
    const r=p.template?c.compile(p.template.content):null;\
    console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');\
  }"
  ```
  Expected: 3 dòng đều OK 0 errs.

---

## 12.8 — Bổ sung thông tin khách hàng / liên hệ (Batch 10) (4 tasks)

**Yêu cầu bổ sung (2026-04-19):** Thêm 3 trường MST + Người liên hệ + SĐT liên hệ vào màn báo giá (create/edit/show/approve). Thông tin lấy từ Dự án TKT (đã snapshot ở BE, chỉ bổ sung display FE). Dự án TKT: "Người liên hệ" thành required.

**BE đã có sẵn** (verify): `QuotationService::createFromRequest` đã snapshot `customer_tax_code`, `customer_contact_name`, `customer_contact_phone` từ prospective_project sang quotations. Không cần sửa BE.

- [x] **Task 54:** FE `pages/assign/quotations/_id/edit.vue` — thêm 3 row vào info table (hiện tại chỉ có "Khách hàng"):
  ```html
  <tr>
      <th>Khách hàng</th>
      <td colspan="3">{{ item.customer_name || '—' }}</td>
  </tr>
  <!-- NEW 3 rows -->
  <tr>
      <th>MST</th>
      <td>{{ item.customer_tax_code || '—' }}</td>
      <th>Địa chỉ</th>
      <td>{{ item.customer_address || '—' }}</td>
  </tr>
  <tr>
      <th>Người liên hệ</th>
      <td>{{ item.customer_contact_name || '—' }}</td>
      <th>SĐT liên hệ</th>
      <td>{{ item.customer_contact_phone || '—' }}</td>
  </tr>
  ```
  Nếu info table đã có cột "Địa chỉ" sẵn thì chỉ thêm MST / Người liên hệ / SĐT liên hệ — adjust theo layout hiện có.

- [x] **Task 55:** FE `pages/assign/quotations/_id/index.vue` (show báo giá) — rename 2 label:
  - `<th>Liên hệ</th>` → `<th>Người liên hệ</th>`
  - `<th>SĐT</th>` → `<th>SĐT liên hệ</th>`
  - "MST" giữ nguyên.

- [x] **Task 56:** FE `components/CustomerInfoSection.vue` + form validation — mark "Người liên hệ" required:
  - `<V2BaseLabel required>Người liên hệ</V2BaseLabel>` + `<V2BaseError v-if="formError.customer_contact_id" ...>` (dùng prop `required` sẵn có của V2BaseLabel, đồng nhất pattern field "Khách hàng" cùng file).
  - `add.vue` + `_id/edit.vue` (project TKT): `submitForm()` thêm validate `customer_contact_id` không rỗng + toast error + set `formError.customer_contact_id`. Validation áp cả "Lưu nháp" và "Gửi duyệt" (confirmed 2026-04-19) — đảm bảo Project TKT luôn có contact → snapshot sang Quotation luôn đầy đủ.
  - `_id/manager.vue` KHÔNG áp dụng: file này là màn **xem chi tiết (view-only)**, tất cả tab con `:disabled="true"`, không có submit method. Create/edit project đi qua `add.vue` + `_id/edit.vue` (đã validate).

- [x] **Task 57:** Smoke test compile SFC:
  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && \
  node -e "const c=require('vue-template-compiler'),fs=require('fs');\
  for (const f of [\
    'pages/assign/quotations/_id/edit.vue',\
    'pages/assign/quotations/_id/index.vue',\
    'pages/assign/prospective-projects/components/CustomerInfoSection.vue',\
    'pages/assign/prospective-projects/add.vue',\
    'pages/assign/prospective-projects/_id/edit.vue']) {\
    const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
    const r=p.template?c.compile(p.template.content):null;\
    console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');\
  }"
  ```
  Expected: 5 dòng, mỗi dòng `tpl: OK script: OK errs: 0`.

---

## Checkpoints

### Checkpoint — 2026-04-19
Vừa hoàn thành: Design + Plan Phase 12 (design-phase12-vat.md + plan-phase12.md). Branch đã chuyển sang `tpe-develop-assign`.
Đang làm dở: Không.
Bước tiếp theo: Bắt đầu Task 1 (migration VAT) khi user xác nhận.
Blocked: Không.

### Checkpoint — 2026-04-19 (Batch 8 FE)
Vừa hoàn thành: Task 42-47 — Update 3 màn (show báo giá, list báo giá, tab dự án tiền khả thi).
- `pages/assign/quotations/_id/index.vue`: thêm 3 cột VAT readonly + row TỔNG 2 cell mới (Tiền VAT, Tổng sau VAT) + methods `lineSaleTotal`, `lineVatAmount`, `lineAfterVat` + computed `totalVat`, `totalAfterVat`. Compile pass 0 errors.
- `pages/assign/quotations/index.vue`: thêm cột `total_after_vat_fmt` sau "Tổng giá trị" vào `defaultTableColumns` + slot `#cell-total_after_vat_fmt` fallback `item.total_sale` khi chưa có VAT. Compile pass 0 errors.
- `ProspectiveProjectQuotationsTab.vue`: tab không có cột "Tổng bán" — thêm mới cả 2 cột (Tổng bán + Tổng sau VAT) trước cột "Ngày duyệt" + slot render + method `formatMoney`. Compile pass 0 errors.
Đang làm dở: Không.
Bước tiếp theo: User quyết định test thủ công end-to-end (Task 48-53) hay xử lý batch tiếp.
Blocked: Không.

### Checkpoint — 2026-04-19 (Wrap up session — Batch 10 + 11 + docs)
Vừa hoàn thành:
- **Batch 10 (Task 54-57 DONE):** Customer info trên báo giá.
  - `edit.vue` thêm 2 row (MST+Địa chỉ, Người liên hệ+SĐT liên hệ) vào info table.
  - `_id/index.vue` (show): rename "Liên hệ"→"Người liên hệ", "SĐT"→"SĐT liên hệ".
  - `CustomerInfoSection.vue`: `<V2BaseLabel required>Người liên hệ</V2BaseLabel>` + V2BaseError.
  - `add.vue` + `_id/edit.vue` project TKT: validate `customer_contact_id` ở đầu submitForm (áp cả lưu nháp + gửi duyệt).
  - `manager.vue` skip (view-only, all tabs disabled).
- **Batch 11 (Task 58-64 DONE):** Profit margin threshold.
  - Migration `2026_04_19_100003_add_profit_margin_threshold_to_general_regulations`.
  - `GeneralRegulation` entity + controller + service + resource: accept + validate 0-100% + trả float.
  - `settings/index.vue`: col-3 panel mới bên phải priority card (tab Quản lý dự án > Cấu hình mức độ ưu tiên): input % + button Lưu.
  - `store/actions.js` + `state.js`: nuxtClientInit commit `profit_margin_threshold`.
  - `edit.vue` + `_id/index.vue` quotation: `marginColorClass` đổi 2 tier (đỏ/xanh) dùng `$store.state.profit_margin_threshold`, bỏ tier vàng.
- **Backfill script (tinker 1-lần):** Copy `customer_tax_code/address/contact_name/contact_phone` từ `prospective_projects` sang 2 quotation (id=3, id=4) trên local để fix snapshot rỗng. Production KHÔNG chạy (giữ immutability).
- **Docs:** Tạo `docs/srs/bao-gia-flow.html` + `docs/srs/bao-gia-flow.pdf` (3 trang A4) — flow YCBG → Quotation → Duyệt, 2 bảng tham chiếu trạng thái + cấp duyệt, cảnh báo margin threshold.

Đang làm dở: Không.

Bước tiếp theo:
1. User test manual end-to-end 6 module (Task 48-53):
   - Module 1 Roll-up CHA-CON logic
   - Module 2 Soft-prompt VAT
   - Module 3 Toolbar bulk apply
   - Module 4 Totals + margin (trước VAT) + cấp duyệt
   - Module 5 Show + Export Excel + List + Tab
   - Module 6 History + edge cases
2. Test bổ sung:
   - Project TKT validate Người liên hệ required (tạo mới + sửa)
   - Báo giá hiển thị MST + Người liên hệ + SĐT liên hệ đủ
   - Cấu hình mức sàn lợi nhuận + cảnh báo màu trên báo giá
3. Nếu có bug → dispatch fix.

Blocked: Không.

---

## Checkpoint template (tham khảo)

```markdown
### Checkpoint — YYYY-MM-DD
Vừa hoàn thành: [task X]
Đang làm dở: [file + line + dừng đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```

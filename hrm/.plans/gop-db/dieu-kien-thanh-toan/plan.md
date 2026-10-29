# Điều kiện thanh toán cho Tiến độ thanh toán HĐ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:executing-plans (hoặc subagent-driven-development) để triển khai từng task. Các bước dùng checkbox `- [ ]`.

**Goal:** Dựng danh mục điều kiện thanh toán cố định (8 giá trị, global) và cho mỗi dòng Tiến độ thanh toán HĐ bán (module Assign) chọn 1 điều kiện + nhập "số ngày bắt đầu tính thanh toán", lưu bền vào hợp đồng.

**Architecture:** Bảng danh mục riêng `payment_conditions` seed cố định + 2 cột mới (`payment_condition_id`, `offset_days`) trên `hrm_contract_process_payments`. BE: 1 route lẻ trả danh mục (khuôn `company-accounts`), validate + ghi ở `ContractService`, Resource trả kèm tên điều kiện (eager-load chống N+1). FE: thêm 2 cột vào component dùng chung `ContractPaymentTermsTable.vue`, `edit.vue` nạp options 1 lần truyền xuống (áp cả Tạo + Sửa qua `create.vue extends edit.vue`).

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt2/Vue2 + Bootstrap-Vue + V2Base* (hrm-client), MySQL `erp_hrm_check` (local).

**Spec:** `docs/superpowers/specs/gop-db/2026-10-16-dieu-kien-thanh-toan-design.md`

**Phụ trách:** @dangquang.tom · **Nhánh:** `develop` (gop_db) — cả hrm-api + hrm-client.

## Global Constraints

- **Nhánh gop_db**: KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`. Bảng mới không trùng tên bảng gộp (đã verify). Tài liệu ở `.plans/gop-db/`, spec ở `docs/superpowers/specs/gop-db/`.
- **KHÔNG commit/push khi chưa được yêu cầu.** Mỗi task xong chỉ dừng ở mức code + tự kiểm; không git.
- **Model mới BẮT BUỘC `extends BaseModel`** (`use App\Models\BaseModel;`), `created_by`/`updated_by` nằm trong `$fillable`, luôn `auth()->id()`.
- **Không bắt buộc nhập** đợt này: 2 cột `nullable`, FormRequest dùng `nullable`, KHÔNG thêm `required`, KHÔNG khai `messages()` (câu chuẩn đã có ở lang file).
- **FE màn này dùng component dùng chung `ContractPaymentTermsTable.vue`** — chỉ dùng `V2Base*`, không HTML thô. `grep` tự kiểm phần thêm mới không có `<input>/<select>/<button>` thô.
- **KHÔNG tự sửa giá trị user vừa nhập**; số định dạng quốc tế (`,` nghìn, `.` thập phân) — nhưng `offset_days` là số nguyên ngày, dùng `V2BaseInput` số, không cần `V2BaseCurrencyInput`.
- **Số**: `offset_days` là số nguyên ≥ 0.
- **Verification của codebase này** = migrate + tinker/DB query + gọi HTTP API thật + Playwright MCP (`http://127.0.0.1:3000`), KHÔNG phải PHPUnit (dự án không chạy unit test BE cho luồng này). Mỗi task kết thúc bằng lệnh/kiểm tra cụ thể + so với kết quả mong đợi.

## Review Focus

1. **HĐ cũ có dòng tiến độ nhưng `payment_condition_id`/`offset_days` NULL** → mở Sửa phải render ô trống, Lưu lại không mất dữ liệu cũ (replace-all create với `?? null`). Pin ở Task 4 + Task 7.
2. **Gửi `payment_condition_id` là id lạ** (không có trong `payment_conditions`) → `exists` trả 422, không ghi rác. Pin ở Task 4 (bước kiểm 422).
3. **`offset_days = -1` hoặc chuỗi** → `integer|min:0` chặn 422 kể cả khi Lưu nháp (rule định dạng luôn bật). Pin ở Task 4 (bước kiểm 422).
4. **Options chưa kịp nạp khi mở Sửa** → giá trị đã chọn vẫn hiển thị nhờ Resource trả `payment_condition_name`; FE merge option đang chọn vào list nếu thiếu. Pin ở Task 6.
5. **Component nhúng ở nơi khác không truyền `conditionOptions`** → prop default `[]`, dropdown rỗng nhưng không vỡ. Pin ở Task 5 (default prop) + grep xác nhận chỉ `edit.vue` nhúng.

---

## Task 1: Bảng danh mục `payment_conditions` + Model + Seeder 8 giá trị

**Files:**
- Create: `hrm-api/database/migrations/2026_10_16_000001_create_payment_conditions_table.php`
- Create: `hrm-api/Modules/Assign/Entities/PaymentCondition.php`
- Create: `hrm-api/Modules/Assign/Database/Seeders/PaymentConditionsTableSeeder.php`

**Interfaces:**
- Produces: bảng `payment_conditions(id, code, name, sort_order, is_active, created_by, updated_by, created_at, updated_at)`; model `Modules\Assign\Entities\PaymentCondition` với `getForSelect(): array` trả `[{id, code, name}]` (active, sort theo `sort_order`); seeder `PaymentConditionsTableSeeder` idempotent nạp 8 dòng theo bảng mã trong spec §4.3.

- [x] **Step 1: Viết migration bảng danh mục**

```php
<?php
// hrm-api/database/migrations/2026_10_16_000001_create_payment_conditions_table.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreatePaymentConditionsTable extends Migration
{
    /** Danh mục điều kiện thanh toán (global, cố định) — nền tảng cho Tiến độ thanh toán HĐ. */
    public function up()
    {
        Schema::create('payment_conditions', function (Blueprint $table) {
            $table->id();
            $table->string('code', 30)->unique();
            $table->string('name', 191);
            $table->integer('sort_order')->default(0);
            $table->boolean('is_active')->default(true);
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
            $table->index('is_active');
        });
    }

    public function down()
    {
        Schema::dropIfExists('payment_conditions');
    }
}
```

- [x] **Step 2: Chạy migration, xác nhận bảng tạo được**

Run: `cd hrm-api && php artisan migrate --path=database/migrations/2026_10_16_000001_create_payment_conditions_table.php`
Expected: `Migrated:` (không lỗi). Kiểm cột: `php artisan tinker --execute="echo implode(',', \Illuminate\Support\Facades\Schema::getColumnListing('payment_conditions'));"` → in đủ `id,code,name,sort_order,is_active,created_by,updated_by,created_at,updated_at`.

- [x] **Step 3: Viết model `PaymentCondition`**

```php
<?php
// hrm-api/Modules/Assign/Entities/PaymentCondition.php
namespace Modules\Assign\Entities;

use App\Models\BaseModel;

class PaymentCondition extends BaseModel
{
    protected $table = 'payment_conditions';

    protected $fillable = ['code', 'name', 'sort_order', 'is_active', 'created_by', 'updated_by'];

    /** Danh mục cho dropdown: chỉ điều kiện đang hoạt động, theo thứ tự hiển thị. */
    public static function getForSelect(): array
    {
        return self::where('is_active', 1)
            ->orderBy('sort_order')
            ->get(['id', 'code', 'name'])
            ->toArray();
    }
}
```

- [x] **Step 4: Viết seeder idempotent 8 giá trị**

```php
<?php
// hrm-api/Modules/Assign/Database/Seeders/PaymentConditionsTableSeeder.php
namespace Modules\Assign\Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PaymentConditionsTableSeeder extends Seeder
{
    public function run()
    {
        $now = now();
        $rows = [
            ['sort_order' => 1, 'code' => 'KY_NGAY_KY',     'name' => 'Kể từ ngày ký'],
            ['sort_order' => 2, 'code' => 'HIEU_LUC',       'name' => 'Kể từ ngày hợp đồng có hiệu lực'],
            ['sort_order' => 3, 'code' => 'DUYET_THIET_KE', 'name' => 'Phê duyệt thiết kế'],
            ['sort_order' => 4, 'code' => 'GIAO_HANG_1',    'name' => 'Giao hàng lần 1 có chữ ký của KH'],
            ['sort_order' => 5, 'code' => 'GIAO_HANG_2',    'name' => 'Giao hàng lần 2 có chữ ký của KH'],
            ['sort_order' => 6, 'code' => 'LAP_DAT',        'name' => 'Lắp đặt có chữ ký của KH'],
            ['sort_order' => 7, 'code' => 'CHAY_THU',       'name' => 'Chạy thử Có chữ ký KH'],
            ['sort_order' => 8, 'code' => 'NGHIEM_THU',     'name' => 'Bàn giao nghiệm thu'],
        ];

        foreach ($rows as $row) {
            DB::table('payment_conditions')->updateOrInsert(
                ['code' => $row['code']],
                [
                    'name'       => $row['name'],
                    'sort_order' => $row['sort_order'],
                    'is_active'  => 1,
                    'updated_at' => $now,
                    'created_at' => $now,
                ]
            );
        }
    }
}
```

- [x] **Step 5: Chạy seeder 2 lần, xác nhận idempotent + 8 dòng**

Run: `cd hrm-api && php artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder" && php artisan db:seed --class="Modules\Assign\Database\Seeders\PaymentConditionsTableSeeder"`
Then: `php artisan tinker --execute="echo \Modules\Assign\Entities\PaymentCondition::count(); echo ' | '; print_r(array_column(\Modules\Assign\Entities\PaymentCondition::getForSelect(),'name'));"`
Expected: count = **8** (không nhân đôi sau 2 lần seed), danh sách tên đúng 8 giá trị theo đúng thứ tự `sort_order`.

---

## Task 2: 2 cột mới trên `hrm_contract_process_payments` + quan hệ belongsTo

**Files:**
- Create: `hrm-api/database/migrations/2026_10_16_000002_add_payment_condition_to_hrm_contract_process_payments.php`
- Modify: `hrm-api/Modules/Assign/Entities/Contract/ContractProcessPayment.php`

**Interfaces:**
- Consumes: bảng `payment_conditions` (Task 1), model `Modules\Assign\Entities\PaymentCondition`.
- Produces: cột `hrm_contract_process_payments.payment_condition_id` (unsignedBigInteger nullable, index) + `offset_days` (int nullable); quan hệ `ContractProcessPayment::paymentCondition()` belongsTo `PaymentCondition` theo khoá `payment_condition_id`.

- [x] **Step 1: Viết migration 2 cột**

```php
<?php
// hrm-api/database/migrations/2026_10_16_000002_add_payment_condition_to_hrm_contract_process_payments.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddPaymentConditionToHrmContractProcessPayments extends Migration
{
    /** Thêm điều kiện thanh toán + số ngày bắt đầu tính thanh toán cho từng đợt tiến độ. */
    public function up()
    {
        Schema::table('hrm_contract_process_payments', function (Blueprint $table) {
            $table->unsignedBigInteger('payment_condition_id')->nullable()->after('milestone');
            $table->integer('offset_days')->nullable()->after('payment_condition_id');
            $table->index('payment_condition_id');
        });
    }

    public function down()
    {
        Schema::table('hrm_contract_process_payments', function (Blueprint $table) {
            $table->dropIndex(['payment_condition_id']);
            $table->dropColumn(['payment_condition_id', 'offset_days']);
        });
    }
}
```

- [x] **Step 2: Chạy migration, xác nhận 2 cột tồn tại**

Run: `cd hrm-api && php artisan migrate --path=database/migrations/2026_10_16_000002_add_payment_condition_to_hrm_contract_process_payments.php`
Then: `php artisan tinker --execute="echo \Illuminate\Support\Facades\Schema::hasColumn('hrm_contract_process_payments','payment_condition_id') ? 'yes':'no'; echo \Illuminate\Support\Facades\Schema::hasColumn('hrm_contract_process_payments','offset_days') ? ' yes':' no';"`
Expected: `yes yes`.

- [x] **Step 3: Thêm quan hệ belongsTo vào model (giữ nguyên phần còn lại)**

Mở `ContractProcessPayment.php`, thêm `use Modules\Assign\Entities\PaymentCondition;` (nếu chưa có) và method:

```php
public function paymentCondition()
{
    return $this->belongsTo(\Modules\Assign\Entities\PaymentCondition::class, 'payment_condition_id');
}
```

- [x] **Step 4: Xác nhận quan hệ load được (chưa có data cũng không lỗi)**

Run: `cd hrm-api && php artisan tinker --execute="\$m = new \Modules\Assign\Entities\Contract\ContractProcessPayment(); echo get_class(\$m->paymentCondition());"`
Expected: in `Illuminate\Database\Eloquent\Relations\BelongsTo` (không exception).

---

## Task 3: BE — endpoint danh mục `GET assign/payment-conditions`

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (thêm route trong group `/assign/contracts`, TRƯỚC route `/{id}` dòng 826)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php` (thêm method `paymentConditions`)

**Interfaces:**
- Consumes: `PaymentCondition::getForSelect()` (Task 1).
- Produces: `GET assign/payment-conditions` → JSON `{ data: [{id, code, name}, ...] }` (8 dòng, không phân trang, không gắn checkPermission — khuôn các danh mục lẻ `company-accounts`).

- [x] **Step 1: Thêm method vào `ContractController`**

Đặt cạnh các method danh mục lẻ (`companyAccounts`, `customerDeputies`). Dùng `use Modules\Assign\Entities\PaymentCondition;` ở đầu file nếu chưa có.

```php
/** Danh mục điều kiện thanh toán cho dropdown Tiến độ thanh toán HĐ. */
public function paymentConditions()
{
    return response()->json(['data' => PaymentCondition::getForSelect()]);
}
```

> Format trả `{data: [...]}` khớp cách FE đọc các danh mục lẻ khác của màn (kiểm nhanh `companyAccounts` để mirror đúng key — nếu `companyAccounts` trả mảng trần thì trả mảng trần cho đồng bộ; ghi ruling vào ledger nếu lệch).

- [x] **Step 2: Thêm route (TRƯỚC `/{id}` để không bị nuốt thành id)**

Chèn sau dòng 825 (`customer-bank-accounts`), trước dòng 826 (`/{id}`):

```php
// Danh mục điều kiện thanh toán cho Tiến độ thanh toán — PHẢI đứng trước /{id}
Route::get('/payment-conditions', [ContractController::class, 'paymentConditions']);
```

- [x] **Step 3: Gọi API thật, xác nhận trả 8 điều kiện**

Lấy token JWT của emp đang test (hoặc dùng session Playwright). Gọi:
`curl -s -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/assign/payment-conditions`
Expected: HTTP 200, JSON chứa 8 phần tử, mỗi phần tử có `id`, `code`, `name`; `code` đầu tiên = `KY_NGAY_KY`.

---

## Task 4: BE — validate 2 FormRequest + ghi dữ liệu ContractService (store + update) + Resource

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/ContractStoreRequest.php` (~dòng 99, khối `process_payments.*`)
- Modify: `hrm-api/Modules/Assign/Http/Requests/ContractUpdateRequest.php` (~dòng 107, khối `process_payments.*`)
- Modify: `hrm-api/Modules/Assign/Services/ContractService.php` (store `:328-336`, update `:466-476`)
- Modify: Resource chi tiết HĐ `DetailContractResource.php` (key `processPayments`) + điểm eager-load `with('paymentCondition')` khi load HĐ chi tiết (trong `ContractService::show`/`ContractController::show` — xác định đúng chỗ build detail)

**Interfaces:**
- Consumes: cột `payment_condition_id`, `offset_days` (Task 2); quan hệ `paymentCondition()` (Task 2).
- Produces: payload `process_payments.*` nhận thêm 2 field có validate; dòng tiến độ lưu kèm 2 field; Resource trả thêm `payment_condition_id`, `offset_days`, `payment_condition_name`.

- [x] **Step 1: Thêm rule vào `ContractStoreRequest` (trong khối `process_payments.*`, KHÔNG khai messages)**

```php
'process_payments.*.payment_condition_id' => 'nullable|integer|exists:payment_conditions,id',
'process_payments.*.offset_days'          => 'nullable|integer|min:0',
```

- [x] **Step 2: Thêm rule y hệt vào `ContractUpdateRequest`**

(Cùng 2 dòng trên, trong khối `process_payments.*` của request update.)

- [x] **Step 3: Thêm 2 field vào mảng create của ContractService — CẢ store và update**

Tại store (`:328-336`) và update (`:466-476`), trong mảng `ContractProcessPayment::create([...])` thêm:

```php
'payment_condition_id' => $pp['payment_condition_id'] ?? null,
'offset_days'          => $pp['offset_days'] ?? null,
```

(Giữ nguyên cấu trúc replace-all; `?? null` để HĐ cũ không có field vẫn chạy.)

- [x] **Step 4: Resource trả thêm 3 field + eager-load**

Trong `DetailContractResource` (phần map `processPayments`), thêm cho mỗi dòng:

```php
'payment_condition_id'   => $pp->payment_condition_id,
'offset_days'            => $pp->offset_days,
'payment_condition_name' => optional($pp->paymentCondition)->name,
```

> PHP 7.4 không có `?->` — dùng `optional()`.

Tại chỗ load HĐ chi tiết (eager-load quan hệ `processPayments`), thêm `.with('paymentCondition')` hoặc `processPayments.paymentCondition` vào danh sách `with()` để tránh N+1.

- [x] **Step 5: Kiểm POST tạo HĐ hợp lệ + đọc lại chi tiết**

Gọi `POST assign/contracts` (hoặc `PUT` 1 HĐ Đang tạo của mình) với `process_payments` có 1 dòng kèm `payment_condition_id` (1 id hợp lệ từ Task 3) + `offset_days: 15`. Sau đó `GET assign/contracts/{id}`.
Expected: dòng tiến độ trả về có `payment_condition_id`, `offset_days=15`, `payment_condition_name` khớp tên điều kiện. Không N+1 (log query 1 lần cho paymentCondition).

- [x] **Step 6: Kiểm chặn 422 (Review Focus 2 + 3)**

Gọi lại với: (a) `payment_condition_id` = 999999 (id lạ) → Expected 422, lỗi tại `process_payments.0.payment_condition_id`. (b) `offset_days` = -1 → Expected 422 tại `process_payments.0.offset_days`. (c) `offset_days` = "abc" → Expected 422.

- [x] **Step 7: Kiểm HĐ cũ không mất dữ liệu (Review Focus 1)**

Lấy 1 HĐ cũ đang ở trạng thái Đang tạo (do mình lập) có sẵn dòng tiến độ nhưng chưa có điều kiện. `GET` chi tiết → 2 field mới = null. `PUT` lại nguyên payload đọc được (2 field null) → `GET` lại: các dòng tiến độ + số tiền/% giữ nguyên, không lỗi.

---

## Task 5: FE — thêm 2 cột vào `ContractPaymentTermsTable.vue`

**Files:**
- Modify: `hrm-client/components/ContractPaymentTermsTable.vue`

**Interfaces:**
- Consumes: Resource trả `payment_condition_id`, `offset_days`, `payment_condition_name` (Task 4); prop `conditionOptions` do cha truyền (Task 6).
- Produces: component hiển thị + sửa được 2 cột mới; `addRow()` khởi tạo `payment_condition_id: null, offset_days: null`; mỗi dòng object giữ 2 field này để `buildPayload` của cha gửi BE.

- [x] **Step 1: Thêm prop `conditionOptions` (default `[]` — Review Focus 5)**

Trong khối `props` (dòng ~123-138), thêm:

```js
conditionOptions: { type: Array, default: () => [] },
```

- [x] **Step 2: `addRow()` thêm 2 field mặc định**

Trong object push của `addRow()` (dòng ~186-199), thêm `payment_condition_id: null, offset_days: null` (giữ nguyên các field cũ gồm `milestone`, `deadline`).

- [x] **Step 3: Thêm 2 `<th>` vào thead (đúng thứ tự ảnh)**

Chèn giữa cột "Số tiền thanh toán" và "Nội dung bổ sung": `<th>Điều kiện thanh toán</th>` và `<th>Số ngày bắt đầu tính thanh toán</th>`. Không in đậm chữ ô (theo convention).

- [x] **Step 4: Thêm 2 `<td>` tương ứng mỗi dòng — dùng V2Base***

Cột Điều kiện (V2BaseSelect, hiển thị theo `name`):

```vue
<td>
  <V2BaseSelect
    :value="row.payment_condition_id"
    :options="conditionOptions"
    :reduce="(o) => o.id"
    label="name"
    :disabled="disabled"
    placeholder="Chọn điều kiện thanh toán"
    size="sm"
    @input="updateField(index, 'payment_condition_id', $event)"
  />
</td>
```

Cột Số ngày (V2BaseInput số nguyên ≥ 0, KHÔNG bắt buộc):

```vue
<td>
  <V2BaseInput
    :value="row.offset_days"
    type="number"
    min="0"
    :disabled="disabled"
    size="sm"
    @input="updateField(index, 'offset_days', $event)"
  />
</td>
```

> Khớp đúng chữ ký `V2BaseSelect`/`V2BaseInput`/`updateField` đang dùng trong chính component này (đọc cột `payment_type`/`note` hiện có để mirror prop `reduce`/`label`/`@input`). Nếu `V2BaseSelect` trong component này đang dùng prop khác (vd `:value-field`/`:text-field`) thì theo đúng cái đang dùng, ghi ruling.

- [x] **Step 5: Tự kiểm không HTML thô ở phần thêm mới**

Run: `cd hrm-client && grep -nE '<input |<select |<button |<textarea |class="form-control"' components/ContractPaymentTermsTable.vue | grep -v V2Base`
Expected: không ra dòng nào thuộc 2 cột vừa thêm (các dòng cũ của component nếu có thì không phát sinh từ task này).

---

## Task 6: FE — `edit.vue` nạp options + truyền prop + map buildPayload

**Files:**
- Modify: `hrm-client/pages/assign/contracts/_id/edit.vue`

**Interfaces:**
- Consumes: endpoint `GET assign/payment-conditions` (Task 3); component prop `conditionOptions` (Task 5); Resource field `payment_condition_name` (Task 4).
- Produces: data `paymentConditionOptions`; HĐ gửi BE kèm `payment_condition_id` + `offset_days` cho mỗi `process_payments`; đọc về giữ nguyên 2 field; merge option đang chọn nếu thiếu.

- [x] **Step 1: Khai data `paymentConditionOptions: []`**

Trong `data()` cạnh `processPayments` (dòng ~629).

- [x] **Step 2: Nạp danh mục 1 lần khi mở màn**

Trong `mounted()` (dòng ~813-826), gọi 1 lần (cạnh `fetchCompanyAccounts` dòng 822):

```js
this.$store.dispatch('apiGetMethod', 'assign/payment-conditions').then((res) => {
  this.paymentConditionOptions = (res && res.data) ? res.data : []
}).catch(() => { this.paymentConditionOptions = [] })
```

> Mirror đúng cách các danh mục lẻ khác đọc response (`res.data` vs `res`). Áp cho cả Tạo + Sửa vì nằm ở `mounted` dùng chung.

- [x] **Step 3: Truyền prop xuống component (dòng 414)**

```vue
<ContractPaymentTermsTable
  v-model="processPayments"
  :contract-total="Number(contract.total_after_vat) || 0"
  :condition-options="paymentConditionOptions"
/>
```

- [x] **Step 4: Đọc về — merge option đang chọn nếu thiếu (Review Focus 4)**

Tại dòng đọc `processPayments` (dòng ~1287), sau khi map, với mỗi dòng có `payment_condition_id` mà không nằm trong `paymentConditionOptions` và có `payment_condition_name` → push `{id: payment_condition_id, name: payment_condition_name}` vào `paymentConditionOptions`. (Đợt này 8 giá trị đều active nên hiếm xảy ra, nhưng giữ để an toàn khi về sau có khoá.)

- [x] **Step 5: Map gửi BE (buildPayload dòng ~1404-1416)**

Thêm vào object map mỗi `process_payments`:

```js
payment_condition_id: pp.payment_condition_id ?? null,
offset_days: (pp.offset_days === '' || pp.offset_days == null) ? null : Number(pp.offset_days),
```

(Giữ nguyên các field cũ `milestone`, `deadline`, `sort_order`…)

- [x] **Step 6: Build FE không lỗi**

Run: `cd hrm-client && grep -n "payment-conditions\|paymentConditionOptions\|condition-options" pages/assign/contracts/_id/edit.vue`
Expected: thấy đủ 3 điểm (gọi API, data, truyền prop). Không còn placeholder.

---

## Task 7: Kiểm thử end-to-end (BE API + FE Playwright)

**Files:** (không sửa — chỉ verify; nếu phát hiện lỗi thì quay lại task tương ứng)

- [x] **Step 1: Playwright MCP — màn Sửa HĐ**

Mở `http://127.0.0.1:3000`, vào 1 HĐ Đang tạo (do mình lập) → Sửa → tab "Điều khoản thanh toán".
Expected: bảng Tiến độ thanh toán có 2 cột mới ("Điều kiện thanh toán" + "Số ngày bắt đầu tính thanh toán"); dropdown điều kiện đủ **8** giá trị đúng tên.

- [x] **Step 2: Chọn điều kiện + nhập số ngày → Lưu → mở lại**

Chọn 1 điều kiện cho 1 đợt, nhập `offset_days` (vd 30), Lưu. Sau khi về danh sách, mở lại Sửa HĐ đó.
Expected: điều kiện + số ngày hiển thị đúng giá trị vừa lưu; các cột %/số tiền không đổi.

- [x] **Step 3: Màn Tạo mới cũng có 2 cột**

Vào Lập hợp đồng mới (hoặc từ báo giá) → tab Điều khoản thanh toán → thêm 1 dòng.
Expected: dòng mới có 2 cột, dropdown 8 điều kiện, số ngày nhập được; để trống vẫn lưu được (không bắt buộc).

- [x] **Step 4: Chốt lại tự kiểm grep (toàn phần thêm mới)**

Run:
`cd hrm-client && grep -nE '<input |<select |<button |<textarea ' components/ContractPaymentTermsTable.vue | grep -v V2Base`
Expected: không ra dòng mới nào từ 2 cột vừa thêm.

---

## Ghi chú thực thi

- Local DB `erp_hrm_check` (`grep DB_ hrm-api/.env` trước khi migrate để chắc trỏ đúng DB dev, KHÔNG prod).
- API `:8000` + client `:3000` phải đang chạy để kiểm bước HTTP + Playwright.
- Chưa commit/push cho tới khi user yêu cầu.

---

### Checkpoint — 2026-10-16 (HOÀN THÀNH)
Vừa hoàn thành: Task 1–7 code + verify; final whole-branch review (subagent opus, fresh context) → 5 findings; re-grade → fix #1 Important; #2–#5 minor deferred.
Fix #1: màn Chi tiết `_id/index.vue` nhúng ContractPaymentTermsTable disabled nhưng không truyền `:condition-options` → Select2 không resolve id→tên. Sửa component tự chứa (computed `effectiveConditionOptions` push {id,name:payment_condition_name} cho row có id ngoài options). Verify node 5 ca PASS + stack thật: chèn tạm pp(contract15, id=8, offset 30) → Playwright màn Chi tiết render 'Bàn giao nghiệm thu' + offset 30 + 0 lỗi console → dọn sạch.
Đang làm dở: không.
Bước tiếp theo: chờ user xác nhận để git commit/push (chưa commit).
Blocked: không.

### Checkpoint — 2026-10-16 (đang chạy, giữ lịch sử)
Vừa hoàn thành: Task 1–7 code xong + verify. Final whole-branch review đang chạy (reviewer opus, fresh context).
Đang làm dở: chờ findings reviewer → re-grade → fix Critical/Important.
Bước tiếp theo: xử lý findings, chốt STATUS, báo user (chưa commit).
Blocked: không.

**Lệch so với plan (đã ghi Ruling ở ledger):**
- Task 7 Step 2 (full save→reload qua UI) + Step 3 (màn Tạo có 2 cột): màn Tạo `create.vue` KHÔNG có bảng tiến độ (chỉ thêm ở màn Sửa) → Step 3 ngoài phạm vi thực tế. Step 2 full UI save bị chặn bởi field bắt buộc KHÔNG liên quan feature trên HĐ test duy nhất (id15) → verify persistence qua tinker (Task 4) + buildPayload/render/merge (Task 7 Playwright). Đã khôi phục hrm_contracts.status=6 WHERE id=15.

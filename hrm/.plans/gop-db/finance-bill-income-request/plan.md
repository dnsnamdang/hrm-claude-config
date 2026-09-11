# Plan — Phiếu đề nghị thu tiền (ERP → HRM, phân hệ Tài chính)

> **For agentic workers:** dùng `superpowers:subagent-driven-development` hoặc `superpowers:executing-plans`, thực hiện task theo checkbox.
> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Spec: `docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md`

**Goal:** Port màn ERP "Phiếu đề nghị thu tiền" sang HRM phân hệ Tài chính — dùng chung bảng ERP, đổi nguồn hợp đồng bán từ `firm_contracts` sang `hrm_contracts`, không port phần Phiếu thu.

**Architecture:** BE `Modules/Finance` (Entity + Service + FormRequest + Resource + ApiController, khuôn `ProductTransferRequest` đã port). FE Nuxt 2 V2Base `pages/finance/bill-income-requests` (list + pending + form trang riêng + detail + print). Không migration, không đổi schema; chỉ thêm 5 quyền vào `PermissionsTableSeeder`.

**Tech Stack:** PHP 7.4 / Laravel 8 / `nwidart/laravel-modules` / `spatie/laravel-permission` · Nuxt 2 (Vue 2) + Bootstrap-Vue + V2Base components · MySQL DB gộp `gop_db`.

---

## Ràng buộc toàn cục (mọi task ngầm bao gồm)

- Nhánh `gop_db` ở **cả 2 repo**. **KHÔNG commit/push khi user chưa yêu cầu.**
- **KHÔNG** dùng `mysql2` / `DB_CONNECTION_SECOND` / `DB_DATABASE_SECOND`; **KHÔNG** khai `$connection` trong model. Tất cả bảng ERP đọc bằng connection mặc định.
- **KHÔNG** sửa bất kỳ file nào trong repo ERP (`D:\laragon\www\erp`) — user đã chốt.
- **KHÔNG** migration. Thay đổi DB duy nhất: 5 dòng `Permission::create` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- **KHÔNG** ghi bảng `bill_income_request_detail_product_export_requests`.
- `auth()->user()->id` là id nhân viên duy nhất (DB đã gộp `employees`).
- BE: rethrow `ValidationException`, không catch chung `Exception`. Sau mỗi file PHP chạy `php -l <file>`.
- FE: đọc trước khi code — `.claude/skills/button-convention/SKILL.md`, `modal-popup/SKILL.md`, `form-validate/SKILL.md`, `unsaved-changes/SKILL.md`, `list-page/SKILL.md`, `print-page/SKILL.md`. Select trong modal **bắt buộc** `V2BaseSelectInModal`. Validate inline `is-invalid` + `invalid-feedback` + flag `touched`.
- FE: cờ quyền **fail-closed** — `canCreate/canEdit/canDelete/canApprove` khởi tạo `false`, chỉ set từ `$store.state.permissions`. Cấm gán literal `true`.
- Nguồn port ERP (chỉ đọc): `app/Http/Controllers/IncomeExpenditure/BillIncomeRequestController.php` · `app/Model/IncomeExpenditure/BillIncomeRequest.php` · `app/Http/Requests/IncomeExpenditure/BillIncomeRequest/*` · `app/Model/Accounting/AccountDetail.php:1746` · `resources/views/income_expenditure/bill_income_requests/*` · `resources/views/partials/classes/IncomeExpenditure/BillIncomeRequest*.blade.php` · `app/Http/Controllers/Common/SearchController.php@searchAllContract`.
- ⚠️ **Base FE đã đổi sau khi viết spec (user nhắc 2026-08-14)**: feature `form-validate-base` đã sửa **base** `V2Base*` để gắn được `v-validate` (vee-validate v2) trực tiếp — 2 mixin mới `utils/mixins/v2ValidateMixin.js` + `utils/mixins/formValidateMixin.js`, 7 component đã gắn (Input, Textarea, Select, SelectInModal, SelectRemote, DatePicker, CurrencyInput). Màn mẫu khách hàng (`pages/assign/customers/index.vue`, `CustomerForm.vue`) đã cập nhật theo bản mới. → Phase 4-6 **đọc code hiện tại của màn mẫu**, KHÔNG bám snapshot trong spec: validate realtime bằng `v-validate`, FE chỉ `required` ô **Tên**, message FE viết đúng nguyên văn message BE, lỗi BE 422 gộp qua `fieldError()`/`applyServerErrors()`.
- Base URL API dev: `http://localhost:8000/api/v1/finance/...` — verify bằng HTTP thật (token JWT của tài khoản có quyền), **không** dựa vào tài khoản dev 0 quyền.

---

## Phase 0 — Brainstorming & chốt design

- [x] Đọc hiểu toàn bộ luồng màn ERP (controller / blade / 3 class JS / model / validate / API công nợ)
- [x] Khảo sát hiện trạng HRM: `Modules/Finance`, `hrm_contracts`, quyền ERP, slot menu Tài chính
- [x] Chốt 10 quyết định với user (xem spec mục 2)
- [x] Viết spec `docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md`
- [x] User review spec — chốt 2 điểm mở: popup chỉ lấy HĐ HRM `status ∈ {6,8,9,10,11,12}`; màn chờ duyệt chỉ có nút Không duyệt
- [x] Lên plan chi tiết (file này)

---

## Phase 1 — BE nền: entity + morphMap + list/show

### Task 1.1 — 9 entity hợp đồng read-only + Supplier

**Files (Create):**
- `Modules/Finance/Entities/Contract/FirmContract.php`
- `Modules/Finance/Entities/Contract/OpeningContract.php`
- `Modules/Finance/Entities/Contract/WrServiceContract.php`
- `Modules/Finance/Entities/Contract/BuyContract2.php`
- `Modules/Finance/Entities/Contract/InlandBuyContract.php`
- `Modules/Finance/Entities/Contract/InlandBuyContractNew.php`
- `Modules/Finance/Entities/Contract/BuyServiceContract.php`
- `Modules/Finance/Entities/Contract/BuyDebtContractBeginning.php`
- `Modules/Finance/Entities/Supplier.php`

**Interfaces:**
- Produces: 8 class hợp đồng ERP + `Supplier`, tất cả **read-only** (không fillable, không boot hook), mỗi class có property `$table` và accessor `getDisplayCodeAttribute()` trả `code`.
- Consumes: không.

- [x] **Bước 1: Lấy đúng tên bảng của 8 nguồn hợp đồng.** Chạy:
```bash
mysql --default-character-set=utf8mb4 -h127.0.0.1 -uroot gop_db -e "SHOW TABLES LIKE '%contract%';"
```
Đối chiếu với model ERP tương ứng (`erp/app/Model/Sale/Firm/Contract/FirmContract.php`, `erp/app/Model/Accounting/OpeningContract.php`, `erp/app/Model/Customers/WrServiceContract.php`, `erp/app/Model/Order/BuyContract2.php`, `erp/app/Model/Order/InlandBuyContract.php`, `erp/app/Model/Order/InlandBuyContractNew.php`, `erp/app/Model/Sale/BuyServiceContract.php`, `erp/app/Model/Contract/BuyDebtContractBeginning.php`) — đọc property `$table` của từng file, **không đoán tên bảng**.

- [x] **Bước 2: Viết 8 entity theo đúng khuôn sau** (ví dụ `FirmContract`, 7 file còn lại đổi namespace/tên/bảng tương ứng):
```php
<?php

namespace Modules\Finance\Entities\Contract;

use Illuminate\Database\Eloquent\Model;

/**
 * Hợp đồng hãng — bảng ERP `firm_contracts` trên DB gộp. CHỈ ĐỌC.
 *
 * KHÔNG kế thừa App\Models\BaseModel (BaseModel có hook creating/saving gán created_by/updated_by,
 * bảng của ERP do cổng ERP quản lý, HRM không được ghi).
 *
 * Entity này KHÔNG xuất hiện trong popup chọn hợp đồng của HRM (user chốt thay bằng hrm_contracts),
 * nhưng BẮT BUỘC phải khai: 6.877 dòng bill_income_request_details của 2.411 phiếu cũ do ERP tạo
 * đang trỏ tới class này qua morphMap — thiếu nó thì HRM không hiển thị được phiếu cũ.
 */
class FirmContract extends Model
{
    protected $table = 'firm_contracts';

    public $timestamps = false;

    /** Chặn mọi thao tác ghi từ phía HRM. */
    protected $guarded = ['*'];
}
```

- [x] **Bước 3: Viết `Supplier`** (`Modules/Finance/Entities/Supplier.php`, cùng khuôn read-only, thêm accessor).
  ⚠️ **PLAN GHI SAI, đã sửa khi làm**: KHÔNG phải bảng `suppliers`. ERP `App\Model\Sale\Supplier` khai
  `$table = "customers"` + override `newQuery()` lọc `is_supplier = true` — NCC và KH dùng chung bảng
  `customers`. Bảng `suppliers` có tồn tại nhưng **0 dòng** (dùng nhầm → popup NCC luôn rỗng).
  Đã verify: 3 dòng `bill_income_request_details.supplier_id` đều khớp `customers` với `is_supplier = 1`.
  HRM lọc bằng **global scope** `is_supplier` (thay vì override `newQuery()`) để `withoutGlobalScope()`
  vẫn gỡ được và quan hệ `belongsTo` cũng ăn bộ lọc.
```php
public function getFullNameWithCodeAttribute()
{
    return trim($this->code . ' - ' . $this->fullname);
}
```

- [x] **Bước 4: Verify.** `php -l` sạch cho cả 9 file, rồi:
```bash
php artisan tinker --execute="echo Modules\Finance\Entities\Contract\FirmContract::count().' | '.Modules\Finance\Entities\Supplier::count();"
```
Kỳ vọng: ra số > 0 cho cả hai (bảng ERP có dữ liệu), không lỗi "Table doesn't exist".

---

### Task 1.2 — Entity `BillIncomeRequest` + `BillIncomeRequestDetail`

**Files (Create):**
- `Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php`
- `Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequestDetail.php`

**Interfaces:**
- Consumes: 9 entity hợp đồng (Task 1.1) + `Modules\Assign\Entities\Contract\Contract`.
- Produces: `BillIncomeRequest::STATUSES`, `::TYPE`, `::typeForSelect()`, `::searchByFilter(Request $r): Builder`, `::generateCode(): string`, `canView(): bool`, `canEdit(): bool`, `canDelete(): bool`, quan hệ `details()`, `currency()`, `employee_create()`, `approved_by()`; `BillIncomeRequestDetail::objectable()`, `customer()`, `supplier()`.

- [x] **Bước 1: Viết `BillIncomeRequest`** — port từ `erp/app/Model/IncomeExpenditure/BillIncomeRequest.php`, giữ nguyên hằng số:
```php
protected $table = 'bill_income_requests';

protected $fillable = [
    'code', 'type', 'reason', 'payer', 'created_by', 'type_money_id', 'updated_by',
    'status', 'type_object', 'exchange_rate', 'approved_id',
    'department_id', 'company_id', 'part_id', 'note',
];

const STATUS_CREATING = 1;          // Đang tạo
const STATUS_AWAITING_APPROVE = 2;  // Chờ KT duyệt
const STATUS_CREATED = 3;           // Đã tạo phiếu thu   (ngoài phạm vi, chỉ hiển thị)
const STATUS_APPROVED = 4;          // Đã hạch toán       (ngoài phạm vi, chỉ hiển thị)
const STATUS_CANCEL = 5;            // Hủy                (ngoài phạm vi, chỉ hiển thị)
const STATUS_REJECT = 6;            // Không duyệt

const TYPE_SELL = 1;                // Thu bán hàng
const TYPE_SUPPLIER = 2;            // Thu nhà cung cấp

const TYPE = [1 => 'Thu bán hàng', 2 => 'Thu nhà cung cấp', 3 => 'Thu khác'];

public const STATUSES = [
    ['id' => 1, 'name' => 'Đang tạo', 'type' => 'danger'],
    ['id' => 2, 'name' => 'Chờ KT duyệt', 'type' => 'danger'],
    ['id' => 3, 'name' => 'Đã tạo phiếu thu', 'type' => 'success'],
    ['id' => 4, 'name' => 'Đã hạch toán', 'type' => 'success'],
    ['id' => 5, 'name' => 'Hủy', 'type' => 'danger'],
    ['id' => 6, 'name' => 'Không duyệt', 'type' => 'danger'],
];

/** Dropdown "Loại thu" — bỏ key 3 (Thu khác) đúng như ERP type_for_select(). */
public static function typeForSelect(): array
{
    $result = [];
    foreach (self::TYPE as $key => $name) {
        if ($key == 3) continue;
        $result[] = ['id' => $key, 'name' => $name];
    }
    return $result;
}
```

- [x] **Bước 2: Quan hệ + gán đơn vị tổ chức khi tạo.** ERP gán `company_id/department_id/part_id` ở hook `created` rồi `save()` lần 2 (2 query, spec mục 9.2) — HRM gán **trước** khi insert:
```php
public function details()
{
    return $this->hasMany(BillIncomeRequestDetail::class, 'parent_id', 'id');
}

public function currency()
{
    return $this->belongsTo(\Modules\Finance\Entities\Currency\Currency::class, 'type_money_id');
}

public function employee_create()
{
    return $this->belongsTo(\Modules\Human\Entities\Employee::class, 'created_by', 'id');
}

public function approved_by()
{
    return $this->belongsTo(\Modules\Human\Entities\Employee::class, 'approved_id', 'id');
}

protected static function booted()
{
    static::creating(function (self $model) {
        $info = optional(auth()->user())->info;
        $model->created_by = $model->created_by ?: auth()->id();
        $model->company_id = $model->company_id ?: ($info->company_id ?? null);
        $model->department_id = $model->department_id ?: ($info->department_id ?? null);
        $model->part_id = $model->part_id ?: ($info->part_id ?? null);
    });
    static::saving(function (self $model) {
        $model->updated_by = auth()->id();
    });
}
```

- [x] **Bước 3: `generateCode()` — có khóa, khác ERP.** ERP không khóa nên 2 cổng tạo cùng lúc có thể trùng mã (spec 9.2):
```php
/**
 * Mã phiếu: {mã công ty}.DNTT{mmyy}.{5 số} — dùng chung dãy số với ERP trên cùng bảng.
 * Khác ERP: bọc lockForUpdate + retry để 2 cổng tạo đồng thời không sinh trùng mã.
 * Gọi TRONG transaction của store().
 */
public static function generateCode(): string
{
    $companyCode = optional(optional(auth()->user())->info)->company->code ?? '';
    $prefix = $companyCode . '.DNTT' . now()->format('my') . '.';

    $max = (int) static::query()
        ->where('code', 'like', $prefix . '%')
        ->lockForUpdate()
        ->selectRaw('MAX(CAST(SUBSTRING(code, ?) AS UNSIGNED)) as max_num', [mb_strlen($prefix) + 1])
        ->value('max_num');

    for ($i = 1; $i <= 5; $i++) {
        $code = $prefix . str_pad($max + $i, 5, '0', STR_PAD_LEFT);
        if (!static::query()->where('code', $code)->exists()) {
            return $code;
        }
    }

    return $prefix . str_pad($max + 6, 5, '0', STR_PAD_LEFT);
}
```

- [x] **Bước 4: 3 hàm quyền.** Port `canView()` (`erp/.../BillIncomeRequest.php:394`) nguyên vẹn nhưng đổi tên quyền sang bản HRM (Task 1.6). `canEdit()`/`canDelete()` **siết hơn ERP** — thêm điều kiện là người tạo:
```php
public function canEdit(): bool
{
    return in_array($this->status, [self::STATUS_CREATING, self::STATUS_REJECT])
        && $this->created_by == auth()->id();
}

public function canDelete(): bool
{
    return $this->canEdit();
}
```

- [x] **Bước 5: `BillIncomeRequestDetail`:**
```php
protected $table = 'bill_income_request_details';

protected $fillable = [
    'parent_id', 'customer_id', 'supplier_id', 'employee_id',
    'objectable_id', 'objectable_type',
    'income_money_request', 'income_money_request_exchange',
    'income_money_real', 'income_money_real_exchange',
    'note', 'is_income_begin',
];

public function objectable()
{
    return $this->morphTo();
}

public function customer()
{
    // ⚠️ PLAN GHI SAI: \Modules\Assign\Entities\Customer KHÔNG tồn tại.
    // Luồng khách hàng duy nhất (/assign/customers, sau customer-cut-mysql2) dùng App\Models\TpCustomer.
    return $this->belongsTo(\App\Models\TpCustomer::class, 'customer_id');
}

public function supplier()
{
    return $this->belongsTo(\Modules\Finance\Entities\Supplier::class, 'supplier_id');
}
```
⚠️ Trước khi viết, xác minh namespace model khách hàng đang dùng cho bảng `customers`: `grep -rn "protected \$table = 'customers'" Modules/ app/`. Dùng đúng class đang có, **không tạo model customer mới**.

- [x] **Bước 6: Verify.** `php -l` 2 file, rồi:
```bash
php artisan tinker --execute="\$m = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest::with('details')->first(); echo \$m->code.' | details='.\$m->details->count();"
```
Kỳ vọng: in ra mã phiếu ERP thật + số dòng chi tiết > 0.

---

### Task 1.3 — Đăng ký `morphMap` cho 9 loại hợp đồng

**Files (Modify):** `Modules/Finance/Providers/FinanceServiceProvider.php` (thêm vào `boot()`)

**Interfaces:**
- Consumes: 8 entity Task 1.1 + `Modules\Assign\Entities\Contract\Contract`.
- Produces: mọi `objectable_type` trong `bill_income_request_details` resolve được.

- [x] **Bước 1: Liệt kê giá trị thật đang có trong DB:**
```bash
mysql --default-character-set=utf8mb4 -h127.0.0.1 -uroot gop_db -e "SELECT DISTINCT objectable_type FROM bill_income_request_details;"
```
Kỳ vọng hiện tại: 4 giá trị (`FirmContract`, `OpeningContract`, `WrServiceContract`, `BuyDebtContractBeginning`). **Mọi giá trị in ra đều phải có mặt ở bước 2.**

- [x] **Bước 2: Thêm vào `boot()`** (đặt sau `registerConfig()`):
```php
use Illuminate\Database\Eloquent\Relations\Relation;
use Modules\Finance\Entities\Contract as FinanceContract;

// Map chuỗi objectable_type mà ERP đã ghi -> entity read-only phía HRM.
// Key là TÊN CLASS PHP CỦA ERP (ERP không dùng morphMap nên lưu nguyên tên class).
// Nhờ map này HRM đọc được 2.411 phiếu cũ; đồng thời khi HRM ghi 1 trong các entity dưới đây,
// Eloquent lưu ngược lại đúng chuỗi class ERP -> dữ liệu 2 cổng đồng nhất.
Relation::morphMap([
    'App\Model\Sale\Firm\Contract\FirmContract'      => FinanceContract\FirmContract::class,
    'App\Model\Accounting\OpeningContract'           => FinanceContract\OpeningContract::class,
    'App\Model\Customers\WrServiceContract'          => FinanceContract\WrServiceContract::class,
    'App\Model\Order\BuyContract2'                   => FinanceContract\BuyContract2::class,
    'App\Model\Order\InlandBuyContract'              => FinanceContract\InlandBuyContract::class,
    'App\Model\Order\InlandBuyContractNew'           => FinanceContract\InlandBuyContractNew::class,
    'App\Model\Sale\BuyServiceContract'              => FinanceContract\BuyServiceContract::class,
    'App\Model\Contract\BuyDebtContractBeginning'    => FinanceContract\BuyDebtContractBeginning::class,
]);
```
Hợp đồng HRM (`Modules\Assign\Entities\Contract\Contract`) **không** cần map — lưu nguyên tên class của chính nó.

- [x] **Bước 3: Verify resolve được mọi loại:**
```bash
php artisan tinker --execute="foreach (Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequestDetail::select('objectable_type')->distinct()->pluck('objectable_type') as \$t) { \$d = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequestDetail::where('objectable_type', \$t)->first(); echo \$t.' => '.(optional(\$d->objectable)->code ?: 'NULL').PHP_EOL; }"
```
Kỳ vọng: mỗi loại in ra một mã hợp đồng thật, **không** có `Class not found`.

---

### Task 1.4 — Service tính công nợ (`AccountDetail`)

**Files (Create):**
- `Modules/Finance/Entities/Accounting/AccountDetail.php` (read-only, bảng `account_details`)
- `Modules/Finance/Services/BillIncomeDebtService.php`

**Interfaces:**
- Produces: `BillIncomeDebtService::getDebtAfterIncomeMoney(int $objectableId, string $objectableType, ?int $customerId, ?int $supplierId): float`

- [x] **Bước 1: Entity read-only** `AccountDetail` (`$table = 'account_details'`, `$guarded = ['*']`, `public $timestamps = false`) + hằng `TYPE_DEBT = 1`, `TYPE_HAS = 2`.

- [x] **Bước 2: Port công thức** từ `erp/app/Model/Accounting/AccountDetail.php:1746`, bỏ nhánh `is_rule_contract`/`is_income_begin`:
```php
/**
 * Số tiền còn nợ của 1 hợp đồng — port ERP AccountDetail::getDebtAfterIncomeMoney().
 *   Thu bán hàng     -> TK 1311, lọc customer_id
 *   Thu nhà cung cấp -> TK 3311, lọc supplier_id
 *   còn nợ = SUM(bên Nợ, type=1) - SUM(bên Có, type=2) trên money_value_exchange
 *
 * LƯU Ý NGHIỆP VỤ: hợp đồng lấy từ `hrm_contracts` chưa có bút toán nào trong account_details
 * -> hàm này trả 0. Đúng thiết kế (user chốt giữ nguyên công thức ERP); khi có luồng hạch toán
 * HĐ HRM vào sổ cái thì số tự lên, không phải sửa code.
 */
public function getDebtAfterIncomeMoney($objectableId, $objectableType, $customerId, $supplierId = null): float
{
    $identifyNumber = $supplierId ? 3311 : 1311;
    $accountId = DB::table('accounts')->where('identify_number', $identifyNumber)->value('id');
    if (!$accountId) {
        return 0;
    }

    $row = AccountDetail::query()
        ->selectRaw('SUM(CASE WHEN type = 1 THEN money_value_exchange ELSE 0 END) as total_debt')
        ->selectRaw('SUM(CASE WHEN type = 2 THEN money_value_exchange ELSE 0 END) as total_have')
        ->where('contractable_id', $objectableId)
        ->where('contractable_type', $objectableType)
        ->when($supplierId, fn ($q) => $q->where('supplier_id', $supplierId))
        ->when(!$supplierId, fn ($q) => $q->where('customer_id', $customerId))
        ->where('account_id', $accountId)
        ->first();

    return (float) ($row->total_debt ?? 0) - (float) ($row->total_have ?? 0);
}
```
⚠️ `$objectableType` truyền vào là **chuỗi đã lưu trong DB** (tên class ERP), không phải class HRM — lấy từ `$detail->getRawOriginal('objectable_type')` hoặc từ mapping của Task 1.3.

- [x] **Bước 3: Verify trên hợp đồng ERP có dữ liệu thật:**
```bash
php artisan tinker --execute="\$s = app(Modules\Finance\Services\BillIncomeDebtService::class); \$d = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequestDetail::whereNotNull('customer_id')->first(); echo \$s->getDebtAfterIncomeMoney(\$d->objectable_id, \$d->getRawOriginal('objectable_type'), \$d->customer_id, null);"
```
Kỳ vọng: ra một số (có thể âm/dương). Đối chiếu đúng con số ấy với màn ERP của cùng phiếu — cột "Số tiền còn nợ".

---

### Task 1.5 — `searchByFilter` + 2 Resource

**Files:**
- Modify: `Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php` (thêm static `searchByFilter`)
- Create: `Modules/Finance/Transformers/BillIncomeRequest/BillIncomeRequestListResource.php`
- Create: `Modules/Finance/Transformers/BillIncomeRequest/BillIncomeRequestDetailResource.php`
- Create (nếu chưa có): `Modules/Finance/Entities/EmployeeManageDepartment.php`

**Interfaces:**
- Consumes: `BillIncomeDebtService` (Task 1.4).
- Produces: `BillIncomeRequest::searchByFilter(Request $r, string $scope = 'all'): Builder`; 2 resource.

- [x] **Bước 1: Port `searchByFilter`** từ `erp/.../BillIncomeRequest.php:150`, giữ **nguyên thứ tự** nhánh quyền, đổi sang tên quyền HRM:
```
1. 'Xem tất cả phiếu đề nghị thu của tổng công ty' -> không lọc
2. 'Xem tất cả phiếu đề nghị thu của công ty'      -> company_id = công ty user
3. 'Xem tất cả phiếu đề nghị thu của phòng ban'    -> department_id IN (employee_manage_departments của user)
4. 'Xem tất cả phiếu đề nghị thu của bộ phận'      -> part_id IN (employee_manage_parts của user)
5. mặc định                                        -> created_by = user
```
Luôn append điều kiện: `status != 1 OR created_by = auth()->id()` (ẩn nháp của người khác).
`$scope = 'pending'` → thêm `where('status', 2)->where('company_id', công ty user)`.
Filter nhận từ request: `code` (like), `contract_code` (whereHasMorph theo **8 class đã map**, KHÔNG dùng `'*'`), `type`, `status`, `customer_id`, `supplier_id`, `company_id`, `department_id`, `part_id`, `created_by`, `income_money_request_from` / `_to` (group theo `parent_id`, `HAVING SUM(income_money_request_exchange)` — dùng **binding**, không nội suy chuỗi như ERP `havingRaw("... >= $price_from")`), `start_date` / `end_date` theo `created_at`. Sort mặc định `created_at DESC`.

- [x] **Bước 2: `BillIncomeRequestListResource`** — trường: `id`, `code`, `type`, `type_name`, `customer_name` (theo `type`: 1 → `details[0].customer.code - fullname`, 2 → `details[0].supplier...`), `department_name`, `created_by_name`, `created_at` (`d/m/Y`), `total_income_money_request` (= `details.sum('income_money_request_exchange')`), `status`, `status_name`, `status_type`, `is_can_edit`, `is_can_delete`. Tất cả tên nhân viên lấy qua `optional()` — nhân viên bị xóa không được làm nổ 500.

- [x] **Bước 3: `BillIncomeRequestDetailResource`** — thông tin chung + `details[]` với: `customer_id/code/name`, `supplier_id/code/name`, `object_id`, `object_code`, `object_type` (chuỗi raw đã lưu), `dept_after_income_money` (gọi `BillIncomeDebtService`), `income_money_request`, `income_money_request_exchange`, `note`. Kèm cờ `is_can_edit`, `is_can_delete`, `is_can_reject` (= `status == 2` && user có quyền `Kế toán thanh toán`).

- [x] **Bước 4: Verify** `php -l` sạch; test thật ở Task 1.7.

---

### Task 1.6 — 5 quyền mới trong seeder

**Files (Modify):** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [x] **Bước 1: Xác nhận dải id còn trống** (nếu đã bị chiếm thì dời xuống, ghi chú lý do như block "Phiếu yêu cầu chuyển hàng" đã làm):
```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT id,name,guard_name FROM permissions WHERE id BETWEEN 1148 AND 1160;"
grep -n "'id' => 114[89]\|'id' => 115[0-2]" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: cả hai lệnh không ra dòng nào.

- [x] **Bước 2: Thêm block sau dòng cuối cùng của seeder (hiện là id 1147):**
```php
// Phiếu đề nghị thu tiền (Tài chính) — 4 quyền xem theo cấp + 1 quyền kế toán duyệt.
// Tên giữ Y HỆT quyền ERP (id 100177, 100179-100182) theo yêu cầu user. KHÔNG trùng khóa vì
// quyền ERP dùng guard 'web', quyền HRM dùng guard 'api' (unique key spatie là name+guard_name).
// LƯU Ý VẬN HÀNH: quyền KHÔNG bắc cầu giữa 2 cổng — người có quyền bên ERP vẫn phải được gán
// role tương ứng bên HRM mới dùng được màn này.
Permission::create(['id' => 1148, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thu của tổng công ty', 'display_name' => 'Xem tất cả phiếu đề nghị thu của tổng công ty', 'group' => 'Đề nghị thu tiền', 'type' => 8, 'sort_order' => 1]);
Permission::create(['id' => 1149, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thu của công ty', 'display_name' => 'Xem tất cả phiếu đề nghị thu của công ty', 'group' => 'Đề nghị thu tiền', 'type' => 8, 'sort_order' => 2]);
Permission::create(['id' => 1150, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thu của phòng ban', 'display_name' => 'Xem tất cả phiếu đề nghị thu của phòng ban', 'group' => 'Đề nghị thu tiền', 'type' => 8, 'sort_order' => 3]);
Permission::create(['id' => 1151, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thu của bộ phận', 'display_name' => 'Xem tất cả phiếu đề nghị thu của bộ phận', 'group' => 'Đề nghị thu tiền', 'type' => 8, 'sort_order' => 4]);
Permission::create(['id' => 1152, 'guard_name' => 'api', 'name' => 'Kế toán thanh toán', 'display_name' => 'Kế toán thanh toán', 'group' => 'Đề nghị thu tiền', 'type' => 8, 'sort_order' => 5]);
```

- [x] **Bước 3: Chèn 5 dòng vào DB dev bằng SQL tay** (KHÔNG chạy cả seeder — nó đang khai trùng id 1117/1118 nên sẽ nổ, xem spec mục 7):
```sql
INSERT INTO permissions (id, name, display_name, guard_name, `group`, type, sort_order, created_at, updated_at) VALUES
(1148,'Xem tất cả phiếu đề nghị thu của tổng công ty','Xem tất cả phiếu đề nghị thu của tổng công ty','api','Đề nghị thu tiền',8,1,NOW(),NOW()),
(1149,'Xem tất cả phiếu đề nghị thu của công ty','Xem tất cả phiếu đề nghị thu của công ty','api','Đề nghị thu tiền',8,2,NOW(),NOW()),
(1150,'Xem tất cả phiếu đề nghị thu của phòng ban','Xem tất cả phiếu đề nghị thu của phòng ban','api','Đề nghị thu tiền',8,3,NOW(),NOW()),
(1151,'Xem tất cả phiếu đề nghị thu của bộ phận','Xem tất cả phiếu đề nghị thu của bộ phận','api','Đề nghị thu tiền',8,4,NOW(),NOW()),
(1152,'Kế toán thanh toán','Kế toán thanh toán','api','Đề nghị thu tiền',8,5,NOW(),NOW());
```
Sau đó `php artisan cache:forget spatie.permission.cache` (hoặc `php artisan permission:cache-reset`).

- [x] **Bước 4: Gán 5 quyền cho role test** (role `Super admin` id 18 — xem memory `gop_db_permission_tables`) rồi verify:
```bash
php artisan tinker --execute="echo auth()->loginUsingId(<ID_TEST>) ? (auth()->user()->can('Kế toán thanh toán') ? 'OK' : 'NO PERM') : 'LOGIN FAIL';"
```

---

### Task 1.7 — Controller + Service + routes (index / pending / show)

**Files:**
- Create: `Modules/Finance/Http/Controllers/V1/BillIncomeRequestController.php`
- Create: `Modules/Finance/Services/BillIncomeRequestService.php`
- Modify: `Modules/Finance/Routes/api.php`

**Interfaces:**
- Consumes: Task 1.2–1.6.
- Produces: `GET /v1/finance/bill-income-requests`, `/pending`, `/{id}`.

- [x] **Bước 1: Service** `searchByFilter(Request $r, string $scope)` → `BillIncomeRequest::searchByFilter($r, $scope)->with(['details.customer','details.supplier','details.objectable','employee_create.info.department'])->paginate((int) $r->get('per_page', 10))`. Khuôn phân trang mirror `ProductTransferRequestService::searchByFilter()`.

- [x] **Bước 2: Controller** extends `ApiController`; `show()` gọi `findOrFail` → `canView()` sai thì trả 403 `'Bạn không có quyền xem phiếu này'`.

- [x] **Bước 3: Routes** — thêm group vào `Modules/Finance/Routes/api.php`, **`/pending` phải khai TRƯỚC `/{id}`**:
```php
Route::group(['prefix' => '/bill-income-requests'], function () {
    Route::get('/', [BillIncomeRequestController::class, 'index']);
    Route::get('/pending', [BillIncomeRequestController::class, 'pending'])
        ->middleware('checkPermission:Kế toán thanh toán');
    Route::get('/search-contracts', [BillIncomeRequestController::class, 'searchContracts']);       // Phase 3
    Route::get('/search-buy-contracts', [BillIncomeRequestController::class, 'searchBuyContracts']); // Phase 3
    Route::get('/search-suppliers', [BillIncomeRequestController::class, 'searchSuppliers']);        // Phase 3
    Route::get('/{id}', [BillIncomeRequestController::class, 'show']);
    Route::get('/{id}/print-data', [BillIncomeRequestController::class, 'printData']);               // Phase 6
    Route::post('/', [BillIncomeRequestController::class, 'store']);                                 // Phase 2
    Route::put('/{id}', [BillIncomeRequestController::class, 'update']);                             // Phase 2
    Route::delete('/{id}', [BillIncomeRequestController::class, 'destroy']);                         // Phase 2
    Route::post('/{id}/change-status', [BillIncomeRequestController::class, 'changeStatus'])
        ->middleware('checkPermission:Kế toán thanh toán');                                          // Phase 2
});
```
`index` / `store` / `update` / `destroy` **không** gắn `checkPermission` — ERP không gate, phạm vi đã chặn trong `searchByFilter` + `canXxx`.

- [x] **Bước 4: Verify HTTP thật** (token của tài khoản đã gán quyền ở Task 1.6):
```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-income-requests?per_page=5" | head -c 800
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-income-requests/<ID_PHIEU_ERP>" | head -c 800
```
Kỳ vọng: list trả 5 phiếu ERP thật kèm `total_income_money_request`; detail trả đủ `details[]` với `object_code` **không rỗng** (chứng minh morphMap chạy) và `dept_after_income_money` khớp màn ERP.

**Checkpoint Phase 1:** ✅ ĐẠT (2026-08-14) — HRM đọc được toàn bộ phiếu ERP có sẵn, đúng phạm vi quyền.

**Bằng chứng verify Phase 1 (HTTP thật trên `localhost:8000`, token JWT của 3 tài khoản):**

| Kiểm thử | Kết quả |
| --- | --- |
| `GET /` (Super admin id 13) | `total = 2398` = 2.411 − **13 phiếu nháp của người khác** (SQL đối chiếu khớp chính xác) |
| `GET /{id}` phiếu ERP 2440 | 8 dòng chi tiết, `object_code` = mã HĐ thật ⇒ morphMap chạy; `dept_after_income_money` = 10.000.000 |
| `GET /pending` (kế toán công ty 3, id 407) | 1 phiếu "Chờ KT duyệt" — đúng công ty |
| `GET /pending` (Super admin, công ty 1) | 0 phiếu (phiếu chờ duyệt nằm ở công ty 3/4) — đúng luật ERP |
| `GET /pending` (user không quyền) | HTTP **403** |
| `GET /{id}` phiếu người khác (user không quyền) | HTTP **403** |
| Phạm vi user không quyền | chỉ thấy 30 phiếu do chính mình tạo |
| Filter `code` / `contract_code` / `type` / `status` / `customer_id` / `customer_name` / tiền from-to / ngày | đều trả đúng tập con |
| morphMap toàn bộ dữ liệu | **7562/7562** dòng resolve được hợp đồng, 0 lỗi `Class not found` |
| Công nợ | service khớp 100% với SQL thuần trên 5 mẫu + 3 dòng nhánh NCC (TK 3311) |
| Regression 3 endpoint Finance khác | `accounts` / `currencies` / `product-transfer-requests` đều HTTP 200 |

**5 điểm LỆCH so với plan gốc (đều do plan sai/thiếu, đã sửa và ghi lý do trong code):**

1. **`Supplier` không phải bảng `suppliers`** → là `customers` + lọc `is_supplier = 1` (bảng `suppliers` có thật nhưng 0 dòng). Xem Task 1.1 Bước 3.
2. **`Modules\Assign\Entities\Customer` không tồn tại** → dùng `App\Models\TpCustomer`. Xem Task 1.2 Bước 5.
3. **KHÔNG gắn middleware `checkPermission:Kế toán thanh toán`** cho `/pending` và `/change-status` như plan ghi. Middleware dùng chung resolve quyền qua spatie `getAllPermissions()` (lọc `model_type = Modules\Timesheet\Entities\Employee`) trong khi **1.252/1.691 dòng `employee_has_roles` trên DB gộp có `model_type = 'App\Employee'`**. Đã đo trực tiếp: **2/2 kế toán thật (id 308, 407) đều bị spatie trả `false`** dù có quyền → middleware sẽ 403 oan. Gate bằng `BillIncomeRequest::isAccountant()` trong Controller (query thẳng pivot). Tiền lệ: `ProductTransferRequestController::reject()`.
4. **Bỏ filter `customer_name` kiểu ERP**: ERP gọi `whereHas('customer', …)` trong khi model KHÔNG khai quan hệ `customer()` → luôn ném `BadMethodCallException`. HRM lọc qua `details.customer`.
5. **Thêm trait `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php`** thay vì chép 3 method quyền từ `ProductTransferRequest` (logic dùng ở 2 nơi). CHƯA sửa `ProductTransferRequest` để dùng trait — file đang chạy thật, theo CLAUDE.md phải hỏi trước khi đụng code dùng chung. **Cần user chốt** có gộp không.

**Lỗi tự phát hiện & đã sửa trong lúc làm:**
- `canView()` **fail-open khi chưa đăng nhập**: `$this->approved_id == auth()->id()` với cả 2 vế NULL → `null == null` = true, mở toang phiếu cho request không auth. Đã thêm guard `if (!$employeeId) return false;`.

**Ghi nhận cần biết cho các phase sau:**
- ✅ **`hrm_contracts` 0 dòng → ĐÃ XỬ LÝ bằng seeder** (user chốt 2026-08-14): `Modules/Finance/Database/Seeders/BillIncomeRequestTestDataSeeder.php`.
  Mặc định **DRY-RUN**, chạy thật: `FINANCE_TEST_DATA=1 php artisan db:seed --class="Modules\Finance\Database\Seeders\BillIncomeRequestTestDataSeeder"`.
  Đã chạy trên DB dev, sinh:
  · **8 hợp đồng HRM** `HĐ-TEST-DNTT-01..08` dựng từ báo giá CÓ THẬT (chép KH/dự án/công ty/phòng ban/tổng tiền) —
    6 cái status ∈ {6,8,9,10,11,12} (popup phải thấy) + 2 cái status {3,2} (popup phải LOẠI) để test luôn bộ lọc.
  · **2 phiếu mẫu** `TEST.DNTT.00001` (Đang tạo) và `TEST.DNTT.00002` (Chờ KT duyệt), chi tiết trỏ hợp đồng HRM.
  · **23 dòng `role_has_permissions`**: gán 5 quyền HRM mới (1148-1152) cho đúng các role đang giữ quyền ERP cùng tên
    (3/7/4/2/7 role) — user chốt "dùng quyền mới thêm bên HRM". Chỉ THÊM, không xoá quyền ERP.
  Idempotent (nhận diện theo tiền tố mã, chạy lại không nhân bản). Gỡ: xoá theo `code LIKE 'HĐ-TEST-DNTT-%'` / `'TEST.DNTT.%'`.

  **Mở rộng 2026-08-14 (user yêu cầu "fake nhiều dữ liệu để test")** — seeder nâng lên 4 bước,
  số lượng chỉnh qua env `FINANCE_TEST_CONTRACTS` (mặc định 40) / `FINANCE_TEST_REQUESTS` (mặc định 60):
  · **40 hợp đồng HRM** (từ 40 báo giá thật; 1/8 để trạng thái thấp để kiểm chứng popup lọc)
  · **59 bút toán công nợ** TK 1311 (`account_details`) cho 33 hợp đồng — đã thu 0/30/50/70/100% luân phiên
    → cột "Số tiền còn nợ" ra số THẬT khác nhau từng hợp đồng, có cả hợp đồng còn nợ 0.
    Mọi dòng gắn `invoiceable_code` tiền tố `TEST-DNTT-DEBT-` để tra và xoá sạch được.
  · **60 phiếu** phủ đủ 6 trạng thái (10 nháp / 18 chờ duyệt / 8 đã tạo phiếu thu / 8 đã hạch toán /
    8 hủy / 8 không duyệt), 2 loại thu (47 Thu bán hàng + 11 Thu NCC dùng hợp đồng mua thật của ERP),
    5 người tạo cùng công ty, 1-4 dòng chi tiết/phiếu, **49/60 phiếu gom từ 2-4 khách hàng**
    (đúng đặc điểm 46% của dữ liệu ERP thật), VNĐ + USD/EURO/JPY, ngày tạo rải 180 ngày.
  ⚠️ **Phiếu nháp luôn gán cho tài khoản dev** — nháp của người khác bị màn danh sách ẩn theo đúng
  luật nghiệp vụ, gán lung tung thì user không thấy phiếu nào để test Sửa/Xóa.
  Verify: danh sách 2.458 phiếu, màn chờ duyệt 18 phiếu, popup hợp đồng của KH 18505 ra 79 dòng
  kèm công nợ thật (vd `HĐ-TEST-DNTT-01` còn nợ 1.276.487.940).
  ⚠️ 2 phiếu mẫu CŨNG hiện bên cổng ERP (bảng dùng chung) và mở chi tiết bên ERP sẽ lỗi `Class not found` — đúng rủi ro đã chấp nhận.
  Verify qua API: `object_code = HĐ-TEST-DNTT-01`, `object_type = Modules\Assign\Entities\Contract\Contract`, `is_can_edit = true` cho phiếu nháp của chính mình.
- Bảng `employees` **không có cột `fullname`** (tên ở `employee_infos`) → mọi chỗ lấy tên người dùng phải đi `employee_create.info.fullname`, không phải `employee_create.fullname` như code ERP.
- `php artisan permission:cache-reset` báo **"Unable to flush cache"** trên máy dev (cache driver chưa sẵn sàng). Không ảnh hưởng màn này vì trait query thẳng DB, nhưng middleware `checkPermission` của màn khác có thể còn giữ cache cũ.
- Tài khoản kế toán công ty 4 (id 308) có `employees.status = 0` → token JWT bị 401. Muốn test công ty 4 phải mở khóa tài khoản khác.

---

## Phase 2 — BE ghi: store / update / destroy / change-status

### Task 2.1 — 3 FormRequest

**Files (Create):**
- `Modules/Finance/Http/Requests/BillIncomeRequest/BillIncomeRequestStoreRequest.php`
- `Modules/Finance/Http/Requests/BillIncomeRequest/BillIncomeRequestUpdateRequest.php`
- `Modules/Finance/Http/Requests/BillIncomeRequest/BillIncomeRequestChangeStatusRequest.php`

- [x] **Bước 1: `StoreRequest::rules()`** — port `erp/app/Http/Requests/.../BillIncomeRequestStoreRequest.php`, bỏ 3 rule động của nhánh phiếu YCXH:
```php
public function rules()
{
    return [
        'type' => 'required|numeric|in:1,2',
        'reason' => 'required',
        'type_money_id' => 'required|exists:currencies,id',
        'exchange_rate' => 'required|numeric|gt:0',
        'status' => 'required|in:1,2',
        'note' => [Rule::requiredIf($this->status == 6)],
        'details' => 'required|array|min:1',
        'details.*.income_money_request' => 'required|numeric|min:0',
        'details.*.customer_id' => [Rule::requiredIf($this->type == 1)],
        'details.*.supplier_id' => [Rule::requiredIf($this->type == 2)],
        'details.*.object_id' => 'required',
        'details.*.object_type' => ['required', Rule::in(BillIncomeRequest::allowedObjectTypes())],
    ];
}

public function messages()
{
    return [
        'type.required' => 'Bắt buộc nhập',
        'type.numeric' => 'Phải là số',
        'reason.required' => 'Bắt buộc nhập',
        'type_money_id.required' => 'Bắt buộc nhập',
        'exchange_rate.required' => 'Bắt buộc nhập',
        'details.required' => 'Bắt buộc nhập',
        'details.*.income_money_request.required' => 'Bắt buộc nhập',
        'details.*.income_money_request.numeric' => 'Phải là số',
        'details.*.customer_id.required' => 'Bắt buộc nhập',
        'details.*.supplier_id.required' => 'Bắt buộc nhập',
        'details.*.object_id.required' => 'Bắt buộc nhập',
    ];
}
```

- [x] **Bước 2: Thêm `allowedObjectTypes()`** vào entity `BillIncomeRequest` — trả mảng 9 chuỗi hợp lệ (8 class ERP đã map ở Task 1.3 + `Modules\Assign\Entities\Contract\Contract::class`).

- [x] **Bước 3: `UpdateRequest`** kế thừa `StoreRequest` (ERP dùng nhầm StoreRequest cho update — spec 9.2); `ChangeStatusRequest`: `status` `required|in:6`, `note` `required` kèm message `'Bắt buộc nhập lý do không duyệt'`.

- [x] **Bước 4:** `php -l` 3 file.

### Task 2.2 — `store` / `update` / `syncDetails`

**Files (Modify):** `BillIncomeRequestService.php`, `BillIncomeRequestController.php`

- [x] **Bước 1: `store()`** trong transaction: `generateCode()` → `create()` (đã gán company/department/part ở hook `creating`) → `syncDetails()` → nếu `status == 2` gửi thông báo (Task 2.4) → commit. Catch `ValidationException` thì **rethrow**, catch `Exception` thì `Log::error` + rollback + trả message `'Thêm phiếu đề nghị thu thất bại!'`.

- [x] **Bước 2: `syncDetails(BillIncomeRequest $bill, array $details)`** — port ERP: xóa hết detail cũ rồi insert lại; map `object_id → objectable_id`, `object_type → objectable_type`; luôn ghi `is_income_begin = 0`; **không** động tới bảng `bill_income_request_detail_product_export_requests`:
```php
BillIncomeRequestDetail::where('parent_id', $bill->id)->delete();
foreach ($details as $detail) {
    BillIncomeRequestDetail::create([
        'parent_id' => $bill->id,
        'customer_id' => $detail['customer_id'] ?? null,
        'supplier_id' => $detail['supplier_id'] ?? null,
        'objectable_id' => $detail['object_id'],
        'objectable_type' => $detail['object_type'],
        'income_money_request' => $detail['income_money_request'],
        'income_money_request_exchange' => $detail['income_money_request_exchange'] ?? 0,
        'note' => $detail['note'] ?? null,
        'is_income_begin' => 0,
    ]);
}
```

- [x] **Bước 3: `update()`** — gate `canEdit()` (403 nếu sai), cập nhật master **trước** rồi mới `syncDetails()` (ERP làm ngược — spec 9.2), cùng transaction.

- [x] **Bước 4: Verify tạo nháp qua HTTP** với 1 hợp đồng HRM thật (nếu `hrm_contracts` chưa có dữ liệu thì tạo 1 hợp đồng ở `/assign/contracts` trước):
```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"type":1,"type_money_id":1,"exchange_rate":1,"reason":"Test thu đợt 1","status":1,"details":[{"customer_id":<ID_KH>,"object_id":<ID_HD>,"object_type":"Modules\\\\Assign\\\\Entities\\\\Contract\\\\Contract","income_money_request":1000000,"income_money_request_exchange":1000000,"note":""}]}' \
  "http://localhost:8000/api/v1/finance/bill-income-requests"
```
Kỳ vọng: 200, và:
```sql
SELECT code, status, company_id, department_id FROM bill_income_requests ORDER BY id DESC LIMIT 1;
SELECT objectable_id, objectable_type FROM bill_income_request_details ORDER BY id DESC LIMIT 1;
```
mã đúng format `xxx.DNTT<mmyy>.00001`, `company_id/department_id` không NULL, `objectable_type` = `Modules\Assign\Entities\Contract\Contract`.

### Task 2.3 — `destroy` + `changeStatus`

**Files (Modify):** `BillIncomeRequestService.php`, `BillIncomeRequestController.php`

- [x] **Bước 1: `destroy()`** — gate `canDelete()` ở **BE** (ERP chỉ ẩn nút trên UI, gọi thẳng URL xóa được phiếu bất kỳ), xóa detail rồi xóa master trong transaction.
- [x] **Bước 2: `changeStatus()`** — chỉ nhận `status = 6`; kiểm tra phiếu đang ở `status = 2`, nếu không trả 422 `'Phiếu không ở trạng thái chờ duyệt'`; ghi `status`, `note`, `approved_id = auth()->id()`.
- [x] **Bước 3: Verify chặn xóa trái phép:**
```bash
# đăng nhập bằng tài khoản KHÁC người tạo, gọi xóa phiếu nháp vừa tạo
curl -s -X DELETE -H "Authorization: Bearer $TOKEN_KHAC" "http://localhost:8000/api/v1/finance/bill-income-requests/<ID>" -w "\n%{http_code}\n"
```
Kỳ vọng: **403**, và phiếu vẫn còn trong DB.

### Task 2.4 — Thông báo khi gửi duyệt

**Files (Modify):** `BillIncomeRequestService.php`

- [x] **Bước 1:** Đọc `.claude/skills/notification-convention/SKILL.md` trước khi viết nội dung.
- [x] **Bước 2:** Khi `status == 2` (cả `store` và `update`) → gửi tới nhóm có quyền `Kế toán thanh toán` (guard `api`), deep-link `/finance/bill-income-requests/{id}`, nội dung theo mẫu ERP: `"Bạn có một phiếu đề nghị thu tiền cần duyệt từ {tên người gửi}"`. Tìm helper thông báo đang dùng trong HRM: `grep -rn "class NotificationHelper\|function sendNotify" app/ Modules/ | head`.
- [x] **Bước 3: Verify** — gửi duyệt 1 phiếu, kiểm tra bản ghi thông báo mới xuất hiện và người nhận đúng là nhóm có quyền.

**Checkpoint Phase 2:** ✅ ĐẠT (2026-08-14) — tạo/sửa/xóa nháp/gửi duyệt/không duyệt chạy đủ bằng HTTP thật.

**Bằng chứng (script `verify_phase2.py`, 12 nhóm kiểm thử, chạy trên hợp đồng HRM mẫu `HĐ-TEST-DNTT-01`):**

| Kiểm thử | Kết quả |
| --- | --- |
| Tạo nháp | 200 · mã sinh đúng `TPE.DNTT0826.00001` · `company_id`/`department_id`/`created_by`/`updated_by` đều có giá trị (gán ở hook `creating`, 1 câu ghi) |
| Dòng chi tiết ghi ra | `objectable_type` = `Modules\Assign\Entities\Contract\Contract` (LENGTH=41 → đúng 1 dấu `\`), `is_income_begin=0` |
| 7 ca validate phải chặn | `details` rỗng · `object_type` lạ · `exchange_rate=0` · `status=4` (lách sang "Đã hạch toán") · thu NCC thiếu `supplier_id` · `type=99` · tiền tệ không tồn tại → **422 đủ 7/7**, lỗi trả đúng tên trường |
| Sửa nháp | 200, tổng tiền + số dòng cập nhật đúng (xoá-ghi lại chi tiết) |
| Người khác sửa/xoá nháp | **403** cả PUT lẫn DELETE, phiếu vẫn còn trong DB |
| Gửi duyệt (1→2) | 200 · sinh **29 notification** cho đúng 29 kế toán công ty 1 |
| Nội dung notification | `[DNTT] Chờ duyệt: <b>TPE.DNTT0826.00001</b>. Người đề nghị: DNS Admin. Số tiền: 2.500.000` + `url = /finance/bill-income-requests/2443` — đúng chuẩn `notification-convention` (prefix, nhóm hành động, in đậm tên, deep-link kèm ID, ≤120 ký tự) |
| Phiếu đã gửi duyệt | chính chủ cũng **403** khi sửa/xoá |
| Không duyệt — ca xấu | không phải kế toán → **403** · thiếu lý do → **422** · `status=4` → **422** |
| Không duyệt — hợp lệ | 200 · DB: `status=6`, `note` = lý do, `approved_id` = người xử lý |
| Phiếu "Không duyệt" | chính chủ sửa lại được (200) — đúng `canEdit()` |
| Không duyệt phiếu sai trạng thái | **422 "Phiếu không ở trạng thái chờ duyệt"** (không trả 403 gây hiểu nhầm) |
| Xoá phiếu | 200, dòng chi tiết xoá theo (còn 0/0) |
| `bill_income_request_detail_product_export_requests` | **0 dòng** trước và sau toàn bộ đợt test — HRM không ghi |

Đã dọn 29 notification test khỏi DB dev sau khi kiểm chứng.

**Điểm làm khác plan / khác ERP ở Phase 2 (đều có ghi lý do trong code):**
1. **Siết rule mạnh hơn ERP** ở `StoreRequest`: `type` in 1|2 · `status` in 1|2 (ERP không validate → FE gửi `status=4` là phiếu thành "Đã hạch toán") · `exchange_rate` phải `> 0` · `details` `min:1` · `object_type` phải thuộc danh sách class hợp lệ · `type_money_id`/`customer_id`/`supplier_id` phải `exists`.
2. **`allowedObjectTypes()` không viết tay** mà lấy từ `(new $class)->getMorphClass()` — luôn khớp morphMap thật, sai 1 ký tự là phiếu ghi xong không mở lại được.
3. **`UpdateRequest` tách class riêng** (kế thừa Store) thay vì dùng lại StoreRequest như ERP.
4. **`ChangeStatusRequest` chỉ nhận `status = 6`** (ERP nhận status bất kỳ → gọi thẳng API đổi được phiếu sang "Đã hạch toán").
5. **Bỏ rule `note` requiredIf `status==6` khỏi Store/Update** — code chết vì `status` ở đó chỉ còn 1|2; lý do không duyệt validate ở `ChangeStatusRequest`.
6. **Thông báo chỉ bắn khi CHUYỂN từ nháp sang chờ duyệt** — sửa lại phiếu đang chờ duyệt không spam kế toán thêm lần nữa (ERP bắn mỗi lần lưu).
7. **`changeStatus` tách 403 và 422**: sai quyền → 403; đúng quyền nhưng phiếu vừa bị người khác xử lý → 422 kèm lý do thật.
8. **`employeeInfoIdsHavingPermission()` thêm vào trait `ChecksEmployeePermission`** (thay vì gọi nhờ `ProductTransferRequest::` như một entity khác) — cùng lý do model_type mismatch.

**📌 NỢ KỸ THUẬT — user chốt HOÃN (2026-08-14), đánh giá lại sau:**
4 method kiểm tra quyền (`currentEmployeeHasPermission` · `currentEmployeeIsSuperAdmin` ·
`employeeInfoIdsHavingPermission` · `currentCompanyId`) hiện tồn tại **2 bản y hệt**:
`Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php:498-635` (167 dòng) và
trait mới `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php`.
Riêng `currentCompanyId()` còn bản thứ **ba** ở `Modules/Finance/Services/CompanyAccountService.php:15`.

Đã cân nhắc gộp (cho `ProductTransferRequest` `use` trait rồi xoá 4 method) nhưng **không làm**:
gộp không sửa lỗi nào, đổi lại phải hồi quy màn Yêu cầu chuyển hàng (entity gọi 23 chỗ, service 3 chỗ);
đây lại là code PHÂN QUYỀN — sai một chi tiết nhỏ (cache tĩnh per-class, `const SUPER_ADMIN_ROLE_ID`
nơi khác tham chiếu) là lọt/chặn quyền chứ không vỡ giao diện, và loại lỗi đó không nổ lúc test.
Gộp 2 file cũng chỉ là dọn nửa vời khi bản thứ ba vẫn còn.

**Điều kiện kích hoạt việc gộp** (làm thành task dọn code riêng, có phạm vi test riêng):
có màn THỨ BA cần đúng logic này, HOẶC phải sửa chính logic dò quyền (khi đó bắt buộc gộp, để 2 bản
là chắc chắn sót một bên). Docblock của trait đã ghi rõ nguồn gốc + cách gộp để người sau không phải dò lại.

---

## Phase 3 — BE phụ trợ: 3 endpoint popup

### Task 3.1 — `search-contracts` (popup hợp đồng bán, UNION 3 nguồn)

**Files (Modify):** `BillIncomeRequestService.php`, `BillIncomeRequestController.php`

**Interfaces:**
- Produces: `GET /search-contracts?customer_id=&code=&page=` → `{ data: [{ object_id, object_code, object_type, sign_date, total_value, dept_after_income_money }], ... }`

- [x] **Bước 1: Xây UNION 3 nguồn** (tham khảo `erp/app/Http/Controllers/Common/SearchController.php@searchAllContract` để biết cột và điều kiện, nhưng **bỏ nhánh `firm_contract`**):
```php
$hrm = DB::table('hrm_contracts')
    ->selectRaw("id as object_id, code as object_code, ? as object_type, sign_date, total_after_vat as total_value",
        [\Modules\Assign\Entities\Contract\Contract::class])
    ->where('customer_id', $customerId)
    // User chốt: chỉ hợp đồng Có hiệu lực trở lên (6,8,9,10,11,12); loại nháp/chờ duyệt (1,2,3,7)
    ->whereIn('status', [6, 8, 9, 10, 11, 12]);

$opening = DB::table('opening_contracts')
    ->selectRaw("id as object_id, code as object_code, ? as object_type, NULL as sign_date, NULL as total_value",
        ['App\Model\Accounting\OpeningContract'])
    ->where('customer_id', $customerId);

$wr = DB::table('wr_service_contracts')
    ->selectRaw("id as object_id, code as object_code, ? as object_type, NULL as sign_date, NULL as total_value",
        ['App\Model\Customers\WrServiceContract'])
    ->where('customer_id', $customerId);

$query = $hrm->unionAll($opening)->unionAll($wr);
```
⚠️ Xác minh tên bảng + tên cột `customer_id`/`code`/`status` của `opening_contracts` và `wr_service_contracts` bằng `SHOW COLUMNS` trước khi viết — **không đoán**.

- [x] **Bước 2:** Lọc thêm theo `code` (like) nếu có; phân trang; với mỗi dòng gọi `BillIncomeDebtService::getDebtAfterIncomeMoney()` để trả `dept_after_income_money`.

- [x] **Bước 3: Verify:**
```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-income-requests/search-contracts?customer_id=<ID_KH>" | head -c 600
```
Kỳ vọng: có hợp đồng HRM của khách đó, **không** có dòng nào `object_type` chứa `FirmContract`.

### Task 3.2 — `search-buy-contracts` (UNION 5 nguồn) + `search-suppliers`

**Files (Modify):** `BillIncomeRequestService.php`, `BillIncomeRequestController.php`

- [x] **Bước 1:** UNION 5 nguồn mua (`buy_contract_2`, `inland_buy_contracts`, `inland_buy_contract_news`, `buy_service_contracts`, `buy_debt_contract_beginnings`), lọc `supplier_id`; cùng khuôn trả về như Task 3.1 (đổi `dept` sang TK 3311 — service tự chọn khi truyền `supplierId`). Xác minh tên bảng/cột bằng `SHOW COLUMNS` + model ERP tương ứng.
- [x] **Bước 2:** `search-suppliers` — trả `id`, `code`, `fullname`, lọc `keyword` theo `code`/`fullname`, phân trang 10.
- [x] **Bước 3: Verify** cả 2 endpoint bằng `curl`, đối chiếu số bản ghi với popup tương ứng bên ERP.

**Checkpoint Phase 3:** ✅ ĐẠT (2026-08-14) — BE xong toàn bộ, 3 endpoint popup verify bằng HTTP thật.

**Bằng chứng (script `verify_phase3.py`, 11 nhóm kiểm thử):**

| Kiểm thử | Kết quả |
| --- | --- |
| `search-contracts` thiếu `customer_id` | **422 "Vui lòng chọn khách hàng trước"** (ERP chỉ chặn ở FE) |
| `search-contracts` KH 853 | total **124** = đúng SQL thuần (đầu kỳ + bảo dưỡng + HĐ HRM hợp lệ) |
| Lọc trạng thái HĐ HRM | HĐ mẫu status **3** và **2** đều KHÔNG xuất hiện trong popup của KH tương ứng |
| Thay `firm_contracts` → `hrm_contracts` | `object_type` trả về chỉ có `Contract` (HRM) + `WrServiceContract` — **không dòng nào là FirmContract** |
| Lọc `code` | có kết quả đúng; mã không tồn tại → total 0 |
| `search-buy-contracts` thiếu `supplier_id` | **422** |
| `search-buy-contracts` NCC 127 | total **19**, chia đúng từng nguồn: InlandBuyContract 11 · BuyDebtContractBeginning 5 · InlandBuyContractNew 2 · BuyServiceContract 1 · BuyContract2 0 — **khớp 100% SQL đếm từng bảng** |
| Công nợ nhánh NCC | tính trên TK **3311**, khớp SQL thuần; ra số thật (vd 44.209.500) |
| `search-suppliers` | total **9.547** = đúng số `customers.is_supplier = 1`; lọc theo tên (BUHLER → 2) và theo mã đều đúng |
| Loại khách hàng thường | mã `29TPHPDO-1` khớp LIKE 108 dòng nhưng chỉ trả **39 dòng là NCC**; KH thường id 8 **không lọt** |

**Điểm kỹ thuật đáng ghi:**
1. **Tên bảng/cột đối chiếu `information_schema` trước khi viết**, không đoán — kết quả khác plan:
   `opening_contracts` KHÔNG có `status` và KHÔNG có cột tiền (trả 0, đúng như ERP select `"0" as payed_cost`);
   `wr_service_contracts` CÓ `total_after_vat` (plan ghi NULL — đã dùng cột thật, popup hiện được giá trị HĐ);
   4/5 nguồn mua dùng đúng cột `payed_cost`, riêng `buy_debt_contract_beginnings` không có cột tiền → 0
   và là nguồn DUY NHẤT có `sign_date`.
2. **Bọc UNION vào subquery (`fromSub`) rồi mới lọc/sắp xếp.** Gọi `where()` thẳng trên builder UNION thì
   điều kiện chỉ dính nhánh ĐẦU TIÊN, các nhánh sau lọt hết — bug im lặng.
3. **`object_type` lấy từ `(new $class)->getMorphClass()`** chứ không viết chuỗi tay, để luôn khớp morphMap.
4. Công nợ tính **từng dòng** (1 query/dòng) nên bắt buộc phân trang — mặc định 10 dòng như popup ERP.
5. Khảo sát ERP: popup gửi `has_dept=1` nhưng **`has_dept` không được dùng ở bất kỳ đâu trong code ERP**
   (grep toàn repo) → tham số chết, HRM không port.

---

## Phase 4 — FE: danh sách + màn chờ duyệt + menu

### Task 4.1 — Store/API client + màn danh sách

**Files:**
- Create: `hrm-client/pages/finance/bill-income-requests/index.vue`
- Create: `hrm-client/components/finance/bill-income-request/` (thư mục dùng chung)

- [x] **Bước 1:** Đọc `.claude/skills/list-page/SKILL.md` + đọc `pages/assign/customers/index.vue` làm khuôn (base UI user chỉ định).
- [x] **Bước 2:** Dựng khung màn: `v2-styles min-vh-100` → `V2BaseFilterPanel` (tìm nhanh theo mã phiếu + `#advanced-filters`) → `V2BaseDataTable`.
- [x] **Bước 3: Bộ lọc** — Mã phiếu · Số hợp đồng · Loại thu · Trạng thái · Khách hàng · Nhà cung cấp · `V2BaseCompanyDepartmentFilter` · Người tạo · Số tiền từ–đến · Khoảng ngày tạo.
- [x] **Bước 4: Cột bảng** — STT · Mã phiếu (link `/finance/bill-income-requests/{id}`) · Loại thu · Khách hàng/NCC · Phòng ban · Người tạo · Ngày tạo · Tổng tiền đề nghị (VND, `toLocaleString`) · Trạng thái (badge theo `status_type`) · Thao tác (Xem / Sửa / Xóa / In).
- [x] **Bước 5: Cờ quyền fail-closed:**
```js
data() {
    return {
        // Fail-closed: KHÔNG BAO GIỜ khởi tạo true. Chỉ set từ quyền thật trong store.
        canApprove: false,
        canEditRow: false,
        canDeleteRow: false,
    }
},
mounted() {
    const perms = (this.$store.state.permissions || [])
    this.canApprove = perms.includes('Kế toán thanh toán')
}
```
`canEditRow` / `canDeleteRow` **không** tính ở FE — đọc thẳng cờ `is_can_edit` / `is_can_delete` do BE trả trong `BillIncomeRequestListResource` (BE đã gate bằng `canEdit()`/`canDelete()`), nên FE không cần suy luận trạng thái + người tạo.

Nút **Tạo mới** không gắn cờ quyền (BE không gate hành vi tạo, đúng như ERP) — hiện với mọi user vào được màn. Ghi comment nêu rõ để lần review sau không nhầm là thiếu kiểm tra quyền.
- [x] **Bước 6: Verify** bằng Playwright: mở màn, thấy đúng dữ liệu phiếu ERP, đổi filter trạng thái → số dòng thay đổi, phân trang 100 dòng/trang chạy đúng.

### Task 4.2 — Màn chờ duyệt + menu

**Files:**
- Create: `hrm-client/pages/finance/bill-income-requests/pending.vue`
- Modify: `hrm-client/components/subsystem-menu/finance.js` (dòng 46, 82, 403)

- [x] **Bước 1:** `pending.vue` dùng lại component bảng của Task 4.1, gọi endpoint `/pending`, bỏ nút Tạo mới, thêm cột thao tác chỉ có Xem + In.
- [x] **Bước 2:** Gắn link cho 3 slot xám:
```js
{ label: 'Đề nghị thu tiền', link: '/finance/bill-income-requests' },                      // :46 và :82
{ label: 'Phiếu đề nghị thu tiền chờ duyệt', link: '/finance/bill-income-requests/pending' }, // :403
```
- [x] **Bước 3: Verify** — menu Tài chính hiện 3 mục sáng, click vào đúng route, không rơi vào `feature-unavailable`.

---

## Phase 5 — FE: form tạo / sửa + 3 popup

### Task 5.1 — Component form dùng chung

**Files (Create):**
- `hrm-client/components/finance/bill-income-request/BillIncomeRequestForm.vue`
- `hrm-client/components/finance/bill-income-request/BillIncomeRequestDetailTable.vue`
- `hrm-client/pages/finance/bill-income-requests/create.vue`
- `hrm-client/pages/finance/bill-income-requests/_id/edit.vue`

- [x] **Bước 1:** Đọc `form-validate`, `unsaved-changes`, `button-convention` SKILL.md trước khi code.
- [x] **Bước 2: Card "Thông tin chung"** — Loại thu (`typeForSelect`, 2 lựa chọn) · Loại tiền (từ danh mục tiền tệ) · Tỷ giá (khóa khi loại tiền = VND) · Lý do thu. Đổi Loại tiền → nạp lại tỷ giá mặc định.
- [x] **Bước 3: Card "Chi tiết"** — chưa chọn loại thu thì hiện *"Chưa chọn loại thu"*. Bảng động cột: STT · Khách hàng/NCC · Hợp đồng · Số tiền còn nợ (readonly) · Số tiền đề nghị thu · (VND quy đổi nếu ngoại tệ) · Ghi chú · nút xóa dòng; dòng Tổng cộng cộng 3 cột tiền.
- [x] **Bước 4: 4 quy tắc hành vi bắt buộc giữ giống ERP** (spec 4.7): đổi Loại thu → reset về 1 dòng trống · đổi KH/NCC trên dòng → xóa hợp đồng + công nợ + tiền + ghi chú của dòng đó · chưa chọn KH/NCC mà bấm chọn hợp đồng → toast cảnh báo · chọn trùng hợp đồng → toast *"Hợp đồng đã tồn tại!"*.
- [x] **Bước 5: 2 nút** Lưu (`status = 1`) và Lưu và gửi duyệt (`status = 2`) theo `button-convention`; chặn double-submit bằng cờ `loading`.
- [x] **Bước 6: Cảnh báo chưa lưu** — chọn đúng mixin theo mục 2b của skill `unsaved-changes` (trang form → `unsavedChangesMixin`).
- [x] **Bước 7: Verify Playwright** — tạo nháp 1 phiếu, F5 lại màn danh sách thấy phiếu mới; thoát form khi đang nhập dở → hiện popup "Thông tin chưa lưu".

### Task 5.2 — 3 popup chọn dữ liệu

**Files (Create):**
- `hrm-client/components/finance/bill-income-request/ChooseCustomerModal.vue` *(dùng lại endpoint `/assign/customers/search`)*
- `hrm-client/components/finance/bill-income-request/ChooseContractModal.vue`
- `hrm-client/components/finance/bill-income-request/ChooseSupplierModal.vue`

- [x] **Bước 1:** Đọc `.claude/skills/modal-popup/SKILL.md`. Select bên trong modal **bắt buộc** `V2BaseSelectInModal`; gọi `$nextTick()` trước `$bvModal.show()`.
- [x] **Bước 2: `ChooseContractModal`** gọi `/search-contracts` (type 1) hoặc `/search-buy-contracts` (type 2), cột: STT · Số hợp đồng · Ngày ký · Giá trị HĐ · Số tiền còn nợ; ô tìm theo số hợp đồng; chọn xong emit `{ object_id, object_code, object_type, dept_after_income_money }`.
- [x] **Bước 3:** 2 modal còn lại theo cùng khuôn (KH: mã/tên/loại KH; NCC: mã/tên).
- [x] **Bước 4: Verify Playwright** — mở từng popup, tìm kiếm, chọn 1 dòng, kiểm tra dữ liệu đổ đúng vào dòng chi tiết và cột công nợ hiện đúng số.

---

## Phase 6 — FE: chi tiết + Không duyệt + In

### Task 6.1 — Màn chi tiết + Không duyệt

**Files (Create):** `hrm-client/pages/finance/bill-income-requests/_id/index.vue`

- [x] **Bước 1:** Layout chỉ đọc, dùng lại `BillIncomeRequestDetailTable` ở chế độ `readonly`.
- [x] **Bước 2:** Nút **Không duyệt** chỉ hiện khi `is_can_reject` từ BE; mở modal nhập lý do (bắt buộc), gọi `POST /{id}/change-status` với `status = 6`.
- [x] **Bước 3:** **Không** render nút "Tạo phiếu thu" (ngoài phạm vi — màn Phiếu thu sẽ port ở feature sau). Ghi comment nêu rõ để người sau không tưởng là thiếu sót.
- [x] **Bước 4: Verify** — tài khoản kế toán không duyệt 1 phiếu → trạng thái đổi thành *Không duyệt*, người tạo mở lại sửa được.

### Task 6.2 — In phiếu

**Files (Create):** `hrm-client/pages/finance/bill-income-requests/_id/print.vue`

- [x] **Bước 1:** Đọc `.claude/skills/print-page/SKILL.md`.
- [x] **Bước 2:** BE `printData` trả dữ liệu theo 4 mẫu ERP (loại thu × loại tiền) — port `getPrintDataAttribute` + 2 hàm sinh bảng, bỏ phần bảng phiếu YCXH.
- [x] **Bước 3: Verify** — in 1 phiếu VND và 1 phiếu ngoại tệ, so bố cục với bản in ERP của cùng phiếu.

---

## Phase 7 — Verify tổng thể

### Task 7.1 — Đối chiếu số liệu 2 cổng

- [x] Đối chiếu số liệu HRM với **DB thật** (thay cho việc mở song song màn ERP — xem "CÒN NỢ" bên dưới):
  tổng phiếu nhìn thấy = tổng DB − nháp người khác (2.400 = 2.413 − 13); phiếu ERP mới nhất trả đủ 8/8 dòng
  chi tiết, mọi dòng resolve được mã hợp đồng; công nợ khớp 100% SQL thuần trên cả 2 nhánh TK 1311/3311.
- [x] Kiểm tra phân quyền bằng **3 tài khoản thật** (Super admin · kế toán công ty 3 · nhân viên không quyền):
  không quyền chỉ thấy 30 phiếu mình lập, gọi `/pending` và mở phiếu người khác đều **403**;
  kế toán công ty 3 thấy đúng 1 phiếu chờ duyệt của công ty mình.
- [x] **BỎ QUA — user chốt khi chốt hoàn thành (2026-08-14)**: không mở song song màn ERP để so từng ô
  trên giao diện, và chỉ test 3/4 cấp quyền (thiếu tài khoản thật cho đủ tổng cty / cty / phòng ban / bộ phận).

### Task 7.2 — Kiểm thử luồng chính

- [x] Vòng đời phiếu chạy bằng **ĐÚNG payload FE dựng** (`buildPayload`) qua HTTP thật: tạo nháp → sửa →
  gửi duyệt → không duyệt → sửa lại → xóa. 13/13 khẳng định đạt, gồm cả cờ `is_can_edit`/`is_can_reject`
  bật/tắt đúng theo từng trạng thái.
- [x] Playwright mở thật 4 màn trên `localhost:3000`: danh sách (10 dòng, đủ 9 cột) · thêm mới (đủ 6 nhãn,
  7 cột bảng chi tiết, 3 nút footer) · chi tiết (đúng nút theo quyền: In / Không duyệt / Quay lại) ·
  chờ duyệt (1 phiếu, **không có** nút Thêm mới). **0 lỗi console** ở cả 4 màn.
- [x] Màn in: đo bằng iframe khổ A4 trừ lề (190mm) theo skill `print-page` — tràn mép phải **0px**,
  `table-layout: fixed`, `border-collapse: collapse`, viền 4 cạnh mọi ô, logo URL tuyệt đối và tải được,
  0 thẻ `<input>` trong vùng in.
- [x] Theo memory `playwright_phantom_writes`: soát lại DB sau đợt test — tổng số phiếu **không đổi**,
  dòng chi tiết của phiếu test đã xóa hết, 29 notification test đã dọn.

### Task 7.3 — Regression rủi ro đã biết

- [x] `SELECT COUNT(*) FROM bill_income_request_detail_product_export_requests` = **0** trước và sau
  toàn bộ đợt test — HRM không ghi bảng này.
- [x] Popup không trả hợp đồng HRM trạng thái thấp; danh sách/chi tiết phiếu ERP cũ vẫn đọc bình thường
  sau khi HRM ghi (đã tạo/xóa phiếu nhiều lần).
- [x] **BỎ QUA — user chốt khi chốt hoàn thành (2026-08-14)**: không mở phiếu do HRM tạo **trên cổng ERP**
  để chụp lại lỗi `Class not found` thật (rủi ro spec 9.1 đã biết và user đã chấp nhận), và không kiểm tra
  chéo phiếu ERP cũ **bên giao diện ERP** (thiếu môi trường ERP chạy được + tài khoản ERP).

---

## Phase 8 — Fix bug sau nghiệm thu

### Task 8.1 — Bộ lọc: nhãn "Nhà cung cấp" hiện 2 lần
- [x] Xác định nguyên nhân: `V2BaseSmartFilterPanel.vue:126` đã render `<V2BaseLabel>{{ field.label }}</V2BaseLabel>`
      cho mọi field không khai `hideLabel`; slot `#field-supplier_id` ở page render thêm 1 nhãn nữa → lặp.
      Các field gộp nhiều ô (`org`, `income_money_range`, `created_range`) không dính vì đã có `hideLabel: true`.
- [x] Sửa `hrm-client/pages/finance/bill-income-requests/index.vue`: bỏ `<V2BaseLabel>Nhà cung cấp</V2BaseLabel>`
      trong slot, để panel là nơi DUY NHẤT render nhãn (trùng tên với popup "Cài đặt bộ lọc").
- [x] Verify: compile template bằng `vue-template-compiler` — 0 lỗi; chuỗi "Nhà cung cấp" trong template còn 1 (comment).
- [x] User mở trình duyệt xác nhận: bộ lọc chỉ còn 1 nhãn (2026-08-18).

**Quy tắc rút ra:** slot `#field-<key>` của `V2BaseSmartFilterPanel` chỉ tự render nhãn khi field khai
`hideLabel: true` (kèm `wrapperClass: 'd-contents'` nếu slot dựng nhiều cột). Field 1 ô → KHÔNG đặt label trong slot.

**Cùng lỗi ở màn Phiếu đề nghị chi tiền — user chốt sửa luôn 2026-08-18, đã sửa:**
`pages/finance/bill-payment-requests/index.vue` (`customer_id` + `supplier_id`) — ghi ở Task BF.1 của
`.plans/gop-db/finance-bill-payment-request/plan.md`. Đã rà 3 màn còn lại dùng `V2BaseSmartFilterPanel`
có slot tự render nhãn (`bill-adjust-dept-requests`, `device-errors`, `customer-care/serials`) — đều đã khai
`hideLabel: true`, không bị lặp.

### Task 8.2 — Bổ sung "Cấu hình cột hiển thị" + 2 cột Người/Ngày cập nhật
User chốt 2026-08-18: chỉ làm cho màn Phiếu đề nghị thu tiền; bộ cột mặc định GIỮ NGUYÊN như bản
đã nghiệm thu, thêm 2 cột mới cũng hiện mặc định (không ẩn cột nào của user đang dùng).

**BE** (`hrm-api`, 3 file sửa):
- [x] `BillIncomeRequest`: thêm quan hệ `employee_update()` (`belongsTo Employee, updated_by`).
- [x] `BillIncomeRequestService::searchByFilter()`: eager load thêm `employee_update.info` (chống N+1).
- [x] `BillIncomeRequestListResource`: trả thêm `updated_by_name` + `updated_at` (`d/m/Y H:i`).
- [x] Verify DB thật: 2.473 phiếu, **0 phiếu NULL `updated_by`** (hook `saving` ở boot() ghi cột này
      từ đầu, kể cả 2.4k phiếu nhập từ ERP) → cột không bị rỗng như cảnh báo ở skill list-page mục 6.

**FE** (`hrm-client/pages/finance/bill-income-requests/index.vue`):
- [x] `mixins: [..., columnCustomizationMixin]` + `columnScreenKey: 'finance_bill_income_requests'`
      (đã đối chiếu 12 khoá `finance_*` khác — không trùng). Màn chờ duyệt dùng chung khoá vì cùng bộ cột.
- [x] Đổi computed `tableColumns` → `allColumns`; thêm `locked: true` cho `index` + `code`
      (`actions` đã có sẵn) — đúng skill list-page mục 5: chỉ 3 cột này khoá.
- [x] Thêm 2 cột `updatedByName` (170px) + `updatedAt` (140px vì có giờ phút), đặt sau Ngày tạo,
      trước Trạng thái; kèm 2 template ô dữ liệu.
- [x] Nút mở popup (`ri-layout-column-line`) trong slot `#actions` + `<ColumnCustomizationModal>`.
- [x] `mounted`: `Promise.all([loadColumnFields(), loadData()])` — chạy song song, không thêm độ trễ vào màn.
- [x] Verify: compile template (`vue-template-compiler`) + parse script (babel) — 0 lỗi; không còn
      computed `tableColumns` cứng; relation trả dữ liệu thật (phiếu 2504 → "DNS Admin", 14/08/2026 15:40).
- [x] User test trình duyệt xong (2026-08-18): cấu hình cột, 2 cột Người/Ngày cập nhật, sort và độ rộng cột đều đạt.

**Đồng bộ định dạng ngày (user chốt 2026-08-18):**
- [x] `BillIncomeRequestListResource`: `created_at` đổi `d/m/Y` → **`d/m/Y H:i`**, khớp cột Ngày cập nhật
      (skill list-page mục 6). `BillIncomeRequestDetailResource` vốn đã `d/m/Y H:i` nên màn chi tiết + In
      không đổi gì.
- [x] FE: cột `createdAt` nới `110px` → **`140px`** (110px chỉ vừa phần ngày, thêm giờ là xuống dòng).

**Sắp xếp theo Ngày cập nhật (user chốt 2026-08-18):**
- [x] BE `BillIncomeRequest::applySort()`: thêm `updatedAt` / `updated_at` → cột DB `updated_at` vào
      whitelist (whitelist là bắt buộc — `sort_by` đi thẳng từ query string vào `orderBy`).
- [x] FE: cột `updatedAt` thêm `sortable: true` — chỉ bật sau khi BE nhận khoá này, bật trước thì user
      bấm mà bảng không đổi.
- [x] Verify SQL sinh ra: `updatedAt` + desc/asc → `order by updated_at desc|asc`; khoá lạ (`hackerCol`)
      → rơi về mặc định `order by created_at desc`, không nhét được vào SQL.

**Nới cột chữ dài (user chốt 2026-08-18):**
- [x] `reason` (Lý do thu) `minWidth: 280px`, `departmentName` (Phòng ban) `minWidth: 200px`.
- [x] Khai luôn `minWidth: 240px` cho `objectName` (Khách hàng / NCC) dù user không yêu cầu: 3 cột chữ
      dài của màn trước đó đều KHÔNG khai minWidth: nới 2 cột mà bỏ trống cột thứ 3 thì auto-layout lấy
      chỗ đúng từ cột đó, nó bị bóp xuống 4-5 dòng (skill list-page mục 15, đúng lỗi từng gặp ở màn chi tiền).

### Task 8.3 — Dropdown "Loại tiền" hiện kèm mã tiền tệ
User yêu cầu 2026-08-21: ô chọn Loại tiền chỉ hiện tên, khó phân biệt — hiện thêm mã theo dạng
`VND — Việt Nam Đồng` (đúng tiền lệ `AccountBankModal.vue` cùng phân hệ Tài chính).
Phạm vi user chốt: **chỉ dropdown Loại tiền**, không đụng nhãn cột bảng chi tiết và bản in.

- [x] `BillIncomeRequestForm.vue::loadOptions()`: `name` của option = `${c.code} — ${c.name}` cho **mọi** loại tiền
      (API `finance/currencies/getAll` đã trả sẵn `code`, không cần sửa BE). Giữ tên thuần ở khoá
      `short_name` — `currencyName` (nhãn cột số tiền ngoại tệ trong bảng chi tiết) phải hiện ĐÚNG tên,
      nếu dùng luôn `name` đã ghép thì header cột thành "VND — Việt Nam Đồng", vỡ layout 150px.
- [x] `currencyName()` đọc `short_name`, fallback `name` cho trường hợp thiếu code.
- [x] Sửa comment "không ghép mã — user chốt 2026-08-14" cho khỏi lạc hậu.
- [x] Verify: compile template + babel parse — 0 lỗi. DB thật (11 tiền tệ): `code` TRÙNG `name` ở 9/11 dòng
      (VNĐ|VNĐ, USD|USD, JPY|JPY…), chỉ EUR|EURO và INR|RUPEE khác nhau. Bản đầu ghép có điều kiện để tránh
      "VNĐ — VNĐ"; **user chốt 2026-08-21 ghép cho TẤT CẢ** để mọi dòng cùng một khuôn → bỏ điều kiện.
- [ ] User mở trình duyệt xác nhận.

### Task 8.4 — Popup chọn KH: ô "Tên / Mã khách hàng" tìm lan sang MST / SĐT / người tạo (2026-08-21)
User báo: gõ vào ô "Tên / Mã khách hàng" của popup mà ra cả những KH chẳng liên quan.
Nguyên nhân (đã trace, KHÔNG phải lọc theo nhóm KH): `CustomerService::index()` cho `keyword` khớp
**5 tiêu chí** — `code`, `fullname`, `tax_code`, `mobile` và **tên người tạo** (EXISTS sang
`employees` + `employee_infos`). Popup lại đã có 2 ô RIÊNG cho MST và SĐT → phần lan ra là dòng thừa.
Bằng chứng DB thật: keyword "Hùng" → **3.299 dòng**, trong đó **1.459 dòng** tên/mã KH không hề chứa
"Hùng" (vd `29TPHPKH-1 | A NAM`, `89THUXAN-1 | CÔNG TY TNHH ... ĐẠI ĐOÀN` — khớp nhờ tên người tạo).

- [x] BE `Modules/Assign/Services/CustomerService.php::index()`: thêm cờ `keyword_scope=code_name`
      → `keyword` chỉ khớp `customers.code` + `customers.fullname`. **Không đổi mặc định**: caller
      không gửi cờ (ô tìm nhanh màn danh sách KH `/assign/customers`) giữ nguyên 5 tiêu chí cũ.
- [x] FE `components/modals/ChooseErpCustomerModal.vue::getData()`: gửi `keyword_scope: 'code_name'`
      khi ô có chữ. Popup này dùng chung **8 màn** (meeting, dự án tiềm năng, yêu cầu bảo hành sửa chữa,
      phiếu điều chỉnh công nợ, phiếu ĐN thu tiền, phiếu thu, phiếu ĐN chi tiền, phiếu chuyển hàng)
      → cả 8 màn cùng đổi, đúng nghĩa nhãn ô.
- [x] **User chốt 2026-08-21 (sau khi được hỏi vì đây là popup + service DÙNG CHUNG): áp cho CẢ 8 màn**,
      không tách prop riêng cho màn phiếu thu/chi tiền. Ô nào ghi "Tên / Mã khách hàng" thì tìm đúng
      tên/mã ở mọi màn; MST và SĐT đã có ô riêng ngay cạnh.
- [x] Verify: `php -l` sạch; compile template + babel parse 0 lỗi; đếm trên DB thật keyword "Hùng":
      cũ 3.299 → mới 1.840 dòng, đúng bằng số dòng có tên/mã chứa từ khóa.
- [ ] User mở trình duyệt xác nhận.

### Task 8.5 — Lưu nháp không bắt buộc Lý do thu + bảng chi tiết (2026-08-21)
User chốt: nút **Lưu nháp** (status = 1) chỉ để cất dở dang → bỏ bắt buộc `reason` và cho phép chưa
có dòng chi tiết nào. Nút **Gửi duyệt** (status = 2) giữ nguyên ràng buộc cũ.

- [x] BE `BillIncomeRequestStoreRequest::rules()` (UpdateRequest kế thừa nên có luôn): rule động theo
      `status` — `reason` `nullable` khi nháp, `details` `nullable|array` khi nháp. Dòng ĐÃ thêm vẫn
      phải đủ hợp đồng + số tiền (nới nữa chỉ đẻ dòng rác không mở được).
- [x] BE `BillIncomeRequestService::store()` + `update()`: `'reason' => $request->get('reason') ?? ''`.
      ⚠️ Bắt buộc: cột `reason` là `text NOT NULL` không default, mà Laravel bật
      `ConvertEmptyStringsToNull` → ô trống về tới service là NULL, insert thẳng là nổ SQL 500.
      Nới validate mà quên chỗ này thì bug đổi từ "422 bắt nhập" thành "500 khi lưu".
- [x] FE: **không phải sửa** — `save()` chỉ chạy vee-validate (rule định dạng), required do BE quyết
      theo status. Nhãn "Lý do thu *" giữ dấu sao vì gửi duyệt vẫn bắt buộc.
- [x] Verify ma trận rule (Validator thật): nháp thiếu cả 2 → PASS · nháp details rỗng → PASS ·
      gửi duyệt thiếu cả 2 → FAIL đúng 2 khoá `reason`, `details` · gửi duyệt details rỗng → FAIL `details`.
- [x] Verify SQL thật: `store()` với `reason = null`, `details = []` → tạo được phiếu, `reason` lưu `''`,
      0 dòng chi tiết (chạy trong transaction rồi rollback, không để lại dữ liệu rác).
- [ ] User mở trình duyệt xác nhận.

### Task 8.6 — Popup chọn KH giữ nguyên bộ lọc sau khi đóng (2026-08-21)
User báo: tìm khách hàng xong đóng popup, mở lại vẫn thấy đúng kết quả đã lọc — tưởng hệ thống chỉ
còn bấy nhiêu KH. Nguyên nhân: `ChooseErpCustomerModal.onModalShow()` cố ý `if (!this.loaded)` —
chỉ tải lần đầu, các lần sau giữ nguyên `filter` / `filterTaxCode` / `filterPhone` / `currentPage`.

- [x] `components/modals/ChooseErpCustomerModal.vue::onModalShow()` → gọi `resetSearch()`: xoá 3 ô lọc,
      về trang 1, `perPage` 10 rồi `getData()`. Mỗi lần mở là một lượt tìm mới.
- [x] Bỏ cờ `loaded` (data + phép gán trong `getData`): sau thay đổi trên không còn ai đọc nó.
- [x] Verify: compile template + babel parse — 0 lỗi; grep `loaded` chỉ còn trong comment giải thích.
- [ ] User mở trình duyệt xác nhận (popup này dùng chung 8 màn, xem Task 8.4).

**2 popup còn lại của màn — user chốt sửa luôn 2026-08-21, ĐÃ SỬA:**
- [x] `ContractSearchModal.vue` (chọn hợp đồng) + `SupplierSearchModal.vue` (chọn NCC): `onShow()`
      trước chỉ `currentPage = 1` + `loadData()`, giữ nguyên ô tìm → đổi sang gọi `resetSearch()`
      (xoá `keyword`, về trang 1, loadData). Không phát sinh lượt gọi API thừa: cả 2 nhánh đều
      tải đúng 1 lần khi mở.
- [x] Verify: compile template + babel parse cả 2 file — 0 lỗi.

### Task 8.7 — Lỗi validate của dòng chi tiết đã xoá vẫn bám sang dòng mới (2026-08-21)
User báo: thêm dòng → bấm Lưu → dòng báo "Bắt buộc nhập" → xoá dòng đó, thêm dòng khác → vẫn thấy
nguyên câu lỗi cũ. Nguyên nhân: `formErrors` khoá theo **VỊ TRÍ** dòng (`details.0.object_id`) trong khi
`removeDetail()` chỉ `splice` mảng dữ liệu → lỗi cũ nằm lại đúng ô đó, dòng thêm mới hứng luôn.
vee-validate không quản mảng này nên không ai xoá hộ (khác các ô cấp phiếu).

- [x] `BillIncomeRequestForm.vue`: thêm `shiftDetailErrors(removedIndex)` — xoá lỗi của dòng vừa xoá và
      **dồn index** lỗi của các dòng phía sau lên 1; `removeDetail()` gọi ngay sau `splice`.
- [x] Thêm `clearAllDetailErrors()` và gọi trong `onTypeChange()` (đổi loại thu = xoá trắng bảng):
      không dọn thì dòng đầu tiên thêm lại sau đó lại hứng lỗi của dòng 0 lần trước.
- [x] Lỗi cấp phiếu (`reason`) và lỗi cấp mảng (`details`) KHÔNG bị đụng khi dồn index.
- [x] Verify: compile template + babel parse 0 lỗi; chạy thử hàm dồn index trên 3 tình huống —
      1 dòng lỗi bị xoá → sạch · xoá dòng giữa của 3 dòng → `details.2.*` tụt về `details.1.*` ·
      có `reason` + `details` → giữ nguyên.
- [ ] User mở trình duyệt xác nhận.

### Task 8.8 — Bổ sung cột "Người nộp" + đổi tiêu đề "Lý do nộp" + bộ lọc Người nộp (2026-08-22)
User yêu cầu thêm thông tin **Người nộp** và **Lý do nộp** vào bảng danh sách (kèm popup Tùy chỉnh cột)
và thêm ô lọc **Người nộp**. Đối chiếu ERP:
`resources/views/income_expenditure/bill_income_requests/approved.blade.php:50-51` và
`forAccounting.blade.php:51-52` — màn CHỜ DUYỆT có 2 cột `reason` ("Lý do nộp") + `payer` ("Người nộp"),
thứ tự `Số tiền → Lý do nộp → Người nộp → Ngày lập`; `index.blade.php:49` chỉ có `reason`.
Ô lọc `payer` `search_type: 'text'` có ở CẢ 3 màn (`index:64`, `approved:66`, `forAccounting:67`).
HRM dùng chung 1 component cho danh sách + chờ duyệt (`pending.vue` → `<BillIncomeRequestList pending-mode />`,
chung khoá cột `finance_bill_income_requests`) nên chỉ khai 1 chỗ là cả 2 màn cùng có.

Nguồn dữ liệu: cột thô `bill_income_requests.payer` — ERP không `editColumn('payer')` nên yajra xuất
thẳng cột này (kiểm chứng trên prod `erp-crm.eteksofts.com/.../for-accounting`: 20/20 phiếu chờ duyệt
hiện "Người nộp 1…9", đúng dữ liệu seed `TEST.DNTT.*`). Form đề nghị (cả ERP lẫn HRM) KHÔNG có ô nhập
`payer` → phiếu nghiệp vụ cũ để trống, đúng như ERP.

- [x] BE `BillIncomeRequestListResource.php`: thêm `payer` vào payload (cột nằm sẵn trên bảng, không N+1).
- [x] BE `BillIncomeRequest::searchByFilter()`: thêm nhánh lọc `payer` LIKE `%…%` (khớp `search_type: text` của ERP).
- [x] FE `index.vue` — `allColumns`: đổi title cột `reason` "Lý do thu" → "Lý do nộp"; thêm cột `payer`
      ("Người nộp") ngay sau `reason`, đúng thứ tự ERP.
- [x] FE `index.vue` — `initialStateForm` thêm `payer: ''`; `filterFields` thêm field text "Người nộp"
      đặt cạnh "Người tạo".
- [x] Verify: `php -l` 2 file BE sạch · `vue-template-compiler` + babel parse `index.vue` sạch ·
      chạy `searchByFilter` thật (tinker, đăng nhập id 13): SQL ra `and \`payer\` like ?` với
      **binding** `%Người nộp 2%` (không nội suy chuỗi) — 11/2491 phiếu khớp; `BillIncomeRequestListResource`
      trả khoá `payer` đúng giá trị (TEST.DNTT.00062/00004/00071).
- [ ] User mở trình duyệt xác nhận.

### Task 8.9 — Bảng chi tiết thiếu dòng "Tổng cộng" ở form tạo/sửa (2026-08-22)
User báo màn `finance/bill-income-requests/create` không có dòng tổng dưới bảng chi tiết như ERP.
ERP có dòng này ở CẢ form nhập (`form.blade.php:305-313`) lẫn màn xem (`formShow.blade.php:203`),
cộng 3 cột: `total_dept_after_income_money` (ẩn khi `type == 3`) · `total_income_money_request` ·
`total_income_money_request_exchange` (chỉ khi loại tiền ≠ VND). Tổng tính ở FE, không thêm API.

- [x] `BillIncomeRequestForm.vue`: 3 computed `totalDeptAfterIncomeMoney` / `totalIncomeMoneyRequest` /
      `totalIncomeMoneyRequestExchange` — `reduce` + `Number(x || 0)` để ô trống không ra `NaN`.
- [x] Thêm dòng cuối `<tbody>` (`v-if="form.details.length"`): `colspan=3` nhãn "Tổng cộng" + 3 ô số
      căn phải, ô Ghi chú và ô Xóa để trống; số ô tự khớp `isVnd` / `readonly`.
- [x] Style `.detail-total-row td` — nền `#f5f6f8` + `font-weight: 600` (ERP dùng `<b>`).
- [x] Màn chi tiết (readonly) dùng chung component nên có luôn dòng tổng, đúng như `formShow` của ERP.
- [x] Verify: compile template + babel parse sạch · chạy thử hàm cộng với dữ liệu lẫn `null`/`''`/chuỗi
      → không `NaN` (4.000.000 / 1.000.250,5 / 31.262.500) · đối chiếu số ô dòng tổng với số cột header
      ở cả 4 tổ hợp `isVnd` × `readonly` → khớp 6/7/7/8, không lệch cột.
- [ ] User mở trình duyệt xác nhận.

### Task 8.10 — Mở 2 tab cùng 1 phiếu: báo nhầm "không có quyền" (2026-08-22)
User báo: tab 1 mở Sửa phiếu A · tab 2 cũng mở A rồi bấm **Lưu và gửi phiếu** · tab 1 bấm Lưu →
hiện "Bạn không có quyền". Sai bản chất: đây là **xung đột dữ liệu**, không phải thiếu quyền.

Nguyên nhân: `canEdit()` gộp 2 điều kiện (`status ∈ {Đang tạo, Không duyệt}` **và**
`created_by == mình`), Controller chỉ có 1 nhánh `if (!canEdit()) → 403`. Tab 2 gửi duyệt xong thì
`status` đổi sang "Chờ KT duyệt" → tab 1 rớt vào đúng nhánh 403 đó.

- [x] Entity: tách `isEditableStatus()` (chỉ xét trạng thái) khỏi `canEdit()`; `canEdit()` gọi lại
      hàm mới nên hành vi cũ không đổi (`is_can_edit`/`is_can_delete` của Resource giữ nguyên).
- [x] Controller `update()` + `destroy()`: xét **người lập trước** (403 "Bạn không có quyền…"),
      **trạng thái sau** (409 + câu user yêu cầu). Đảo thứ tự là phiếu của người khác đã gửi duyệt
      sẽ báo nhầm "dữ liệu đã thay đổi". Câu thông báo đặt ở hằng số `MSG_STATUS_CONFLICT`.
      Bám tiền lệ `BillPaymentApprovalFlowService.php:175-178` (tách 409 khỏi 403).
- [x] FE **không phải sửa**: `applyServerErrors()` chỉ nuốt lỗi có mảng `errors` (422), còn lại
      rơi xuống toast `error.response.data.message` — cả nhánh Lưu (`:959`) lẫn Xóa (`:1032`).
- [x] Verify qua **chính endpoint thật** (HTTP kernel + token JWT, chạy trong transaction rồi
      `rollBack()` nên không đụng dữ liệu thật — đã đối chiếu `status`/`created_by` sau rollback
      khớp ban đầu). Phiếu `TEST.DNTT.00089`:
      · tab 2 gửi duyệt trước → tab 1 Lưu = **HTTP 409** + đúng câu
      "Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng
      khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất."
      · phiếu của người khác (còn sửa được) = **HTTP 403** "Bạn không có quyền sửa phiếu này" (giữ nguyên).
      `php -l` 2 file sạch.
- [ ] User mở trình duyệt xác nhận (mở 2 tab như kịch bản đã mô tả).

- [x] **Không duyệt** (`changeStatus`) — user chốt 2026-08-22 thống nhất luôn: nhánh
      "phiếu không còn ở Chờ KT duyệt" đổi **422 → 409** + dùng chung `MSG_STATUS_CONFLICT`
      (422 là lỗi dữ liệu nhập, đây là xung đột trạng thái). Nhánh 403 "Bạn không có quyền duyệt"
      và nhánh 422 của `note` (FormRequest) giữ nguyên.
      Verify qua endpoint thật (transaction + rollback, `status` sau rollback = 2 như ban đầu):
      phiếu `TPE.DNTT0826.00003`, kế toán id 13 → kế toán khác vừa xử lý xong = **HTTP 409** +
      đúng câu thông báo. FE nhánh Không duyệt (`:1012`) cũng đi qua `applyServerErrors()` nên
      hiện thẳng `message`, không phải sửa.

### Task 8.11 — Bỏ nút "Xem chi tiết" ở danh sách phiếu đề nghị thu (2026-08-22)
User chốt: cột **Mã phiếu** đã là link vào màn chi tiết nên nút con mắt là lối đi thứ 2 cho cùng
một việc → bỏ.

- [x] `pages/finance/bill-income-requests/index.vue` — `getRowActions()`: xoá action `view`.
- [x] Xoá luôn nhánh `case 'view'` trong `handleRowAction()` (đã thành code chết) + sửa 2 docblock
      còn ghi "màn chờ duyệt chỉ Xem + In".
- [x] Màn **chờ duyệt** dùng chung component nên cũng mất nút này — vẫn vào chi tiết được qua link
      Mã phiếu, bộ nút còn In / Tạo phiếu thu.
- [x] Verify: parse template + script sạch; grep không còn `'view'` / `ri-eye-line` / "Xem chi tiết"
      (chỉ còn trong chú thích). Gọi thẳng `getRowActions()` trên component đang chạy ở
      localhost:3000 với item đủ cờ quyền → trả về đúng 4 nút
      `edit | create_bill_income | print | delete`, `conKeyView = false`.
- [ ] User mở trình duyệt xác nhận.

### Task 8.12 — Bảng chi tiết: thanh cuộn ngang phía TRÊN (2026-08-22)
User yêu cầu đồng bộ với màn Đề nghị thanh toán / `customer-care/warranty-repair-requests/create`.

- [x] `BillIncomeRequestForm.vue`: bọc bảng chi tiết bằng component dùng chung **`V2BaseTableScroll`**
      (thanh cuộn ngang ở CẢ trên và dưới, đồng bộ 2 chiều, tự ẩn khi bảng không tràn),
      `body-class="table-responsive"` giữ khuôn cũ.
- [x] Đổi `width` → `min-width` cho **8 cột nội dung** của header (giữ `width` cho STT + nút thêm dòng):
      `width` chỉ là gợi ý nên màn hẹp là cột bị bóp, bảng không tràn và thanh cuộn không bao giờ hiện.
- [x] Verify trên trình duyệt (khung 900px): bảng **1059** > khung **852** → thanh trên **hiện**, nằm
      đúng phía trên bảng; kéo thanh trên 180 → bảng chạy 180; kéo bảng 45 → thanh trên về 45.
      Dòng **Tổng cộng** (Task 8.9) vẫn nằm trong vùng cuộn, không bị lệch. Parse sạch.
- [ ] User xác nhận.

### Checkpoint — 2026-08-18 (thêm cấu hình cột)
Vừa hoàn thành: Task 8.2 — popup Cấu hình cột hiển thị + 2 cột Người/Ngày cập nhật (3 file BE, 1 file FE).
Đang làm dở: không có.
Bước tiếp theo: user kiểm trên trình duyệt.
Việc để sau (user chốt 2026-08-18): làm cấu hình cột cho **màn Phiếu đề nghị chi tiền** — màn đó cũng
chưa có mixin/nút/modal, cách làm y hệt Task 8.2 (khoá gợi ý `finance_bill_payment_requests`).
Blocked: không.

### Task 8.3 — Seeder dữ liệu test: đủ 3 loại hợp đồng bán + đủ trạng thái
User yêu cầu 2026-08-19: seeder `BillIncomeRequestTestDataSeeder` mới chỉ sinh hợp đồng BÁN
(`hrm_contracts`), thiếu 2 nguồn còn lại mà popup "Chọn hợp đồng" union vào; cần đủ cả 3 loại và
phủ hết trạng thái, đồng thời in ra danh sách khách hàng / NCC để biết chọn ai khi test.

- [x] Bước 1a (hợp đồng bán) phủ ĐỦ 10 trạng thái của `Contract` (thêm 1 Đã duyệt + 7 Chờ hiệu lực).
      Hàng đợi trạng thái ưu tiên cái CÒN THIẾU nên chạy bổ sung trên tập cũ vẫn vá được;
      `$need = max(target - đã có, số trạng thái thiếu)` — đủ số lượng mà thiếu trạng thái vẫn tạo bù.
- [x] Bước 1b MỚI — hợp đồng ĐẦU KỲ (`opening_contracts`, tiền tố `HĐ-TEST-DNTT-DK-`), mặc định 12 cái
      (`FINANCE_TEST_OPENING`). Bảng KHÔNG có cột `status`/`total_*` → popup luôn hiện, cột Tổng giá trị
      luôn 0 (service select `0 as total_value`), số có nghĩa duy nhất là Số tiền còn nợ.
- [x] Bước 1c MỚI — hợp đồng BẢO DƯỠNG/DỊCH VỤ (`wr_service_contracts`, tiền tố `HĐ-TEST-DNTT-BD-`),
      mặc định 14 cái (`FINANCE_TEST_WR`), phủ đủ 7 trạng thái có thật (1,2,3,4,5,10,11). Popup KHÔNG lọc
      trạng thái nguồn này. `created_at` để gần hiện tại — khách hàng thật có hàng chục hợp đồng bảo dưỡng,
      để ngày cũ là hợp đồng mẫu tụt xuống trang 3-4.
- [x] 2 bảng trên là bảng ERP dùng chung, entity HRM khai read-only → seeder ghi bằng query builder.
      Cột NOT NULL không mặc định của `wr_service_contracts` (`customer_address`, `customer_contact_name`,
      `customer_name`, `customer_type`, `company_account_number`, `approver_id`) phải truyền đủ.
- [x] Khách hàng của 2 loại mới lấy LẠI từ hợp đồng bán mẫu → 1 khách hàng có đủ 3 loại trong popup.
- [x] Bước 2 (công nợ TK 1311) chạy cho CẢ 3 loại, khoá theo `contractable_type` thật; đổi từ
      "đã có bút toán mẫu thì bỏ qua cả bước" sang bỏ qua theo TỪNG hợp đồng (không thì hợp đồng mới
      thêm sẽ mãi không có công nợ).
- [x] Bước 3 (phiếu): danh sách hợp đồng trộn XEN KẼ theo loại (`interleaveByKind`) nên 1 phiếu nhiều
      dòng gom được cả 3 loại; `objectable_type` + tra công nợ dùng `type` của từng hợp đồng.
- [x] Bước MỚI — in danh sách KHÁCH HÀNG (kèm số hợp đồng từng loại) và NHÀ CUNG CẤP đang dùng trong
      phiếu mẫu, để mở form tạo phiếu là biết gõ tên nào. Cảnh báo `is_supplier=0` nếu có.
- [x] Verify: chạy thật trên `gop_db` — 42 hợp đồng bán (đủ 10 trạng thái), 12 đầu kỳ, 14 bảo dưỡng
      (đủ 7 trạng thái), 46 bút toán mới, 30 phiếu mới (dòng chi tiết: 35 bán / 14 đầu kỳ / 11 bảo dưỡng).
      Gọi thẳng `searchSellContracts(customer_id=18505)` → trang 1 có đủ 3 loại kèm số còn nợ thật.

## Checkpoint

### Checkpoint — 2026-08-19 (seeder đủ 3 loại hợp đồng)
Vừa hoàn thành: Task 8.3 — mở rộng `BillIncomeRequestTestDataSeeder` (1 file BE) sang hợp đồng đầu kỳ
+ bảo dưỡng/dịch vụ, phủ hết trạng thái, in danh sách khách hàng / NCC để chọn khi test.
Đang làm dở: không có. Đã chạy thật trên DB `gop_db`.
Bước tiếp theo: user vào màn tạo phiếu chọn thử 1 khách hàng trong danh sách in ra (gợi ý #18505,
#916, #13102 — có đủ cả 3 loại) và kiểm popup.
Blocked: không.

### Checkpoint — 2026-08-18 (USER TEST XONG)
Vừa hoàn thành: user test trình duyệt xong toàn bộ Phase 8 — không báo lỗi. Feature trở lại trạng thái
HOÀN THÀNH.
Đang làm dở: không có. **User đã commit**: `hrm-api` `bb4863e0e` "fix bug phiếu đề nghị thu tiền"
(3 file) · `hrm-client` `dde97025c` "fix bug" (index.vue của cả 2 màn + package-lock.json).
Bước tiếp theo: việc để sau — cấu hình cột cho màn Phiếu đề nghị chi tiền.
Blocked: không.

### Checkpoint — 2026-08-18 (hết phiên: Phase 8 xong code)
Vừa hoàn thành: **Task 8.1 + 8.2 trọn vẹn** — 4 file BE (`BillIncomeRequest` relation `employee_update`
+ whitelist sort `updated_at` · `BillIncomeRequestService` eager load · `BillIncomeRequestListResource`
2 field mới + `created_at` sang `d/m/Y H:i`) và 1 file FE (`pages/finance/bill-income-requests/index.vue`:
bỏ nhãn lọc lặp · mixin cấu hình cột + nút + modal · `tableColumns` → `allColumns` + `locked` 3 cột ·
2 cột Người/Ngày cập nhật có sort · nới `minWidth` 3 cột chữ dài).
Đang làm dở: không có. **Chưa commit** (đúng quy tắc: chỉ commit khi user yêu cầu).
Bước tiếp theo: user mở trình duyệt kiểm 5 điểm — (1) bộ lọc chỉ còn 1 nhãn "Nhà cung cấp";
(2) popup Cấu hình cột: đủ cột, STT/Mã/Hành động xám, kéo thả + F5 còn giữ; (3) 2 cột Người/Ngày cập
nhật có dữ liệu; (4) bấm sắp xếp cột Ngày cập nhật đổi thứ tự thật; (5) 3 cột chữ dài không bị bóp.
Blocked: không.
Việc để sau (user chốt): làm cấu hình cột cho **màn Phiếu đề nghị chi tiền** (`finance_bill_payment_requests`).

### Checkpoint — 2026-08-18 (fix bug bộ lọc)
Vừa hoàn thành: Task 8.1 — bỏ nhãn "Nhà cung cấp" lặp ở bộ lọc màn danh sách (1 file FE).
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt xác nhận; chốt có sửa luôn 2 nhãn lặp tương tự ở màn Phiếu đề nghị chi tiền không.
Blocked: không.

### Checkpoint — 2026-08-14 (CHỐT HOÀN THÀNH)

Vừa hoàn thành: **user test trình duyệt xong**, chốt feature **HOÀN THÀNH**. STATUS.md đã chuyển
entry từ "Đang làm" sang "Hoàn thành".
Đang làm dở: không có.
2 việc "CÒN NỢ" ở Task 7.1 / 7.3 (đối chiếu trực tiếp trên giao diện ERP · test đủ 4 cấp quyền)
**user chốt bỏ qua**, không làm thêm.
Bước tiếp theo: user tự commit khi muốn (repo chưa commit theo quy tắc "không commit khi user chưa yêu cầu").
Blocked: không.

### Checkpoint — 2026-08-14 (HẾT PHASE 4→7 — TOÀN BỘ MÀN ĐÃ XONG)
Vừa hoàn thành: **Phase 4, 5, 6, 7** — toàn bộ frontend + verify tổng thể.

**FE mới (9 file, `hrm-client`):**
`pages/finance/bill-income-requests/` → `index.vue` (danh sách, dùng chung cho cả màn chờ duyệt qua
prop `pendingMode`) · `pending.vue` · `create.vue` · `_id/edit.vue` · `_id/index.vue` (chi tiết +
modal Không duyệt) · `_id/print.vue` · `components/BillIncomeRequestForm.vue` ·
`components/ContractSearchModal.vue` · `components/SupplierSearchModal.vue`.
**FE sửa:** `components/subsystem-menu/finance.js` (gắn link 3 slot xám).
**BE sửa thêm:** message `exchange_rate.gt` → 'Phải lớn hơn 0' (khớp nguyên văn rule FE `positive_vn`);
seeder gán thêm 5 quyền mới cho role **Super admin**.

**Kết quả verify (chi tiết ở Task 7.1-7.3):** contract FE↔BE tự động 4 nhóm — 0 vấn đề;
vòng đời phiếu bằng payload FE thật 13/13 đạt; Playwright 4 màn **0 lỗi console**; màn in tràn mép phải 0px.

🐛 **Lỗi thật phát hiện khi test Playwright**: màn chờ duyệt đá về `/pages/extras/404` với **Super admin** —
`middleware/checkPermission.js` chỉ so tên quyền trong `store.state.permissions`, KHÔNG có nhánh bỏ qua cho
super admin, trong khi BE (`isAccountant()`) lại cho phép. Role 18 giữ 2.148 quyền api nhưng chưa có 5 quyền
mới. Đã sửa seeder để gán cả role 18 → màn mở được, khớp lại hành vi BE.

🐛 **Lỗi thứ 2 — user phát hiện khi review: form KHÔNG bám base của màn khách hàng.**
Đợt đầu tôi chép khuôn từ `ProductTransferRequestForm.vue` (màn anh em cùng phân hệ) thay vì màn mẫu
khách hàng như user đã dặn. Hệ quả nặng hơn "khác giao diện": các class `form-card` / `form-card-head` /
`form-header` / `header-icon` / `readonly-cell` **KHÔNG có trong `v2-styles.scss`** — chúng nằm trong
`<style>` RIÊNG của `ProductTransferRequestForm.vue` mà tôi không chép sang → form và màn chi tiết render
bằng div trơn, mất hết khung/nền/viền.
**Đã sửa cả 2 màn (form + chi tiết) sang đúng khuôn `CustomerForm.vue` bản mới:**
· khối = `<div class="card">` + `card-header py-2` + `<h6 class="mb-0 font-weight-bold">` + `card-body`
  (class Bootstrap có CSS thật) · bỏ hẳn khối header tự chế (tên màn đã do `PageTitleMixin` hiện)
· dấu bắt buộc = `<Required />` (`components/common/Required`) thay cho prop `required` / `<span class="text-danger">`
· lỗi inline = `<div class="text-small-error mt-1"><i class="ri-error-warning-line mr-1"></i>{{ fieldError(...) }}</div>`
  — đúng như màn KH (file đó dùng 31 lần, **0 lần** dùng `V2BaseError`)
· ô chỉ đọc = `V2BaseInput :disabled="true"` thay cho `<input class="form-control readonly-cell">`
**Đo đối chiếu bằng Playwright — khớp 100% với `/assign/customers/add`:**
card `bg #FFF · border-top 0.8px · radius 4px · margin-bottom 24px`, header `bg rgb(237,239,241) · padding-top 12px`,
h6 `12px`. Nhãn hiện đúng "Loại thu *", 3 card có style thật, 0 lỗi console.
📌 Bài học: trước khi chép khuôn từ màn khác, phải kiểm tra class đó nằm ở `v2-styles.scss` (dùng chung)
hay ở `<style>` riêng của màn đó — chép template mà bỏ style là mất sạch giao diện.

🔁 **Đợt sửa thứ 3 — user yêu cầu "form sửa giống form bên ERP":** dựng lại bố cục + luồng nhập bám đúng
`erp/resources/views/income_expenditure/bill_income_requests/form.blade.php` (khung vẫn dùng base HRM):

| Hạng mục | Trước | Sau (theo ERP) |
| --- | --- | --- |
| Bố cục Thông tin chung | 4 cột đều nhau | 2 cột `col-md-6`: Mã phiếu · Loại thu · (Loại tiền + Tỷ giá chung 1 cột) · Người tạo · Phòng ban · Lý do thu |
| Header card | chỉ tiêu đề | thêm "người tạo - ngày lập" ở góc phải (ERP `<% form.creator %> - <% form.created_time %>`) |
| Tỷ giá | ô trơn | `input-group` + addon **VND**, khoá ô khi loại tiền là VND |
| Người nộp tiền | có ô nhập | **BỎ** — form ERP không có ô này (BE để `payer` nullable nên không chặn lưu) |
| Bảng chi tiết | luôn hiện | chỉ hiện sau khi chọn Loại thu (ERP `ng-if="form.type"`) |
| Header bảng | 1 tầng | **2 tầng**: cột "Số tiền đề nghị thu" `colspan` 2 khi ngoại tệ, tầng dưới là tên loại tiền / VND |
| Thêm dòng | nút "Chọn hợp đồng" ngoài bảng | dấu **+** ở ô cuối header bảng, thêm 1 dòng TRỐNG |
| Chọn KH/NCC | 1 lần cho cả phiếu | **theo TỪNG DÒNG** — ô readonly + nút kính lúp trên mỗi dòng |
| Chọn hợp đồng | popup chung của phiếu | nút kính lúp trên dòng, popup lọc theo KH **của chính dòng đó**, chọn xong tự đóng (`close-on-choose`) |
| Bảng rỗng | "Chưa có dòng nào…" | "Không có dữ liệu" (nguyên văn ERP) |
| Xóa dòng | `V2BaseIconButton` | icon thùng rác đỏ dạng link, đúng vị trí ERP |

⚠️ Chọn đối tượng **theo dòng** không phải chi tiết thẩm mỹ mà là yêu cầu dữ liệu: đã đếm trên DB thật —
**1.128/2.411 phiếu ERP (46%) có từ 2 khách hàng trở lên** trong cùng một phiếu, cao nhất **25 khách hàng**.
Mô hình cũ (1 khách hàng/phiếu) sẽ không nhập nổi gần một nửa số phiếu thực tế.

Verify Playwright: 4 nhãn đúng (không còn "Người nộp tiền"), addon "VND" hiện, header bảng đúng
`rowspan=2`/`colspan`, bấm **+** ra dòng có 2 nút kính lúp + nút xóa, nút hợp đồng **khoá** khi chưa chọn KH
(title "Chọn khách hàng trước"), chọn KH xong ô điền `50TPHXBI-277 - CÔNG TY TNHH THƯƠNG MẠI MẪU` và nút
hợp đồng mở khoá, popup hợp đồng mở đúng KH của dòng với 5 cột y như ERP.

🔁 **Đợt sửa 4 (user báo "màn xem chi tiết và màn danh sách đang khác màn mẫu")** — đối chiếu lại
`pages/assign/customers/index.vue` + `_id/index.vue` và sửa cho khớp:

| Hạng mục | Trước | Sau (theo màn KH) |
| --- | --- | --- |
| Bộ lọc | `V2BaseFilterPanel` (khai tay từng ô) | **`V2BaseSmartFilterPanel`** + schema `filterFields` → có nút "Cài đặt bộ lọc", user tự bật/tắt + kéo sắp xếp |
| Nút toolbar | slot `#actions-bottom`, nhãn "Thêm mới" | slot `#actions`, nhãn **"Tạo mới"** |
| Hành động dòng | hàng icon nhét dưới mã phiếu | **cột "Hành động" riêng** + `V2BaseRowActions` (tự gom vào menu "…" khi quá 3 nút) |
| Link mã | `font-weight-bold text-primary` | `v2-cell-link field-line` |
| Ô chữ | `<span class="field-line">` | `<div class="field-line text-dark font-weight-normal">` |
| Badge trạng thái | không icon | có icon (`ri-checkbox-circle-line` / `ri-time-line`) |
| Sắp xếp | không có | `@sort` + `sortBy`/`sortDirection`, cột Mã phiếu + Ngày tạo cho sort |
| **Màn chi tiết** | file riêng, tự vẽ `.field-value` | **KHÔNG có màn riêng** — dùng lại chính form với prop `readonly`, y như `customers/_id/index.vue` dùng lại `CustomerForm` |

**BE thêm**: `BillIncomeRequest::applySort()` nhận `sort_by` + `sort_desc`, **whitelist tên cột**
(`code` · `createdAt`/`created_at` · `status` · `type`) — nhét thẳng `sort_by` từ query string vào
`orderBy()` là lỗ SQL injection.

**Chế độ `readonly` của form**: khoá mọi ô · ẩn nút **+** thêm dòng và nút xoá dòng · ô Số tiền/Ghi chú
đổi sang text · chặn bấm ô Khách hàng/Hợp đồng mở popup (guard trong method + `cursor: default`) ·
`unsavedSnapshotSource()` trả `null` để không bao giờ hỏi "chưa lưu" · footer đổi sang bộ nút màn xem
(**Sửa** theo cờ BE + `#custom-actions`: In phiếu · Không duyệt · Xóa).

🐛 **Lỗi hạ tầng phát hiện kèm**: bảng `filter_customizations` **chưa có trên DB dev** dù migration
`Modules/Human/.../2026_08_12_000000_create_filter_customizations_table.php` đã nằm trong repo →
`GET human/filter-customizations/detail` trả **400** cho MỌI màn dùng SmartFilterPanel, **kể cả màn
khách hàng** (component catch nên màn vẫn chạy, chỉ lỗi đỏ trong console). Đã chạy migration đó
(`php artisan migrate --path=...`) → hết lỗi ở cả 2 màn.

Verify Playwright: danh sách đủ **11 cột** (có "Hành động"), nút "Cài đặt bộ lọc" + "Tạo mới" hiện,
link mã đúng class `v2-cell-link field-line`, badge có icon, hành động dòng của phiếu người khác chỉ
còn **Xem chi tiết + In phiếu** (ẩn Sửa/Xóa đúng cờ BE), **0 lỗi console**.
Màn chi tiết: 3 card giống form, **7/7 ô đều khoá**, không có nút thêm/xoá dòng, ô Khách hàng hiện
`29TPHPXU-4 - CÔNG TY CỔ PHẦN HYUNDAI PHẠM VĂN ĐỒNG` và ô Hợp đồng `HĐ-TEST-DNTT-02` với
`cursor: default`, bấm vào **không mở popup**, footer đúng: In phiếu · Không duyệt · Quay lại.

📌 **NÚT "TẠO PHIẾU THU" — ĐÃ DỰNG SẴN, ĐANG KHOÁ (user chốt 2026-08-14, để không quên chức năng).**

Làm rõ hiểu nhầm trước đó: **ERP KHÔNG có nút "Duyệt" riêng**. Màn chi tiết phiếu đề nghị thu bên ERP
(`show.blade.php:19-26`) chỉ có ĐÚNG 2 nút, cùng gate `can('Kế toán thanh toán') && status == 2`:
**"Tạo phiếu thu"** (= đồng ý, link sang `bill_income.create?bill_income_request_id={id}`) và
**"Không duyệt"**. Tức là *duyệt chính là hành động lập phiếu thu*.

Trạng thái phiếu đề nghị KHÔNG tự đổi mà bị màn Phiếu thu đẩy:
· `BillIncome::updateStatusAndSendNotifyBillIncomeRequest()` → **3 Đã tạo phiếu thu** (+ ghi `approved_id`,
  bắn thông báo cho quyền `Thủ quỹ duyệt phiếu thu`)
· `BillIncomeController:213` khi phiếu thu được duyệt + hạch toán → **4 Đã hạch toán** (kèm `saveAccountsDetail()`).

Đã bổ sung: BE `BillIncomeRequest::canCreateBillIncome()` (port nguyên vẹn ERP :453; `canReject()` gọi lại
hàm này vì ERP gate chung 1 điều kiện) + cờ `is_can_create_bill_income` trong **CẢ 2 Resource**
(`DetailResource` cho footer màn xem, `ListResource` cho nút trên dòng ở màn danh sách).

FE dựng nút **"Tạo phiếu thu"** ở **2 chỗ**: footer màn xem và hàng hành động của màn danh sách
(`getRowActions`, icon `ri-file-add-line`), hiện đúng theo cờ quyền; bấm vào hiện toast
*"Chức năng "Tạo phiếu thu" đang chờ chuyển màn Phiếu thu sang HRM"*.

⚠️ **Lần đầu làm bằng `:interactable="false"` là SAI** — user báo "không thấy nút". Đo ra: nút disabled
có màu chữ `#94a3b8` trên nền `#f1f5f9` (xám trên xám) nên chìm hẳn giữa các nút màu khác.
Đã đổi sang **nút bình thường + toast khi bấm**: nền `rgb(26,188,156)`, chữ trắng, `cursor: pointer`.
📌 Bài học: muốn "dựng sẵn chức năng chưa làm" thì để nút SÁNG BÌNH THƯỜNG và báo khi bấm, đừng disable —
nút disabled trong theme này gần như vô hình.

**Khi port xong màn Phiếu thu**: đổi `notifyBillIncomePending()` thành điều hướng
`/finance/bill-incomes/create?bill_income_request_id={id}` ở 2 chỗ (form + index) — không phải sửa gì thêm ở BE.

Verify: màn danh sách, dòng `TPE.DNTT0826.00001` (Chờ KT duyệt) có 3 nút *Xem chi tiết · **Tạo phiếu thu** · In phiếu*;
màn chi tiết có 4 nút *Tạo phiếu thu · In phiếu · Không duyệt · Quay lại*.

📌 Ghi nhận không sửa: `components/modals/ChooseErpCustomerModal.vue` có cảnh báo Vue
*"The computed property 'fields' is already defined in data"* — lỗi CÓ SẴN của component dùng chung,
hiện ở mọi màn nhúng nó, không phải do màn này. Không tự sửa (file dùng chung).

Đang làm dở: không có.
Bước tiếp theo: user test trình duyệt; sau đó chốt 2 việc CÒN NỢ ở Task 7.1/7.3 (đối chiếu trực tiếp
trên giao diện ERP + 4 tài khoản đủ 4 cấp quyền) và quyết định về nợ kỹ thuật gộp trait quyền.
Blocked: không.

### Checkpoint — 2026-08-14 (hết Phase 3 — BE XONG TOÀN BỘ)
Vừa hoàn thành: **Phase 3 (Task 3.1 + 3.2)** — 3 endpoint popup. **Toàn bộ backend của màn đã xong.**
Files sửa: `BillIncomeRequestService` (`searchSellContracts` · `searchBuyContracts` · `paginateContractUnion`
· `searchSuppliers` + hằng `HRM_CONTRACT_SELECTABLE_STATUSES`) · `BillIncomeRequestController`
(3 action + `paginatedResponse`) · `Routes/api.php` (3 route tĩnh, đặt TRƯỚC `/{id}`).
Đang làm dở: không có — bằng chứng verify ghi ở "Checkpoint Phase 3".
Bước tiếp theo: **Phase 4 — FE danh sách + màn chờ duyệt + menu** (Task 4.1, 4.2).
⚠️ Trước khi code FE: đọc code HIỆN TẠI của màn mẫu `pages/assign/customers/index.vue` +
`CustomerForm.vue` (đã đổi base theo `form-validate-base`, xem Ràng buộc toàn cục) — KHÔNG bám snapshot trong spec.
Blocked: không.

### Checkpoint — 2026-08-14 (hết Phase 2)
Vừa hoàn thành: **Phase 2 trọn vẹn (Task 2.1 → 2.4)** + **seeder dữ liệu test** (user chốt).
Files mới: 3 FormRequest (`Store`/`Update`/`ChangeStatus`) · `BillIncomeRequestTestDataSeeder`.
Files sửa: `BillIncomeRequestService` (store/update/syncDetails/destroy/changeStatus/notifyAccountants/buildNotificationContent) ·
`BillIncomeRequestController` (4 action + savedMessage) · `Routes/api.php` (4 route ghi) ·
`BillIncomeRequest` (allowedObjectTypes) · trait `ChecksEmployeePermission` (employeeInfoIdsHavingPermission).
Đang làm dở: không có — bằng chứng verify ghi ở "Checkpoint Phase 2".
Bước tiếp theo: **Phase 3 — BE phụ trợ** (Task 3.1 `search-contracts` UNION 3 nguồn → 3.2 `search-buy-contracts` + `search-suppliers`).
Blocked: không. Dữ liệu test đã sẵn (8 hợp đồng HRM, 6 cái đúng tập trạng thái popup + 2 cái phải bị loại).
Còn 1 việc chờ user chốt (không chặn): có gộp 3 method quyền của `ProductTransferRequest` sang trait chung không.

### Checkpoint — 2026-08-14 (hết Phase 1)
Vừa hoàn thành: **Phase 1 trọn vẹn (Task 1.1 → 1.7)** — 15 file mới + 3 file sửa ở `hrm-api`, verify bằng HTTP thật.
Files mới: 8 entity hợp đồng read-only + `Supplier` + `AccountDetail` · `BillIncomeRequest` + `BillIncomeRequestDetail` ·
trait `ChecksEmployeePermission` · `BillIncomeDebtService` + `BillIncomeRequestService` ·
`BillIncomeRequestListResource` + `BillIncomeRequestDetailResource` · `BillIncomeRequestController`.
Files sửa: `FinanceServiceProvider` (morphMap 8 loại) · `Modules/Finance/Routes/api.php` (3 route) ·
`PermissionsTableSeeder` (5 quyền id 1148-1152, đã INSERT vào DB dev).
Đang làm dở: không có — Phase 1 đóng, bằng chứng verify ghi ở "Checkpoint Phase 1" phía trên.
Bước tiếp theo: **Phase 2 — BE ghi** (Task 2.1 3 FormRequest → 2.2 store/update/syncDetails →
2.3 destroy/changeStatus → 2.4 thông báo khi gửi duyệt).
Blocked: không. 2 việc **cần user chốt** trước/trong Phase 2:
1. Có gộp 3 method quyền của `ProductTransferRequest` sang trait `ChecksEmployeePermission` không (sửa code đang chạy)?
2. `hrm_contracts` đang 0 dòng — Phase 2/3 test tạo phiếu bằng hợp đồng nào?

### Checkpoint — 2026-08-13 (tạm dừng, mai làm tiếp)
Vừa hoàn thành: Phase 0 — brainstorming (10 quyết định đã chốt với user), spec đầy đủ (user đã duyệt),
plan chi tiết 7 phase / 20 task (file này).
Đang làm dở: **chưa viết một dòng code nào** ở cả 2 repo. Chưa đụng git.
Bước tiếp theo: Task 1.1 — tạo 9 entity hợp đồng read-only trong `Modules/Finance/Entities/Contract/`
(bước đầu tiên là chạy `SHOW TABLES LIKE '%contract%'` + đọc `$table` của 8 model ERP, không đoán tên bảng).
Blocked: không. **Chờ user chọn cách chạy**: subagent-driven (khuyến nghị) hay inline.

2 mặc định đã chốt khi user duyệt spec, ghi lại kẻo quên:
- Popup hợp đồng HRM chỉ lấy `status ∈ {6, 8, 9, 10, 11, 12}` (Có hiệu lực trở lên).
- Màn chờ duyệt đợt này chỉ có nút **Không duyệt**, không có nút Duyệt riêng.


### Checkpoint — 2026-08-22 (đợt sửa theo phản hồi user)
Vừa hoàn thành: **Task 8.8 → 8.11** (4 việc, nhánh `gop_db`, chưa commit).
· 8.8 — cột **Người nộp** (`payer`) + đổi tiêu đề cột `reason` thành **"Lý do nộp"** (bám ERP
  `approved.blade.php:50-51`) + ô lọc **Người nộp** (LIKE, dùng binding). 2 file BE, 1 file FE.
· 8.9 — bảng chi tiết form thêm dòng **Tổng cộng** (3 computed + 1 dòng `<tbody>` + style),
  số ô khớp header ở cả 4 tổ hợp `isVnd` × `readonly`.
· 8.10 — mở 2 tab cùng 1 phiếu: tách `isEditableStatus()` khỏi `canEdit()`; `update()`/`destroy()`/
  `changeStatus()` trả **409** + câu "Dữ liệu đã được thay đổi..." thay cho 403/422 khi phiếu vừa bị
  người khác chuyển trạng thái; vẫn 403 khi thật sự thiếu quyền.
· 8.11 — bỏ nút **Xem chi tiết** ở danh sách (cột Mã phiếu đã là link).
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt xác nhận 4 việc trên** (ô checkbox cuối mỗi task).
Blocked: không.

---

## Phase 9 — Lịch sử thay đổi (skill `entity-history`) — 2026-08-22

Yêu cầu user: màn **Đề nghị thu tiền** thêm chức năng **Xem lịch sử thay đổi**, "làm theo quy tắc
chung, mẫu màn danh sách khách hàng".

**2 quyết định đã chốt với user (skill §0):**
1. Bảng chi tiết phiếu log theo kiểu **diff từng dòng** (`__key`, in `~` sửa / `-` bỏ / `+` thêm)
   — đúng chuẩn màn Khách hàng, KHÔNG dùng tóm tắt 1 dòng như `bill_adjust_dept_requests`.
   ⇒ phải **mở rộng service dùng chung `CatalogHistoryService`** (thuần thêm).
2. **Không gắn permission riêng** — ai vào được màn thì xem được lịch sử (mặc định của skill).

**Hạ tầng dùng lại (không viết mới):** bảng chung `catalog_histories` · trait `LogsCatalogHistory`
· endpoint chung `GET /api/v1/catalog-histories/{table}/{id}` (+ `/filter-options`) ·
FE `CatalogHistoryModal.vue` + `SystemInfoSection.vue`. Tiền lệ cùng module:
`bill_adjust_dept_requests`.

### BE

- [x] **9.1** `app/Services/CatalogHistoryService.php` — hỗ trợ **khoá dạng BẢNG** (thuần thêm,
      không đổi hành vi 20+ màn đang dùng):
      · `logUpdate()`: giá trị là mảng bản ghi (`[['__key'=>…, 'Nhãn'=>'giá trị', …], …]`) thì so
        bằng JSON chuẩn hoá và lưu nguyên mảng dưới `['__rows' => …]`, KHÔNG đi qua `normalize()`
        (normalize json_encode cả mảng → log ra 1 chuỗi JSON dài).
      · `changesOf()`: nhận diện `__rows` (và mảng bản ghi thô của log `delete`) → dựng
        `removed` / `added` / `changed[].fields` đúng DTO §4; bản ghi bị sửa **chỉ liệt kê cột đã
        đổi**; đổi thứ tự dòng (không đổi nội dung) thì bỏ qua, không sinh log rác.
      · Ghép cặp bản ghi bằng `__key`; trùng khoá thì tự tách. Tên bản ghi trên dòng `~` lấy
        `__name`.
- [x] **9.2** `CatalogHistoryService::TABLES` — khai `bill_income_requests` + nhãn tiếng Việt:
      Loại thu · Lý do thu · Người nộp tiền · Tiền tệ · Tỷ giá · Ghi chú · Trạng thái ·
      Bảng chi tiết (khoá ảo `details_rows`).
- [x] **9.3** `BillIncomeRequestService` — `use LogsCatalogHistory` + `catalogTable()` /
      `catalogColumns()` / `catalogDisplay()` (id → chữ: Loại thu, Trạng thái, Tiền tệ; tỷ giá +
      tiền format số) + `detailRows()` dựng bản ghi từng dòng chi tiết
      (`__key` = customer|supplier|objectable_type|objectable_id vì `syncDetails()` xoá-tạo lại
      nên id dòng KHÔNG bền).
      Gắn log vào: `store()` → `create` · `update()` → `update` (snapshot TRƯỚC khi fill, log SAU
      transaction) · `destroy()` → `delete` · `changeStatus()` → `change_status` **kèm lý do không
      duyệt vào `note` của log** (skill §4.1).
- [x] **9.4** 3 chỗ ĐỔI TRẠNG THÁI PHIẾU TỪ MÀN KHÁC cũng phải ghi log, nếu không timeline đứt
      quãng ở "Chờ KT duyệt":
      · `BillIncomeWriteService::markRequestCreatedAndNotify()` → **Đã tạo phiếu thu**
      · `BillIncomeApprovalService::approve()` → **Đã hạch toán**
      · `BillIncomeApprovalService::cancel()` → **Hủy** (kèm lý do hủy vào `note` của log)
      Chỉ ghi khi trạng thái THỰC SỰ đổi (3 chỗ này dùng `update()` query builder, gọi lại nhiều
      lần được).
      Ngoài phạm vi: `syncIncomeMoneyReal()` ghi **số thực thu** ngược về dòng chi tiết — đó là số
      của phiếu thu, không phải người dùng sửa phiếu đề nghị ⇒ KHÔNG track.

### FE

- [x] **9.5** `pages/finance/bill-income-requests/index.vue` — thêm hành động **Lịch sử**
      (`ri-history-line`, không gắn quyền) vào menu ⋮ từng dòng + nhúng
      `<CatalogHistoryModal ref="historyModal" modal-id="history-bill-income-request"
      record-prefix="Phiếu" />`, mở bằng `open('bill_income_requests', item.id, item.code)`.
      Màn **chờ duyệt** (`pending.vue`) dùng lại chính file này nên tự có.
- [x] **9.6** `pages/finance/bill-income-requests/_id/index.vue` — khối **Lịch sử** trong THÂN
      TRANG (không phải nút ở footer, skill §5.1): `<SystemInfoSection
      entity-type="bill_income_requests" :entity-id="…" endpoint-base="catalog-histories" />`.

### Verify

- [x] **9.7** `php -l` toàn bộ file sửa · tinker: sửa 1 trường → 1 log đúng subset · không đổi gì →
      không log · thêm 1 dòng chi tiết → đúng 1 dòng `+` · sửa số tiền 1 dòng → đúng 1 dòng `~` chỉ
      cột đó · đổi trạng thái → log riêng kèm lý do · thứ tự mới → cũ · **log của 20+ màn danh mục
      cũ đọc ra không đổi** (chống hồi quy khi mở rộng service chung).
- [x] **9.8** FE: compile template 2 file sửa. Không tự test Playwright — user tự mở trình duyệt.

### Checkpoint — 2026-08-22 (Phase 9 — Lịch sử thay đổi)
Vừa hoàn thành: **Task 9.1 → 9.8** (nhánh `gop_db`, chưa commit).
Files sửa BE (4): `app/Services/CatalogHistoryService.php` (whitelist `bill_income_requests` +
hỗ trợ **khoá dạng BẢNG**: `isRowList` / `rowsOf` / `rowsFingerprint` / `rowListChange` / `indexRows`
/ `rowText` / `rowName`, cắm vào `logUpdate()` + `changesOf()`) ·
`Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php` (`statusName()` +
`logStatusHistory()`) · `Modules/Finance/Services/BillIncomeRequestService.php` (trait
`LogsCatalogHistory` + `catalogTable/catalogColumns/catalogDisplay/detailRows` + log ở
store/update/destroy/changeStatus) · `BillIncomeWriteService.php` + `BillIncomeApprovalService.php`
(3 chỗ đổi trạng thái từ màn Phiếu thu).
Files sửa FE (3): `bill-income-requests/index.vue` (hành động **Lịch sử** + `CatalogHistoryModal`) ·
`_id/index.vue` (khối `SystemInfoSection` qua slot mới) · `components/BillIncomeRequestForm.vue`
(thêm slot `after-content` TRƯỚC `V2Footer` — đặt khối Lịch sử sau footer thì bị thanh nút
`position: fixed` đè và hở 66px spacer).

Bằng chứng verify (tinker, dữ liệu test đã dọn sạch — `catalog_histories` của
`bill_income_requests` về lại 0 dòng):
- Sửa 1 ô số tiền + thêm 1 dòng + bỏ 1 dòng → đúng `~` (chỉ cột đã đổi) / `+` / `-`.
- Không đổi gì → không ghi · chỉ đổi THỨ TỰ dòng → không ghi · `"1"` vs `1` → không ghi log rác.
- Đổi 2 trường phẳng → 1 dòng log 2 key. Xoá hết dòng chi tiết → 2 dòng `-`.
- End-to-end `update()` trên phiếu thật (chạy trong transaction rồi **rollback**): 1 dòng log gộp
  "Người nộp tiền" + "Bảng chi tiết ~ 1 dòng", `changed_by` + phòng ban resolve đúng.
- `changeStatus()` (Không duyệt) và 3 chỗ đổi trạng thái từ màn Phiếu thu → 4 dòng
  "Thay đổi trạng thái", **lý do không duyệt / lý do hủy hiện ở khối ghi chú**; trạng thái không
  đổi → không ghi.
- Chống hồi quy: log cột phẳng + mảng chuỗi thường của màn danh mục (`works`) đọc ra y như cũ,
  không rẽ nhầm sang nhánh khoá bảng; log cũ `bill_adjust_dept_requests` đọc bình thường.
- `filter-options`: đúng 3 nhóm cố định + 783 người thực hiện (không suy từ log).
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt xác nhận** popup Lịch sử ngoài danh sách + khối Lịch sử ở màn
chi tiết (chưa tự test Playwright — theo thoả thuận).
Blocked: không.

### Bổ sung Phase 9 — 2026-08-22 (rà theo khi làm màn Đề nghị thanh toán)
Làm lịch sử cho màn Đề nghị thanh toán thì lộ ra 1 bẫy chung, đã sửa luôn ở màn này:
- `store()`: chuyển việc gán khoá ảo `details_rows` + `logCatalogCreate()` **ra NGOÀI**
  `DB::transaction()`. Khoá ảo không có cột trong bảng — gán xong mà model còn `save()` nữa là
  `SQLSTATE[42S22] Unknown column ... in field list`. Gán sau lần save cuối cùng là an toàn tuyệt
  đối, không phụ thuộc vào việc hàm gửi thông báo có save model hay không.
- `detailRows()`: tên bản ghi ghép bằng `array_filter` thay vì nối chuỗi — dòng không có đối tượng
  trước đó ra tên bắt đầu bằng `" / "`.
Đã verify lại `store()` + `destroy()` end-to-end (transaction rồi rollback): mỗi thao tác đúng 1
dòng log `create` / `delete`.

### Phase 10 — Fix: popup chọn KH tìm theo SĐT ra dòng có cột SĐT trống (2026-08-24) @khoipv
Bug user báo: ở màn Đề nghị thu tiền, popup "Chọn khách hàng" gõ SĐT `0241` → ra danh sách
công ty nhưng **cột SĐT trống trơn (`—`)**, trông như "ra cả KH không có SĐT đó".

Điều tra (không phải lỗi lọc):
- FE `ChooseErpCustomerModal.vue:285` gửi đúng `mobile=0241`; `buildQueryString` không nuốt param.
- BE `CustomerService.php:140-142` áp đúng `where customers.mobile like '%0241%'`; các nhánh
  `orWhere` phân quyền đều bọc trong `where(function(){})` nên không thoát bộ lọc.
- Chạy lại nguyên câu query của popup qua tinker: `COUNT = 6`, **cả 6 dòng đều có SĐT chứa 0241**.
- Thủ phạm: `CustomerListResource.php:36` trả `mobile = null` cho MỌI KH không phải "của mình",
  không phân biệt loại KH.

Rule đúng (đã ghi ở 2 chỗ khác trong chính codebase): mask CHỈ áp cho **KH CÁ NHÂN**
- `CustomerService::applyB2cOwnershipVisibility` docblock: "KH tổ chức (type 2-5) không bị lớp
  này giới hạn (rule B2B nằm ở người liên hệ)"
- `CustomerExportFormatter::taxCodeOrMobile`: chỉ che khi `customer_type === 1`

- [x] BE: `CustomerListResource` — chỉ che `mobile` khi KH CÁ NHÂN và không phải KH của mình
- [x] BE: KH cá nhân — bỏ che khi user tìm KHỚP ĐÚNG full SĐT (escape hatch sẵn có ở
      `applyVisibilityScope` / `applyB2cOwnershipVisibility`; số user tự gõ ra thì che vô nghĩa)
- [x] Verify: chạy lại query popup + resource, đối chiếu SĐT thật trong DB

### Checkpoint — 2026-08-24
Vừa hoàn thành: fix mask SĐT ở `CustomerListResource` (thêm `shouldMaskMobile()` +
`matchesExactSearchedPhone()`), chỉ sửa BE — FE không đụng gì.
Bằng chứng verify (tinker, auth employee 13, chạy nguyên luồng service + resource):
- Tìm `0241` ở popup: 6 KH tổ chức hiện ĐÚNG SĐT thật trong DB (02413714430, 02413863038,
  02413865996, 02413867677, 02413883889, 02412345699); 1 KH cá nhân của người khác vẫn che `null`.
- KH cá nhân gõ KHỚP ĐÚNG full `0902416240` → hiện số; gõ mảnh `090241` → vẫn che.
- Không đổi bộ lọc: `where mobile like '%0241%'` giữ nguyên, số dòng trả về không đổi.
Ảnh hưởng kèm theo (có chủ ý): màn danh sách `/assign/customers` và các popup chọn KH khác
(AddCustomer, AddCustomerModal, AddRelatedUnitModal, QuickAddCustomerModal) nay cũng hiện SĐT của
KH TỔ CHỨC — đồng bộ với bản xuất Excel vốn chưa từng che nhóm này.
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt** popup Chọn khách hàng ở màn Đề nghị thu tiền, tìm `0241`
xác nhận cột SĐT đã có số (chưa tự test Playwright — theo thoả thuận).
Blocked: không.

### Phase 10b — Fix tiếp: ô SĐT khớp GIỮA chuỗi (2026-08-24) @khoipv
User báo tiếp: sau khi bỏ mask vẫn thấy `79TKHPNH-30 - ANH THẠCH` trong kết quả tìm `0241`.
SĐT thật của KH này là `0902417023` — chứa `0241` ở GIỮA (090**2417**023), lại là KH cá nhân của
người khác nên cột SĐT bị che `—` → vừa lạc đề vừa không thấy số để đối chiếu.

Nguyên nhân: `CustomerService.php:140` dùng `mobile LIKE '%0241%'`. Trong DB có 19 KH khớp kiểu
này thì **11 KH không hề có số bắt đầu bằng 0241** (0902416240, 0942802412, 0375002417...).

- [x] BE: ô SĐT riêng (`mobile`) đổi sang khớp từ ĐẦU SỐ —
      `CONCAT(',', REPLACE(mobile,' ',''), ',') LIKE '%,<kw>%'` (bọc dấu phẩy để KH cá nhân có
      nhiều số ghép chuỗi vẫn khớp đúng từng số)
- [x] Verify: tìm `0241` → 6 dòng, không còn 79TKHPNH-30; tìm đủ `0902417023` → ra đúng KH đó

Phạm vi ảnh hưởng: chỉ `ChooseErpCustomerModal` gửi tham số `mobile` (grep toàn hrm-client) →
không đụng bộ lọc màn danh sách KH. Ô "MST/SĐT" gộp của màn danh sách (`tax_code`) GIỮ NGUYÊN
khớp giữa chuỗi vì còn dùng để tra mã số thuế.

⚠️ Đánh đổi: tìm theo ĐUÔI số (gõ `7023`) nay không ra kết quả. Nếu user cần thì mở lại thành
"khớp đầu số HOẶC đuôi số" — chưa làm vì chưa có yêu cầu.

### Checkpoint — 2026-08-24 (lần 2)
Vừa hoàn thành: Phase 10 (bỏ mask SĐT KH tổ chức) + Phase 10b (ô SĐT khớp từ đầu số).
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt** popup Chọn khách hàng ở màn Đề nghị thu tiền, tìm `0241`
xác nhận ra đúng 6 công ty kèm SĐT, không còn ANH THẠCH.
Blocked: không.

### Phase 10c — Đổi tiêu đề cột "Lý do nộp" -> "Lý do thu" (2026-08-24) @khoipv
- [x] FE: `pages/finance/bill-income-requests/index.vue:480` — `title: 'Lý do nộp'` -> `'Lý do thu'`
      (áp cho CẢ màn chờ duyệt vì `pending.vue` render lại chính `index.vue` qua prop `pendingMode`)

Ghi chú: ERP đặt 2 tên cho cùng 1 trường — "Lý do nộp" ở `index.blade.php:49` /
`approved.blade.php:50`, "Lý do thu" ở form + màn In. Nay thống nhất theo "Lý do thu".
Chỉ đổi NHÃN hiển thị, `key: 'reason'` giữ nguyên nên không đụng API/sort/cấu hình cột.
Grep toàn hrm-client + hrm-api: không còn chỗ nào khác dùng chuỗi "Lý do nộp".

### Phase 10d — Bỏ cột "Người nộp" khỏi màn danh sách (2026-08-24) @khoipv
- [x] FE: gỡ `{ key: 'payer', title: 'Người nộp', ... }` khỏi `allColumns()`
      (`pages/finance/bill-income-requests/index.vue`)
- [x] FE: gỡ luôn `<template #cell-payer>` — slot mồ côi không render nhưng để lại thì lần sau
      bật cột lại sẽ tưởng đã có sẵn định dạng

GIỮ NGUYÊN (không nằm trong yêu cầu):
- Ô lọc "Người nộp" ở tìm kiếm nâng cao (`filter.payer`) — vẫn lọc được dù cột không hiện.
- BE vẫn trả trường `payer`; form nhập, màn chi tiết và bản in không đổi.

Cấu hình cột đã lưu: KHÔNG cần migration. `columnCustomizationMixin.mergedColumns()` (dòng 51)
lọc `savedCol` không còn trong `allColumns` -> user nào từng lưu cấu hình có cột này thì cột tự
biến mất, không lỗi. Màn "Chờ duyệt" dùng chung `columnScreenKey: finance_bill_income_requests`
nên cũng mất cột theo, đúng chủ đích (2 màn cùng bộ cột).

### Checkpoint — 2026-08-24 (wrap up đợt 4)
Vừa hoàn thành: 4 việc trong 1 phiên, đều ở màn **Đề nghị thu tiền** (nhánh `gop_db`, CHƯA commit).
1. Phase 10 — BE `CustomerListResource`: bỏ che SĐT của KH TỔ CHỨC (mask ownership vốn chỉ dành cho
   lead CÁ NHÂN); KH cá nhân bỏ che thêm khi user gõ KHỚP ĐÚNG full SĐT.
2. Phase 10b — BE `CustomerService`: ô SĐT của popup chọn KH đổi từ `LIKE '%kw%'` sang khớp từ
   ĐẦU SỐ `CONCAT(',', REPLACE(mobile,' '), ',') LIKE '%,kw%'`.
3. Phase 10c — FE `index.vue`: đổi tiêu đề cột `Lý do nộp` → `Lý do thu`.
4. Phase 10d — FE `index.vue`: bỏ cột `Người nộp` (+ slot `#cell-payer`).

File đụng: BE 2 (`Modules/Assign/Transformers/CustomerResource/CustomerListResource.php`,
`Modules/Assign/Services/CustomerService.php`) · FE 1
(`pages/finance/bill-income-requests/index.vue`).

Verify đã chạy: `php -l` sạch 2 file BE; tinker chạy nguyên luồng service + resource với auth thật:
tìm `0241` → 6 KH tổ chức kèm SĐT đúng như DB, không còn `79TKHPNH-30` (0902417023, khớp giữa
chuỗi); gõ đủ `0902417023` → ra đúng KH đó kèm số; gõ mảnh `090241` → KH cá nhân vẫn bị che.
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt nghiệm thu** 3 điểm — (a) popup chọn KH tìm `0241`,
(b) tiêu đề cột "Lý do thu", (c) cột "Người nộp" đã biến mất ở CẢ màn danh sách và màn chờ duyệt.
Đạt thì mới commit (chưa commit theo quy tắc project).
Blocked: không.

📌 Còn treo (chưa làm vì ngoài yêu cầu, chờ user quyết):
- Ô lọc "Người nộp" ở tìm kiếm nâng cao — vẫn giữ, có bỏ nốt không?
- Tìm SĐT theo ĐUÔI số (gõ `7023`) nay không ra kết quả — có cần mở thành "khớp đầu HOẶC đuôi"?

---

## Phase 11 — Popup chọn KH: ẩn luôn dòng bị che SĐT khi tìm theo SĐT (2026-08-25)

**User báo:** ở popup "Chọn khách hàng" (màn Đề nghị thu tiền), gõ `024` vào ô Số điện thoại
vẫn ra khách hàng KHÔNG có SĐT (cột SĐT hiện `—`) → tưởng hệ thống lọc sai.

**Root cause — 2 tầng dùng 2 luật khác nhau cho cùng 1 ô nhập:**

| Tầng | Luật với từ khoá `024` | Kết quả |
| --- | --- | --- |
| WHERE lọc danh sách (`CustomerService`, Phase 10b) | `LIKE ',024%'` — khớp ĐẦU SỐ | KH cá nhân **lọt vào** danh sách |
| Mask SĐT khi trả về (`CustomerListResource`, Phase 10) | `=== '024'` — khớp KHÍT | SĐT bị **che** → FE hiện `—` |

Kiểm chứng trên DB `gop_db`: dòng user khoanh đỏ là `29TPHPTA-263` (id 41706, `customer_type=1`)
**CÓ** `mobile = 02433660388` — bắt đầu bằng `024` nên lọt bộ lọc hợp lệ, chỉ là bị che số.
Tức cả 2 tầng đều chạy đúng ý đồ riêng, mâu thuẫn nằm ở chỗ 2 ý đồ không khớp nhau.

**Quyết định của user (2026-08-25):** khách nào bị che SĐT thì KHÔNG hiện ra nữa. Phạm vi:
- **Chỉ khi đang tìm theo SĐT** — không gõ gì thì danh sách giữ nguyên như cũ (không siết);
- **Chỉ ở popup chọn khách hàng** — màn danh sách KH `/assign/customers` không đổi.

### BE
- [x] `Modules/Assign/Services/CustomerService.php` — thêm `applyHideMaskedMobile($query, $request)`,
      gọi ngay sau `applyB2cOwnershipVisibility()`. Điều kiện dựng **trùng khít 3 vế** của
      `CustomerListResource::shouldMaskMobile()` — lệch 1 vế là ẩn nhầm dòng lẽ ra chọn được:
      1. KH TỔ CHỨC (`customer_type != 1`) → không bao giờ bị che, luôn giữ;
      2. KH cá nhân **của mình** (`created_by = myErpId` HOẶC id ∈ `myVisibleCustomerIds()`) → giữ;
      3. Gõ **khớp khít** trọn 1 số (`LIKE '%,kw,%'`) → escape hatch cũ, giữ.
- [x] Chỉ chạy khi có cờ `hide_masked_mobile` **VÀ** `mobile`/`tax_code` thực sự có giá trị
      (bỏ qua `''`, `'null'`, `'undefined'` — `AddCustomer.vue` gửi chuỗi rỗng khi user không gõ).

### FE — chỉ 2 popup CÓ ô tìm SĐT
- [x] `components/modals/ChooseErpCustomerModal.vue` — thêm `hide_masked_mobile: 1` vào params
      (đây là popup ở màn Đề nghị thu tiền user báo lỗi).
- [x] `components/modals/AddCustomer.vue` — thêm `&hide_masked_mobile=1` vào query string.
- [x] KHÔNG đụng `AddCustomerModal.vue` và `AddRelatedUnitModal.vue` — 2 popup này chỉ có ô
      `keyword`, không có ô SĐT nên cờ vô nghĩa.

### Verify đã chạy
`php -l` sạch; FE compile sạch bằng `vue-template-compiler` + babel parse (không dùng eslint —
hrm-client không có ESLint config chạy được trên Node 14).
Chạy hàm thật trên DB `gop_db` qua tinker, 4 kịch bản:

| Kịch bản | Trước | Sau |
| --- | --- | --- |
| Gõ `024` | 285 dòng (34 KH cá nhân cột SĐT trống) | **251 dòng, 0 dòng bị che** |
| Gõ khít `02433660388` | — | **1 dòng, KH cá nhân vẫn ra** (escape hatch nguyên vẹn) |
| Có cờ nhưng KHÔNG gõ SĐT | 43.078 | **43.078 — không siết gì** |
| KH cá nhân do chính mình tạo (erp_id 61), gõ `024` | — | **253 dòng, KH 41706 VẪN hiện** |

### Checkpoint — 2026-08-25
Vừa hoàn thành: Phase 11 — popup chọn KH ẩn dòng bị che SĐT khi tìm theo SĐT (nhánh `gop_db`,
CHƯA commit). File đụng: BE 1 (`Modules/Assign/Services/CustomerService.php`) · FE 2
(`components/modals/ChooseErpCustomerModal.vue`, `components/modals/AddCustomer.vue`).
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt nghiệm thu** — mở popup chọn KH ở màn Đề nghị thu tiền,
gõ `024` vào ô Số điện thoại → không còn dòng nào cột SĐT trống `—`; gõ đủ `02433660388` →
KH cá nhân đó vẫn ra kèm số. Đạt thì mới commit (chưa commit theo quy tắc project).
Blocked: không.

⚠️ Đánh đổi đã biết (user chốt, ghi lại để sau khỏi tưởng bug): luật này ẩn **cả KH cá nhân vốn
chọn được** (đã lọt lớp quyền vì từng phát sinh báo giá/meeting/dự án TKT). Nếu có người báo
"tìm SĐT không thấy khách X mà trước thấy" → nguyên nhân ở đây, cách ra là gõ ĐỦ cả số điện thoại.

📌 Còn treo (từ đợt 4, chưa làm — chờ user quyết):
- Ô lọc "Người nộp" ở tìm kiếm nâng cao — vẫn giữ, có bỏ nốt không?
- Tìm SĐT theo ĐUÔI số (gõ `7023`) nay không ra kết quả — có cần mở thành "khớp đầu HOẶC đuôi"?

---

## Phase 12 — Popup chọn KH: ô MST và ô SĐT phải lọc ĐỘC LẬP (2026-08-25)

**User báo:** gõ `0` vào CẢ 2 ô "Mã số thuế" và "Số điện thoại" → ra 10.984 KH mà cột SĐT trống `—`.

**Root cause — KHÁC hẳn Phase 11, không phải lỗi che SĐT:** các dòng đó là KH **TỔ CHỨC**
(`customer_type` 2, 3) mà tổ chức thì không bao giờ bị mask. Tra DB: `15TPHPTA`, `67TANDKH-73`,
`20TTHPPH-240` đều có `mobile = NULL` **thật** — khách thực sự không có SĐT.

Lỗi nằm ở `elseif` trong `CustomerService::index()`:

```php
if ($request->filled('tax_code')) { ... }        // ô GỘP "MST/SĐT" của màn danh sách KH
elseif ($request->filled('mobile')) { ... }      // ← chỉ chạy khi KHÔNG gõ MST
```

Gõ cả 2 ô → nhánh `tax_code` chạy, **ô SĐT bị bỏ qua hoàn toàn**. 10.984 dòng đó thực chất là
"mọi KH có chữ số `0` trong MST **hoặc** trong SĐT", không liên quan gì tới ô Số điện thoại.

Gốc sâu hơn: `tax_code` phục vụ **2 ngữ nghĩa đối nghịch** trên cùng 1 tham số —
- màn danh sách KH: ô **GỘP** label "MST/SĐT" (`index.vue:553`), cố ý tìm lan sang `mobile`;
- popup chọn KH: ô **RIÊNG** label "Mã số thuế", bên cạnh đã có ô SĐT riêng.

### Quyết định user (2026-08-25)
- Gõ cả 2 ô → áp **CẢ 2 điều kiện (AND)**;
- Ô MST khớp từ **ĐẦU mã** (đồng bộ ô SĐT đã sửa Phase 10b), thay vì khớp giữa chuỗi.

### BE
- [x] `CustomerService::index()` — thêm nhánh cờ `tax_code_only` ĐỨNG TRƯỚC nhánh gộp:
      `tax_code LIKE 'kw%'` (đầu mã) và `mobile LIKE ',kw%'` áp **song song, không `elseif`**.
      Nhánh gộp cũ giữ NGUYÊN cho màn danh sách KH (đã verify SQL còn `or mobile like ?`).
- [x] `CustomerService::applyHideMaskedMobile()` — khi có `tax_code_only` thì CHỈ đọc ô `mobile`
      làm từ khoá SĐT (ô MST giờ là MST thuần, dùng làm escape hatch SĐT là sai).
- [x] `CustomerService::index()` `$b2cExactPhone` — cùng lý do, bỏ `tax_code` khi có cờ.
- [x] `CustomerListResource::matchesExactSearchedPhone()` — đồng bộ nốt, tránh mở khoá mask nhầm.

### FE — 2 popup có ô MST riêng
- [x] `ChooseErpCustomerModal.vue` — thêm `tax_code_only: 1`.
- [x] `AddCustomer.vue` — thêm `&tax_code_only=1`.

### Verify đã chạy
`php -l` sạch 2 file BE · FE compile sạch (vue-template-compiler + babel).
Chạy **nguyên luồng `index()` + `CustomerListResource`** với auth thật (`TpEmployee` id 61):

| Kịch bản | Kết quả |
| --- | --- |
| POPUP — MST=`0` + SĐT=`0` (ca user báo) | **614 dòng**, trang 1 **0/10 dòng trống SĐT** |
| POPUP — chỉ SĐT=`024` (ca Phase 11) | 176 dòng, 0/10 trống SĐT — không hồi quy |
| POPUP — chỉ MST đầy đủ `0101234567` | 1 dòng |
| POPUP — không gõ gì | 11.263 dòng — không siết |
| SQL nhánh popup | 2 điều kiện nối **`and`**, binding `0101%` + `%,024%` — đúng AND + đầu mã/đầu số |
| Hồi quy màn danh sách (KHÔNG cờ) | SQL vẫn `(tax_code like ? or mobile like ?)` — ô gộp NGUYÊN VẸN |

### Checkpoint — 2026-08-25 (2)
Vừa hoàn thành: Phase 12 — tách ngữ nghĩa ô MST giữa popup và màn danh sách (nhánh `gop_db`,
CHƯA commit). File đụng: BE 2 (`CustomerService.php`, `CustomerListResource.php`) · FE 2
(`ChooseErpCustomerModal.vue`, `AddCustomer.vue`).
Đang làm dở: không có.
Bước tiếp theo: **user mở trình duyệt nghiệm thu** — popup chọn KH, gõ `0` vào cả ô MST và ô SĐT
→ không còn dòng nào cột SĐT trống; gõ riêng từng ô vẫn lọc đúng. Đạt thì mới commit.
Blocked: không.

⚠️ Ghi để sau khỏi tưởng bug: ô MST giờ khớp **đầu mã** ở popup. Ai quen gõ mảnh GIỮA mã số thuế
để tìm sẽ thấy "không ra kết quả" — đó là chủ đích (user chốt), gõ từ đầu mã.

---

## Phase 13 — Bỏ hẳn "Người nộp" khỏi màn Đề nghị thu tiền (2026-08-25) @khoipv

Chốt nốt câu hỏi treo từ Phase 10d ("ô lọc Người nộp có bỏ nốt không?") — **user chốt bỏ**.

Phạm vi: **CHỈ màn Đề nghị thu tiền**. Màn Phiếu thu (`bill-incomes`) giữ nguyên "Người nộp tiền"
ở cả bản in lẫn file Excel (user chốt 2026-08-25 khi được hỏi).

📌 Màn Đề nghị thu tiền **không có chức năng xuất Excel** (đã rà: 17 màn Tài chính dùng
`downloadExcel`, không có màn này) → phần "xuất Excel" của yêu cầu không có gì để sửa.

- [x] **FE-1** `pages/finance/bill-income-requests/index.vue` — bỏ trường `payer` khỏi
      `filterFields` (ô "Người nộp" ở tìm kiếm nâng cao) và khỏi `initialStateForm`.
      Dùng chung cho cả màn CHỜ DUYỆT (`pending.vue` bọc chính file này).
- [x] **FE-2** `pages/finance/bill-income-requests/_id/print.vue` — bỏ dòng "Người nộp tiền".
- [x] **Verify** parse sạch bằng `vue-template-compiler` + `@babel/parser` (3 file: `index.vue`,
      `print.vue`, `pending.vue`); grep lại màn này **không còn chỗ nào đọc `payer`** (chỉ còn
      comment giải thích).

### Ghi chú

- Cấu hình bộ lọc đã lưu của user có chứa `payer` **không gây lỗi**: `V2BaseSmartFilterPanel`
  `mergedFields()` bỏ qua key không còn trong schema (`return null` + `filter(Boolean)`).
- **FE-3 (user báo ngay sau đó)** Khối thông tin bản in chia lệch **4 dòng trái / 2 dòng phải**:
  "Lý do thu" để `grid-column: 1 / -1` nên chiếm trọn hàng cuối, cộng với ô trống do bỏ dòng
  "Người nộp tiền". Bỏ span -> 6 ô chẵn, lưới 2 cột chia đều **3 dòng mỗi bên**:
  trái (Người đề nghị · Loại thu · Trạng thái) — phải (Phòng ban · Loại tiền · Lý do thu).
  📌 Thêm/bớt ô ở khối này phải giữ **tổng số ô CHẴN**, lẻ là lưới hụt 1 ô.
- `filterStateMixin` giữ bộ lọc trong `localStorage` **10 phút** khi user bấm vào 1 phiếu rồi quay
  lại; ai vừa gõ "Người nộp" trước đó có thể còn bị lọc ngầm tối đa 10 phút, sau đó tự hết.

### Checkpoint — 2026-08-25 (3)
Vừa hoàn thành: Phase 13 — bỏ hẳn "Người nộp" khỏi màn Đề nghị thu tiền (ô lọc + dòng trên bản in)
+ chia đều lại khối thông tin bản in (3 dòng mỗi cột). FE 2 file, BE 0 file, không migration.
Đang làm dở: không.
Bước tiếp theo: user mở màn danh sách + màn In 1 phiếu xem đã sạch chưa.
Chưa kiểm chứng bằng mắt: chỉ parse template/script (theo thoả thuận không tự test Playwright).
Blocked: không.

📌 **Không đụng BE:** cột `bill_income_requests.payer` vẫn lưu (form ERP có ghi), Resource vẫn trả,
criteria vẫn hiểu tham số `payer` — cần bật lại ô lọc thì chỉ thêm lại 1 khối trong `filterFields`.

---

## Phase 14 — Bộ tài liệu bàn giao: Testcase + HDSD + SRS (2026-08-28) @khoipv

Yêu cầu user: xuất **testcase, HDSD, SRS** cho màn Đề nghị thu tiền, bám đúng 3 skill
(`testcase-documenter`, `hdsd-documenter`, `srs-documenter`) và **lấy màn mẫu là bộ tài liệu
Danh mục khách hàng** (`.plans/gop-db/customer-docs/`, cũng chính là 2 file khung
`HDSD_MAU.docx` / `SRS_MAU.docx` đóng gói trong skill).

Phạm vi tài liệu: **cả 2 lối vào cùng 1 màn** — danh sách `/finance/bill-income-requests`
và màn chờ duyệt của kế toán `/finance/bill-income-requests/pending` (dùng chung component,
khác endpoint + bộ nút).

- [x] **TL-1** Đọc lại toàn bộ nguồn: routes · Controller · Service (đọc + ghi + 3 popup +
      thông báo) · Entity (6 trạng thái, 5 quyền, phạm vi theo cấp, `canView/canEdit/canReject`) ·
      3 FormRequest (nguyên văn thông báo lỗi) · 2 Resource · seeder quyền 1148-1152 ·
      FE `index.vue` / `pending.vue` / `create.vue` / `_id/{index,edit,print}.vue` /
      `BillIncomeRequestForm.vue` / `ContractSearchModal.vue` / `SupplierSearchModal.vue` ·
      menu `subsystem-menu/finance.js`.
- [x] **TL-2** Chụp ảnh thật bằng Playwright trên `hrm-crm.eteksofts.com` (tài khoản user cấp) —
      25 ảnh, lưu `dntt_shots/` (KHÔNG commit theo skill).
      Chỉ thao tác an toàn: mở form không lưu, các hộp xác nhận đều bấm Hủy/Đóng.
      1 lần bấm "Lưu và gửi duyệt" trên form TRỐNG để chụp lỗi bắt buộc nhập — dữ liệu chặn ở
      bước kiểm tra nên **không sinh phiếu nào**.
- [x] **TL-3** `gen_testcase.py` → `testcase - Phiếu đề nghị thu tiền.xlsx` (engine `tc_engine.py`).
- [x] **TL-4** `gen_hdsd.py` → `HDSD_Phiếu đề nghị thu tiền.docx` (engine `hdsd_engine.py`).
- [x] **TL-5** `gen_srs.py` → `SRS - Phiếu đề nghị thu tiền.docx` (thư viện `srs_docx_lib.py`).

### Ghi chú khi làm

- Tài khoản chụp ảnh đang bật **Cài đặt bộ lọc** ở chế độ rút gọn (5/9 tiêu chí). Đã bấm
  **Khôi phục mặc định → Lưu** để ảnh bộ lọc nâng cao hiện đủ 9 tiêu chí như thiết kế gốc.
  Đây là cấu hình hiển thị riêng của người dùng, không phải dữ liệu nghiệp vụ.
- Popup cấu hình cột trên giao diện có tiêu đề **"Tuỳ chỉnh cột"** (không phải "Cấu hình cột
  hiển thị" như tooltip của nút) — tài liệu ghi theo đúng chữ trên màn hình.
- Thứ tự cột trong ảnh là thứ tự đã tuỳ chỉnh của tài khoản chụp; tài liệu mô tả **thứ tự mặc
  định theo thiết kế** và nói rõ người dùng tự đổi được.

### Checkpoint — 2026-08-28
Vừa hoàn thành: Phase 14 — 3 tài liệu bàn giao + 3 generator, ảnh chụp thật 25 tấm.
Đang làm dở: không.
Bước tiếp theo: user mở 3 file đọc soát nội dung nghiệp vụ (đặc biệt bảng quyền và phần
"Tạo phiếu thu" — nút đã dựng nhưng màn Phiếu thu là feature khác).
Blocked: không.

---

## Phase 15 — Xuất lại SRS theo FORM MẪU MỚI của QA (2026-08-28)

Yêu cầu user: xuất lại `SRS - Phiếu đề nghị thu tiền.docx` theo bản mẫu QA gửi —
**"SRS - Danh mục quốc gia.docx"**
(https://docs.google.com/document/d/1tKvOQqJyK0bJC6BrZGM92974irpDAsFn/edit — chủ sở hữu
hangtechqa@gmail.com, sửa lần cuối 28/08/2026).

Quyết định đã chốt với user:
- **Phân quyền**: GIỮ quyền thật (Q1 + V1–V4 + ma trận ✅/❌ theo `PermissionsTableSeeder`),
  KHÔNG copy kiểu "chờ cập nhật" của mẫu — màn này đã có quyền thật, tài liệu phải nghiệm thu được.
- **Layout**: theo mẫu — ghi đường dẫn MENU, bỏ dòng "URL đầy đủ".
- **Skill**: chưa đụng `.claude/skills/srs-documenter` (tài sản chung, phải qua PR); form mới để
  ở `srs_form_v2.py` trong thư mục feature, chốt xong mới bung lên skill.

- [x] **TL-6** Đọc bản mẫu mới trên Google Drive, chốt 5 điểm khác so với form 2026-08-17.
- [x] **TL-7** `srs_form_v2.py` — lớp `SrsDocV2` bổ sung 3 thứ mẫu yêu cầu:
      `layout(menu=…)` (đường dẫn menu thay URL) · `rule_ref()` (đoạn "Quy tắc chung: Áp dụng
      SRS Các quy tắc chung <hyperlink>…" đầu mỗi mục Giới thiệu) · `rule_table()` (Phần 4 dạng
      bảng 5 cột STT / Mã quy tắc / Tên quy tắc / Mô tả / Phạm vi áp dụng).
- [x] **TL-8** Vá `gen_srs.py`: 12 mục Layout đổi sang menu, 12 đoạn "Quy tắc chung", Phần 4
      chuyển 17 BR sang bảng, câu dẫn "Quy tắc áp dụng" ở đầu Phần 4.
- [x] **TL-9** Sinh lại `SRS - Phiếu đề nghị thu tiền.docx` (41 bảng · 29 ảnh · 53 trang,
      mục lục đã update bằng Word) + tự kiểm: 0 chỗ còn "URL đầy đủ", 12 dòng Menu,
      12 đoạn Quy tắc chung, 13 hyperlink sang tài liệu quy tắc chung.

### Ghi chú khi làm

- Anchor `#heading=…` trỏ vào tài liệu **SRS_Các quy tắc chung_VN_1.0** lấy NGUYÊN từ bản mẫu
  (list / search / create / notice / history / excel / detail), không tự bịa. Chức năng đặc thù
  của màn này (Chọn đối tượng & hợp đồng, In phiếu) trỏ về link gốc không anchor.
- Đường dẫn menu lấy từ `components/subsystem-menu/finance.js`: nhóm *Khởi tạo phiếu yêu cầu -
  Công nợ - Thu - Chi* → *Đề nghị thu tiền*; màn chờ duyệt ở nhóm *Phê duyệt - Công nợ - Thu -
  Chi* → *Phiếu đề nghị thu tiền chờ duyệt*.
- Bảng "Mô tả chi tiết giao diện" giữ nguyên cấu hình 8/7/6 cột hiện có — bản mẫu cũng dùng
  4→8 cột tuỳ chức năng nên không phải sửa.

### Checkpoint — 2026-08-28
Vừa hoàn thành: TL-6 → TL-9, SRS đã xuất lại theo form mẫu mới.
Đang làm dở: không.
Bước tiếp theo: user mở file soát; nếu duyệt form thì tạo PR bung `srs_form_v2.py` lên
`.claude/skills/srs-documenter/` (cập nhật SKILL.md + srs_docx_lib.py + gen_srs_mau.py).
Blocked: không.

### Bổ sung — sửa sơ đồ Use Case (feedback user, 2026-08-28)

Feedback: (1) sơ đồ tổng quan sai nghiệp vụ — "phần lọc nó ở màn danh sách mà";
(2) còn chữ "HỆ THỐNG HRM — PHIẾU ĐỀ NGHỊ THU TIỀN" trên ảnh.

- [x] **TL-10** `uml_overview_v2.py` — vẽ lại sơ đồ tổng quan **có phân cấp**:
      chỉ 5 use case là màn hình thật (FR-01 danh sách · FR-04 lập · FR-06 sửa ·
      FR-07 chi tiết · FR-08 chờ duyệt) mới nối thẳng tới actor; 7 use case còn lại là
      thao tác NGAY TRÊN các màn đó nên nối bằng «include»/«extend»:
      FR-02 lọc · FR-03 cài đặt bộ lọc/tuỳ chỉnh cột · FR-10 xóa → «extend» FR-01;
      FR-05 chọn đối tượng & hợp đồng → «include» FR-04 và FR-06;
      FR-09 không duyệt · FR-11 in · FR-12 lịch sử → «extend» FR-07.
      Bỏ dòng tiêu đề "HỆ THỐNG HRM — …" trong khung.
- [x] **TL-11** `draw_usecase2()` — sửa CHIỀU MŨI TÊN cho đúng chuẩn UML ở cả 7 biểu đồ
      từng chức năng: «include» cha → con, «extend» con → cha (bản cũ vẽ ngược chiều extend).
- [x] **TL-12** Sinh lại `SRS - Phiếu đề nghị thu tiền.docx` (41 bảng · 29 ảnh · 53 trang).

### Checkpoint — 2026-08-28 (lần 2)
Vừa hoàn thành: TL-10 → TL-12, sơ đồ use case vẽ lại theo phân cấp màn hình.
Đang làm dở: không.
Bước tiếp theo: user soát lại Hình 1 + 7 biểu đồ use case từng chức năng.
Blocked: không.

### Bổ sung — bung form mới lên skill srs-documenter (2026-08-28)

User duyệt form → cập nhật skill dùng chung (KHÔNG commit, để user tự tạo PR).

- [x] **TL-13** `.claude/skills/srs-documenter/assets/srs_uml_render.py`
      + `draw_overview2()` (sơ đồ tổng quan có phân cấp, không tiêu đề khung);
      `draw_usecase()` sửa chiều mũi tên «extend»; `draw_overview()` cũ giữ lại + ghi chú deprecated.
- [x] **TL-14** `srs_docx_lib.py` — `layout(menu=…)` (nuốt `route=`/`url=` cũ nên generator cũ
      không vỡ) · `rule_ref()` + hằng `COMMON_DOC` / `ANCHOR` · `rule_table()` · `overview_figure2()`.
- [x] **TL-15** `gen_srs_mau.py` — khung mẫu cập nhật đủ 4 điểm của form mới.
- [x] **TL-16** `SKILL.md` — bảng "4 điểm của form 2026-08-28", đổi bản mẫu sang link Drive
      "SRS - Danh mục quốc gia" + trỏ file đối chiếu local là SRS Đề nghị thu tiền, mục Layout
      viết lại theo menu, bảng "cái gì vào mains / subs", bước tự kiểm tra bổ sung 4 assert mới.
- [x] **TL-17** `gen_srs.py` của màn này trỏ thẳng về `srs_docx_lib`; xóa 2 file tạm
      `srs_form_v2.py` + `uml_overview_v2.py`; sinh lại .docx — kết quả không đổi
      (41 bảng · 29 ảnh · 53 trang) → xác nhận skill chạy đúng.

### Checkpoint — 2026-08-28 (lần 3)
Vừa hoàn thành: TL-13 → TL-17, form mới đã nằm trong skill dùng chung.
Đang làm dở: không.
Bước tiếp theo: user tạo PR cho `hrm-claude-config` (4 file skill đang ở trạng thái modified).
Blocked: không.

- [x] **TL-18** Thay `assets/SRS_MAU.docx` = chính file `SRS - Phiếu đề nghị thu tiền.docx`
      (user chốt lấy màn này làm bản mẫu chuẩn). SKILL.md trỏ lại về `assets/SRS_MAU.docx`,
      ghi rõ generator sinh ra nó là `.plans/gop-db/finance-bill-income-request/gen_srs.py`,
      và nêu 1 điểm cố ý khác bản QA: form của team GIỮ quyền thật thay vì để "chờ cập nhật".
      Bản mẫu cũ (Danh mục khách hàng) lấy lại được bằng
      `git show 4be4678:hrm/.claude/skills/srs-documenter/assets/SRS_MAU.docx`.

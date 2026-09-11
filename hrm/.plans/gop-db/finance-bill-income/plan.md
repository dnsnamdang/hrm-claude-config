# Plan — Phiếu thu tiền (ERP → HRM)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để thực thi từng task. Step dùng checkbox (`- [ ]`) để theo dõi.

- Người phụ trách: @khoipv
- Nhánh: `gop_db` (cả 2 repo — KHÔNG tạo branch riêng)
- Spec: `docs/superpowers/specs/gop-db/2026-08-18-finance-bill-income-design.md` (ĐÃ DUYỆT 2026-08-18)
- Design tóm tắt: `.plans/gop-db/finance-bill-income/design.md`

**Goal:** Port màn ERP "Phiếu thu tiền" (`admin/income-expenditure/bill_incomes`, bảng `bill_incomes`) sang HRM tại `Modules/Finance` + `pages/finance/bill-incomes` — đầy đủ 1:1 gồm 4 chế độ danh sách, tạo/sửa/xóa nháp, duyệt kèm **ghi bút toán sổ cái**, hủy, in 2 liên, xuất Excel.

**Architecture:** BE bám bộ `BillIncomeRequest*` trong `Modules/Finance` (Entity + Service + FormRequest + Resource + ApiController), quyền kiểm bằng trait `ChecksEmployeePermission` chứ không dùng middleware. Phần ghi sổ cái tách riêng `BillIncomeAccountingService` với hàm **thuần** `buildEntries()` trả mảng dòng đã đủ cột — unit test được không cần DB, đây là cơ chế kiểm chứng chính. FE bám base màn Danh mục khách hàng qua bản đã port `pages/finance/bill-income-requests/index.vue`.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL (DB gộp `gop_db`, connection default) · PHPUnit 9.5 · Nuxt 2 / Vue 2 / Bootstrap-Vue.

## Global Constraints

- Nhánh git phải là `gop_db` ở CẢ `hrm-api` và `hrm-client` — kiểm `git branch --show-current` trước khi sửa file; sai nhánh thì DỪNG, báo lại.
- **KHÔNG git commit/push** — user tự commit.
- KHÔNG đổi schema 3 bảng `bill_incomes` / `bill_income_details` / `bill_income_detail_product_export_requests`, KHÔNG migration.
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`. **Model `TpXxx` thì ĐƯỢC dùng** nếu nó chạy trên connection mặc định — cụ thể `App\Models\TpCustomer` (bảng `customers` trên DB gộp) là luồng khách hàng duy nhất sau feature `customer-cut-mysql2`, và là entity mà `BillIncomeRequestDetail` đang dùng. Đừng thay bằng `Modules\Timesheet\Entities\Customer` (id lệch).
- KHÔNG nới `$guarded` của `Modules/Finance/Entities/Accounting/AccountDetail.php` (đang là entity CHỈ ĐỌC, `BillIncomeDebtService` phụ thuộc) — ghi sổ cái qua entity mới `AccountDetailEntry`.
- KHÔNG sửa `registerMorphMap()` ngoài việc THÊM đúng 1 cặp cho `BillIncome` (Task 2). Không đụng 10 cặp đã có.
- `ValidationException` KHÔNG được catch — để bay lên cho FE nhận 422 chuẩn Laravel.
- KHÔNG gắn middleware `checkPermission` cho route nào của màn này — gate trong Controller/Entity (lý do: spec §4.3).
- Cờ quyền FE **fail-closed**: khởi tạo `false`, cấm gán literal `true` (pattern bị chặn khi review: `can[A-Za-z]*\s*=\s*true`).
- KHÔNG chạy `PermissionsTableSeeder` trên DB local (`run()` truncate bảng, và seeder đang có lỗi trùng id 1117/1118 sẵn).
- KHÔNG tự test bằng Playwright — verify bằng `php -l` + phpunit + tinker (BE) và parse `vue-template-compiler` + `@babel/parser` (FE); user tự mở trình duyệt.
- Dữ liệu nghiệp vụ đã lưu: **không sửa**. Mọi bản ghi test tạo ra phải xóa sạch. Baseline **đã đếm thật 2026-08-18**: `bill_incomes` **2.347** · `bill_income_details` **7.401** · `account_details` **971.973** · `account_detail_refs` **1.024.988**. (Con số 971.914 trong docblock `AccountDetail.php` là của feature cũ, đã lỗi thời — dùng số đếm thật.) Dòng `account_details` mới nhất là `2026-08-14`, tức DB không có ai ghi song song → so sánh baseline bằng **bằng đúng** là hợp lệ.
- Mọi text hiển thị tiếng Việt. Toast dùng đúng câu ERP đã ghi trong spec §5.5.
- ⚠️ **Tên quan hệ trộn 2 kiểu — đây là bẫy đã dính 1 lần, đọc kỹ:**
  - Entity **MỚI** của feature này (`BillIncome`, `BillIncomeDetail`) dùng **camelCase**: `details`, `billIncomeRequest`, `employeeCreate`, `approvedBy`, `accountDept`, `accountHas`, `customer`, `supplier`, `employee`, `objectable`, `productExportRequests`.
  - Entity **CŨ** `BillIncomeRequest` (feature trước, KHÔNG được sửa) dùng **snake_case**: `details`, `currency`, `employee_create`, `employee_update`, `approved_by`.
  → Eager load xuyên 2 entity phải viết `billIncomeRequest.employee_create.info`, KHÔNG phải `billIncomeRequest.employeeCreate.info`. Sai tên là Eloquent ném `Call to undefined relationship` lúc chạy, `php -l` không bắt được.
- FE trước khi code phải đọc: `.claude/skills/erp-to-hrm-screen/SKILL.md`, `list-page`, `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`, `select-and-input-state`, `print-page`, `notification-convention`. Icon phải đối chiếu font local: `grep "^\.ri-xxx:before" hrm-client/assets/scss/custom/plugins/icons/_remixicon.scss`.

---

## Phase 1 — Backend nền tảng (Task 1-6): xem được danh sách + chi tiết

### Task 1: Entity `BillIncome` + 2 entity chi tiết

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php`
- Create: `hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeDetail.php`
- Create: `hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeDetailProductExportRequest.php`

**Interfaces:**
- Consumes: `Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest` (đã có), `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (đã có), `Modules\Human\Entities\Employee`.
- Produces: class `Modules\Finance\Entities\BillIncome\BillIncome` — hằng `STATUS_CREATING = 1`, `STATUS_AWAITING_APPROVE = 2`, `STATUS_APPROVED = 3`, `STATUS_CANCEL = 4`, `STATUSES` (mảng 4 phần tử `id/name/type`), 3 hằng `PERMISSION_*`; quan hệ `details()`, `billIncomeRequest()`, `employeeCreate()`, `approvedBy()`; static `generateCode(): string`. Task 2-10 dùng class này.

- [x] **Step 1: Kiểm tra branch cả 2 repo**

Chạy: `git -C D:/laragon/www/hrm/hrm-api branch --show-current` và `git -C D:/laragon/www/hrm/hrm-client branch --show-current`
Kỳ vọng: cả 2 in `gop_db`. Khác → DỪNG, báo user.

- [x] **Step 2: Đếm baseline dữ liệu**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT (SELECT COUNT(*) FROM bill_incomes) bi, (SELECT COUNT(*) FROM bill_income_details) bid, (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Ghi lại 4 con số vào checkpoint — cuối Task 17 phải về đúng giá trị này.

- [x] **Step 3: Viết `BillIncome.php`**

```php
<?php

namespace Modules\Finance\Entities\BillIncome;

use Illuminate\Database\Eloquent\Model;
use Modules\Finance\Entities\Account\Account;
use Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest;
use Modules\Finance\Entities\Concerns\ChecksEmployeePermission;
use Modules\Human\Entities\Employee;

/**
 * Phiếu thu tiền — bảng ERP `bill_incomes` trên DB gộp (port từ
 * `App\Model\IncomeExpenditure\BillIncome` bên ERP, 2.347 dòng dữ liệu thật).
 *
 * DÙNG CHUNG bảng với cổng ERP: KHÔNG đổi schema, KHÔNG migration.
 *
 * KHÔNG kế thừa BaseModel của HRM. 3 cột đơn vị tổ chức gán ở hook `creating` (KHÔNG bắt chước
 * ERP gán ở `created` rồi `save()` lần 2 — 2 câu ghi và để lại bản ghi nửa vời nếu lần 2 lỗi).
 *
 * KHÔNG khai accessor `getDateAccountingAttribute()` trả `d/m/Y` như ERP: cột này được ghi thẳng
 * vào sổ cái (`invoiceable_date_accounting`), ERP phải `preg_match` đổi ngược lại — HRM giữ
 * `Y-m-d` từ đầu, format ở Resource.
 *
 * Kiểm tra quyền dùng trait `ChecksEmployeePermission` (query thẳng pivot spatie, so theo `name`
 * không lọc guard) chứ KHÔNG dùng `$user->can()` như ERP.
 *
 * @property int    $id
 * @property string $code
 * @property int    $bill_income_request_id
 * @property int    $status
 * @property int    $account_dept
 * @property int    $created_by
 * @property int    $approved_id
 * @property int    $company_id
 * @property float  $sum_money
 */
class BillIncome extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'bill_incomes';

    protected $fillable = [
        'code',
        'bill_income_request_id',
        'status',
        'date_accounting',
        'created_by',
        'updated_by',
        'account_dept',
        'exchange_rate',
        'approved_id',
        'company_id',
        'department_id',
        'part_id',
        'note',
        'payer',
        'sum_money',
    ];

    const STATUS_CREATING = 1;          // Đang tạo
    const STATUS_AWAITING_APPROVE = 2;  // Chờ duyệt
    const STATUS_APPROVED = 3;          // Đã duyệt
    const STATUS_CANCEL = 4;            // Hủy

    public const STATUSES = [
        ['id' => self::STATUS_CREATING, 'name' => 'Đang tạo', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_APPROVE, 'name' => 'Chờ duyệt', 'type' => 'danger'],
        ['id' => self::STATUS_APPROVED, 'name' => 'Đã duyệt', 'type' => 'success'],
        ['id' => self::STATUS_CANCEL, 'name' => 'Hủy', 'type' => 'danger'],
    ];

    /** Tên giữ y hệt ERP. Bản HRM guard `api` id 1500-1502 (Task 3); bản ERP guard `web` đã có sẵn. */
    const PERMISSION_VIEW_ALL_COMPANY = 'Xem tất cả phiếu thu của tổng công ty';
    const PERMISSION_VIEW_COMPANY = 'Xem tất cả phiếu thu của công ty';
    const PERMISSION_TREASURER = 'Thủ quỹ duyệt phiếu thu';

    protected static function boot()
    {
        parent::boot();

        static::creating(function (self $model) {
            $info = optional(auth()->user())->info;

            // 3 cột đơn vị tổ chức GÁN ĐÈ VÔ ĐIỀU KIỆN từ người đăng nhập — đúng ERP
            // (`created` hook :71-74 gán thẳng, không xét giá trị đang có). KHÔNG dùng `??`:
            // 3 cột này nằm trong $fillable, nếu client gửi lên `0` hoặc `""` thì `??` sẽ giữ
            // nguyên (chỉ null mới rơi vế phải), MySQL ép về 0, và bản ghi lọt khỏi mọi nhánh
            // lọc theo cấp. Đơn vị tổ chức của phiếu là của người lập, không phải thứ client khai.
            $model->company_id = optional($info)->company_id;
            $model->department_id = optional($info)->department_id;
            $model->part_id = optional($info)->part_id;

            $model->created_by = $model->created_by ?: auth()->id();
        });

        static::saving(function (self $model) {
            $model->updated_by = auth()->id() ?? $model->updated_by;
        });
    }

    public function details()
    {
        return $this->hasMany(BillIncomeDetail::class, 'parent_id', 'id');
    }

    public function billIncomeRequest()
    {
        return $this->belongsTo(BillIncomeRequest::class, 'bill_income_request_id', 'id');
    }

    public function accountDept()
    {
        return $this->belongsTo(Account::class, 'account_dept', 'id');
    }

    public function employeeCreate()
    {
        return $this->belongsTo(Employee::class, 'created_by', 'id');
    }

    public function approvedBy()
    {
        return $this->belongsTo(Employee::class, 'approved_id', 'id');
    }

    /**
     * Mã phiếu `{mã công ty}.PT{mmyy}.{5 số}`.
     *
     * Copy pattern `BillIncomeRequest::generateCode()` (:382) — có `lockForUpdate()`. ERP dùng
     * `autoGenerateCode()` KHÔNG khóa: 2 phiếu tạo cùng lúc sinh trùng mã, mà `code` là UNIQUE
     * nên 1 phiếu chết. Phải gọi trong transaction.
     */
    public static function generateCode(): string
    {
        $companyCode = optional(optional(auth()->user())->info)->company->code ?? '';
        $prefix = $companyCode . '.PT' . now()->format('my') . '.';

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
}
```

- [x] **Step 4: Viết `BillIncomeDetail.php`**

```php
<?php

namespace Modules\Finance\Entities\BillIncome;

use Illuminate\Database\Eloquent\Model;
use Modules\Finance\Entities\Account\Account;
use Modules\Finance\Entities\Supplier;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Entities\Customer;

/**
 * Chi tiết phiếu thu — bảng ERP `bill_income_details` (7.401 dòng).
 *
 * `objectable_type` lưu TÊN CLASS PHP CỦA ERP; map ngược bằng `Relation::morphMap()` đã đăng ký
 * trong `FinanceServiceProvider` (10 class, có sẵn từ màn Đề nghị thu tiền).
 *
 * 3 cặp tiền: `_request` = đề nghị thu (chỉ đọc), `_approve` = duyệt thu (kế toán nhập lúc lập),
 * `_real` = thực thu (thủ quỹ nhập lúc duyệt — chính là số ghi vào sổ cái).
 * Hậu tố `_exchange` = giá trị quy đổi VND.
 */
class BillIncomeDetail extends Model
{
    protected $table = 'bill_income_details';

    protected $fillable = [
        'parent_id',
        'customer_id',
        'supplier_id',
        'employee_id',
        'objectable_id',
        'objectable_type',
        'income_money_request',
        'income_money_request_exchange',
        'income_money_approve',
        'income_money_approve_exchange',
        'income_money_real',
        'income_money_real_exchange',
        'account_has',
        'is_income_begin',
        'note',
    ];

    public function parent()
    {
        return $this->belongsTo(BillIncome::class, 'parent_id', 'id');
    }

    public function objectable()
    {
        return $this->morphTo();
    }

    public function accountHas()
    {
        return $this->belongsTo(Account::class, 'account_has', 'id');
    }

    public function customer()
    {
        return $this->belongsTo(Customer::class, 'customer_id', 'id');
    }

    public function supplier()
    {
        return $this->belongsTo(Supplier::class, 'supplier_id', 'id');
    }

    public function employee()
    {
        return $this->belongsTo(Employee::class, 'employee_id', 'id');
    }

    public function productExportRequests()
    {
        return $this->hasMany(BillIncomeDetailProductExportRequest::class, 'bill_income_detail_id', 'id');
    }
}
```

- [x] **Step 5: Viết `BillIncomeDetailProductExportRequest.php`**

```php
<?php

namespace Modules\Finance\Entities\BillIncome;

use Illuminate\Database\Eloquent\Model;

/**
 * Phân bổ tiền thu theo phiếu xuất hàng — bảng ERP
 * `bill_income_detail_product_export_requests`.
 *
 * ⚠️ Bảng có **0 dòng** trên DB gộp (đếm 2026-08-18). Vẫn port đủ theo quyết định của user
 * (spec §2), nhưng KHÔNG có dữ liệu mẫu để test chạy thật — chỉ verify bằng đọc code đối chiếu.
 */
class BillIncomeDetailProductExportRequest extends Model
{
    protected $table = 'bill_income_detail_product_export_requests';

    protected $fillable = [
        'bill_income_detail_id',
        'product_export_request_id',
        'objectable_id',
        'objectable_type',
        // NOT NULL trên DB — thiếu là insert nổ. ERP lưu sẵn mã và giá trị đã phân bổ sau VAT
        // để bản in / màn sửa không phải join ngược sang phiếu xuất hàng.
        'objectable_code',
        'sum_amount_allocated_after_vat',
        'allocated_value',
        'allocated_value_exchange',
    ];

    public function objectable()
    {
        return $this->morphTo();
    }

    public function detail()
    {
        return $this->belongsTo(BillIncomeDetail::class, 'bill_income_detail_id', 'id');
    }
}
```

- [x] **Step 6: Kiểm tên class phụ thuộc có thật**

3 class import ở Step 4 phải tồn tại, nếu không thì đổi cho đúng:
```bash
ls hrm-api/Modules/Finance/Entities/Account/Account.php hrm-api/Modules/Finance/Entities/Supplier.php
grep -rn "class Customer" hrm-api/Modules/Timesheet/Entities/Customer.php
grep -rn "use Modules\\\\Timesheet\\\\Entities\\\\Customer" hrm-api/Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequestDetail.php
```
Dòng cuối cho biết màn Đề nghị thu tiền đang dùng entity khách hàng nào — **dùng đúng entity đó**, đừng chọn khác (id khách hàng ERP ≠ id HRM).

- [x] **Step 7: Verify cú pháp**

```bash
php -l hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php
php -l hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeDetail.php
php -l hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeDetailProductExportRequest.php
```
Kỳ vọng: cả 3 in `No syntax errors detected`.

- [x] **Step 8: Verify đọc được dữ liệu thật**

```bash
cd hrm-api && php artisan tinker --execute="\$b = Modules\Finance\Entities\BillIncome\BillIncome::with('details')->orderBy('id','desc')->first(); echo \$b->code, ' | details=', \$b->details->count(), ' | req=', optional(\$b->billIncomeRequest)->code, PHP_EOL;"
```
Kỳ vọng: in ra mã phiếu dạng `xxx.PT....`, số chi tiết ≥ 1, mã phiếu đề nghị dạng `xxx.DNTT....`.

---

### Task 2: Entity ghi sổ cái + đăng ký morphMap cho `BillIncome`

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/Accounting/AccountDetailEntry.php`
- Create: `hrm-api/Modules/Finance/Entities/Accounting/AccountDetailRef.php`
- Modify: `hrm-api/Modules/Finance/Providers/FinanceServiceProvider.php` (hàm `registerMorphMap()`, thêm đúng 1 dòng)

**Interfaces:**
- Consumes: `Modules\Finance\Entities\BillIncome\BillIncome` (Task 1).
- Produces: `Modules\Finance\Entities\Accounting\AccountDetailEntry` (ghi được, `$table = 'account_details'`, hằng `TYPE_DEBT = 1` / `TYPE_HAS = 2`) và `AccountDetailRef` (`$table = 'account_detail_refs'`, fillable `account_detail_id` + `account_ref_id`). Task 9 dùng để persist bút toán.

- [x] **Step 1: Viết `AccountDetailEntry.php`**

```php
<?php

namespace Modules\Finance\Entities\Accounting;

use Illuminate\Database\Eloquent\Model;

/**
 * Dòng sổ cái — GHI vào bảng ERP `account_details` (971.914 dòng).
 *
 * Vì sao có class riêng thay vì nới `AccountDetail`: `AccountDetail` được khai CHỈ ĐỌC
 * (`$guarded = ['*']`, docblock ghi "việc GHI sổ cái vẫn do cổng ERP làm") và
 * `BillIncomeDebtService` đang dựa vào hợp đồng đó. Nới guard sẽ đổi nghĩa 1 class dùng chung.
 *
 * ⚠️ KHÔNG khai hook `created` denormalize như ERP (`App\Model\Accounting\AccountDetail:134-232`,
 * điền 15 cột rồi `save()` lần 2). Toàn bộ phần denormalize làm tường minh trong
 * `BillIncomeAccountingService::buildEntries()` để unit test được không cần DB (spec §5.6.1).
 * Hệ quả: `$fillable` ở đây phải liệt kê ĐỦ cả 15 cột denormalize.
 */
class AccountDetailEntry extends Model
{
    protected $table = 'account_details';

    /** Bên Nợ. */
    const TYPE_DEBT = 1;

    /** Bên Có. */
    const TYPE_HAS = 2;

    protected $fillable = [
        // 14 cột ERP truyền thẳng khi create()
        'account_id',
        'customer_id',
        'supplier_id',
        'employee_id',
        'money_value',
        'money_value_exchange',
        'type',
        'currency_id',
        'exchange_rate',
        'invoiceable_id',
        'invoiceable_type',
        'contractable_id',
        'contractable_type',
        'billable_id',
        'billable_type',
        // 15 cột hook `created` của ERP điền thêm — HRM điền tường minh
        'identify_number',
        'company_id',
        'department_id',
        'part_id',
        'created_by',
        'invoiceable_code',
        'invoiceable_date_accounting',
        'contractable_code',
        'contract_type',
        'contract_created_by',
        'contract_customer_id',
        'invoice_type',
        'employee_company_id',
        'employee_department_id',
        'employee_part_id',
    ];
}
```

- [x] **Step 2: Viết `AccountDetailRef.php`**

```php
<?php

namespace Modules\Finance\Entities\Accounting;

use Illuminate\Database\Eloquent\Model;

/**
 * Dòng đối ứng của bút toán — bảng ERP `account_detail_refs`.
 * Mỗi dòng bên Có sinh 1 dòng ở đây trỏ về tài khoản Nợ của phiếu (`bill_incomes.account_dept`).
 */
class AccountDetailRef extends Model
{
    protected $table = 'account_detail_refs';

    protected $fillable = [
        'account_detail_id',
        'account_ref_id',
    ];
}
```

- [x] **Step 3: Thêm 1 cặp vào morphMap**

Mở `hrm-api/Modules/Finance/Providers/FinanceServiceProvider.php`, trong `registerMorphMap()` thêm **đúng 1 dòng** vào cuối mảng (giữ nguyên 10 dòng đã có):

```php
            // Chứng từ phiếu thu — để `account_details.invoiceable_type` ghi đúng chuỗi class ERP,
            // nếu không cổng ERP đọc sổ cái sẽ không resolve được chứng từ (spec §5.6).
            'App\Model\IncomeExpenditure\BillIncome'      => BillIncome\BillIncome::class,
```

Thêm `use Modules\Finance\Entities\BillIncome;` vào phần import nếu chưa có (đối chiếu cách file này đang alias `FinanceContract`).

- [x] **Step 4: Verify cú pháp + morphMap hoạt động 2 chiều**

```bash
php -l hrm-api/Modules/Finance/Entities/Accounting/AccountDetailEntry.php
php -l hrm-api/Modules/Finance/Entities/Accounting/AccountDetailRef.php
php -l hrm-api/Modules/Finance/Providers/FinanceServiceProvider.php
cd hrm-api && php artisan tinker --execute="\$m = Illuminate\Database\Eloquent\Relations\Relation::morphMap(); echo count(\$m), ' cặp', PHP_EOL; echo \$m['App\Model\IncomeExpenditure\BillIncome'] ?? 'THIẾU', PHP_EOL; echo (new Modules\Finance\Entities\BillIncome\BillIncome)->getMorphClass(), PHP_EOL;"
```
Kỳ vọng: **11 cặp** (10 cũ + 1 mới), dòng 2 in class HRM, dòng 3 in `App\Model\IncomeExpenditure\BillIncome`. Nếu dòng 3 in class HRM → morphMap chưa ăn, kiểm lại import.

- [x] **Step 5: Verify không phá 10 cặp cũ**

```bash
cd hrm-api && php artisan tinker --execute="\$d = Modules\Finance\Entities\BillIncome\BillIncomeDetail::whereNotNull('objectable_type')->first(); echo \$d->objectable_type, ' -> ', get_class(\$d->objectable), PHP_EOL;"
```
Kỳ vọng: in chuỗi class ERP rồi mũi tên sang class HRM tương ứng, KHÔNG lỗi "Class not found".

---

### Task 3: Quyền — seeder + lớp quyết định thuần + unit test

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeAccess.php`
- Create: `hrm-api/tests/Unit/BillIncomeAccessTest.php`
- Modify: `hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php` (thêm 5 method cờ quyền ở cuối class)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm 3 dòng)

**Interfaces:**
- Consumes: hằng `PERMISSION_*` và `STATUS_*` của `BillIncome` (Task 1); trait `ChecksEmployeePermission` (đã có, method `currentEmployeeHasPermission(string): bool` và `currentEmployeeIsSuperAdmin(): bool`).
- Produces: `BillIncomeAccess::canView(array $ctx, array $bill): bool`, `::canEdit(array $bill): bool`, `::canDelete(array $bill): bool`, `::canApprove(array $ctx, array $bill): bool`; và trên entity: `BillIncome::context(): array`, `$bill->canView()/canEdit()/canDelete()/canApprove(): bool`, `BillIncome::isTreasurer(): bool`. Task 4/5/6/7/9 dùng.

- [x] **Step 1: Viết test trước (test thuần, không DB, không auth)**

Tạo `hrm-api/tests/Unit/BillIncomeAccessTest.php`:

```php
<?php

namespace Tests\Unit;

use Modules\Finance\Entities\BillIncome\BillIncomeAccess;
use PHPUnit\Framework\TestCase;

/**
 * Unit test phần quyết định thuần của quyền xem/sửa/xóa/duyệt phiếu thu.
 * Mirror ERP `BillIncome::canView()/canEdit()/canDelete()` + `searchByFilter()`.
 * Không phụ thuộc auth/DB — cùng kiểu với `CustomerPhoneVisibilityTest`.
 */
class BillIncomeAccessTest extends TestCase
{
    private const ME = 100;

    /** Không quyền gì, không phải super admin. */
    private function ctxNone(): array
    {
        return [
            'employee_id' => self::ME,
            'is_super_admin' => false,
            'view_all_company' => false,
            'view_company' => false,
            'is_treasurer' => false,
            'company_id' => 9,
        ];
    }

    private function bill(array $overrides = []): array
    {
        return array_merge([
            'created_by' => 999,
            'approved_id' => null,
            'status' => 3,
            'company_id' => 9,
        ], $overrides);
    }

    public function test_owner_can_view_even_when_creating(): void
    {
        $this->assertTrue(BillIncomeAccess::canView(
            $this->ctxNone(),
            $this->bill(['created_by' => self::ME, 'status' => 1])
        ));
    }

    public function test_approver_can_view(): void
    {
        $this->assertTrue(BillIncomeAccess::canView(
            $this->ctxNone(),
            $this->bill(['approved_id' => self::ME])
        ));
    }

    public function test_stranger_cannot_view_without_permission(): void
    {
        $this->assertFalse(BillIncomeAccess::canView($this->ctxNone(), $this->bill()));
    }

    public function test_view_all_company_can_view_other_company(): void
    {
        $ctx = array_merge($this->ctxNone(), ['view_all_company' => true]);
        $this->assertTrue(BillIncomeAccess::canView($ctx, $this->bill(['company_id' => 77])));
    }

    /** Quyền xem KHÔNG mở phiếu nháp của người khác — mirror nhánh `status != STATUS_CREATING` của ERP. */
    public function test_view_permission_does_not_expose_other_people_drafts(): void
    {
        $ctx = array_merge($this->ctxNone(), ['view_all_company' => true]);
        $this->assertFalse(BillIncomeAccess::canView($ctx, $this->bill(['status' => 1])));
    }

    public function test_view_company_only_same_company(): void
    {
        $ctx = array_merge($this->ctxNone(), ['view_company' => true]);
        $this->assertTrue(BillIncomeAccess::canView($ctx, $this->bill(['company_id' => 9])));
        $this->assertFalse(BillIncomeAccess::canView($ctx, $this->bill(['company_id' => 77])));
    }

    /**
     * ERP so `$this->company_id == $user->info->company_id` nên null == null ra true
     * → người không thuộc công ty nào xem được phiếu không thuộc công ty nào. HRM chặn.
     */
    public function test_null_company_is_not_a_match(): void
    {
        $ctx = array_merge($this->ctxNone(), ['view_company' => true, 'company_id' => null]);
        $this->assertFalse(BillIncomeAccess::canView($ctx, $this->bill(['company_id' => null])));
    }

    public function test_super_admin_sees_everything(): void
    {
        $ctx = array_merge($this->ctxNone(), ['is_super_admin' => true]);
        $this->assertTrue(BillIncomeAccess::canView($ctx, $this->bill(['status' => 1, 'company_id' => 77])));
    }

    public function test_edit_and_delete_only_when_creating(): void
    {
        $this->assertTrue(BillIncomeAccess::canEdit($this->bill(['status' => 1])));
        $this->assertTrue(BillIncomeAccess::canDelete($this->bill(['status' => 1])));

        foreach ([2, 3, 4] as $status) {
            $this->assertFalse(BillIncomeAccess::canEdit($this->bill(['status' => $status])));
            $this->assertFalse(BillIncomeAccess::canDelete($this->bill(['status' => $status])));
        }
    }

    public function test_approve_needs_treasurer_and_awaiting_status(): void
    {
        $treasurer = array_merge($this->ctxNone(), ['is_treasurer' => true]);

        $this->assertTrue(BillIncomeAccess::canApprove($treasurer, $this->bill(['status' => 2])));
        $this->assertFalse(BillIncomeAccess::canApprove($treasurer, $this->bill(['status' => 3])));
        $this->assertFalse(BillIncomeAccess::canApprove($this->ctxNone(), $this->bill(['status' => 2])));
    }

    /** Không xác định được người đăng nhập -> fail-closed. */
    public function test_no_employee_id_is_fail_closed(): void
    {
        $ctx = array_merge($this->ctxNone(), ['employee_id' => null]);
        $this->assertFalse(BillIncomeAccess::canView($ctx, $this->bill(['created_by' => null])));
    }
}
```

- [x] **Step 2: Chạy test để chắc chắn nó FAIL**

```bash
cd hrm-api && php vendor/bin/phpunit --filter BillIncomeAccessTest
```
Kỳ vọng: FAIL với `Class "Modules\Finance\Entities\BillIncome\BillIncomeAccess" not found`.

- [x] **Step 3: Viết `BillIncomeAccess.php`**

```php
<?php

namespace Modules\Finance\Entities\BillIncome;

/**
 * Quyết định thuần về quyền trên 1 phiếu thu — không đụng auth/DB nên unit test được.
 *
 * Port ERP `BillIncome::canView()` (:536), `canEdit()` (:559), `canDelete()` (:570) và nhánh
 * quyền của `searchByFilter()` (:171).
 *
 * `$ctx`: employee_id · is_super_admin · view_all_company · view_company · is_treasurer · company_id
 * `$bill`: created_by · approved_id · status · company_id
 */
class BillIncomeAccess
{
    public static function canView(array $ctx, array $bill): bool
    {
        if (!empty($ctx['is_super_admin'])) {
            return true;
        }

        $me = $ctx['employee_id'] ?? null;
        // Fail-closed: không xác định được người đăng nhập thì không cho xem.
        if ($me === null) {
            return false;
        }

        if (($bill['created_by'] ?? null) === $me) {
            return true;
        }

        if (($bill['approved_id'] ?? null) === $me) {
            return true;
        }

        // Quyền xem theo cấp KHÔNG mở phiếu nháp của người khác.
        if (($bill['status'] ?? null) === BillIncome::STATUS_CREATING) {
            return false;
        }

        if (!empty($ctx['view_all_company'])) {
            return true;
        }

        if (!empty($ctx['view_company'])) {
            $mine = $ctx['company_id'] ?? null;
            $theirs = $bill['company_id'] ?? null;

            // null KHÔNG khớp null (ERP dùng `==` nên coi là cùng công ty — lỗ hổng).
            return $mine !== null && $theirs !== null && $mine === $theirs;
        }

        return false;
    }

    public static function canEdit(array $bill): bool
    {
        return ($bill['status'] ?? null) === BillIncome::STATUS_CREATING;
    }

    public static function canDelete(array $bill): bool
    {
        return ($bill['status'] ?? null) === BillIncome::STATUS_CREATING;
    }

    public static function canApprove(array $ctx, array $bill): bool
    {
        return ($bill['status'] ?? null) === BillIncome::STATUS_AWAITING_APPROVE
            && !empty($ctx['is_treasurer']);
    }
}
```

- [x] **Step 4: Chạy test — phải PASS**

```bash
cd hrm-api && php vendor/bin/phpunit --filter BillIncomeAccessTest
```
Kỳ vọng: `OK (11 tests, ...)`. Nếu `test_no_employee_id_is_fail_closed` fail thì kiểm lại thứ tự nhánh: check `$me === null` phải đứng TRƯỚC so `created_by`.

- [x] **Step 5: Nối vào entity `BillIncome`**

Thêm vào cuối class `BillIncome` (trước dấu `}` đóng class):

```php
    /** Ngữ cảnh quyền của người đang đăng nhập — 1 chỗ duy nhất, dùng lại cho cả list lẫn detail. */
    public static function context(): array
    {
        return [
            'employee_id' => auth()->id(),
            'is_super_admin' => self::currentEmployeeIsSuperAdmin(),
            'view_all_company' => self::currentEmployeeHasPermission(self::PERMISSION_VIEW_ALL_COMPANY),
            'view_company' => self::currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY),
            'is_treasurer' => self::isTreasurer(),
            'company_id' => optional(optional(auth()->user())->info)->company_id,
        ];
    }

    /** Thủ quỹ — vai duyệt/hủy phiếu thu. Super admin cũng tính là có. */
    public static function isTreasurer(): bool
    {
        return self::currentEmployeeIsSuperAdmin()
            || self::currentEmployeeHasPermission(self::PERMISSION_TREASURER);
    }

    private function asArray(): array
    {
        return [
            'created_by' => $this->created_by === null ? null : (int) $this->created_by,
            'approved_id' => $this->approved_id === null ? null : (int) $this->approved_id,
            'status' => (int) $this->status,
            'company_id' => $this->company_id === null ? null : (int) $this->company_id,
        ];
    }

    public function canView(): bool
    {
        return BillIncomeAccess::canView(self::context(), $this->asArray());
    }

    public function canEdit(): bool
    {
        return BillIncomeAccess::canEdit($this->asArray());
    }

    public function canDelete(): bool
    {
        return BillIncomeAccess::canDelete($this->asArray());
    }

    public function canApprove(): bool
    {
        return BillIncomeAccess::canApprove(self::context(), $this->asArray());
    }
```

⚠️ `context()['employee_id']` là `auth()->id()` (int hoặc null) còn `asArray()` ép `(int)` — 2 bên phải cùng kiểu vì `BillIncomeAccess` so bằng `===`. Nếu `auth()->id()` trả string thì bọc `(int)` luôn.

- [x] **Step 6: Thêm 3 quyền vào seeder**

Mở `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, thêm ngay sau khối quyền của màn Đề nghị thanh toán (tìm bằng `grep -n "1176" file`):

```php
        // Màn Phiếu thu tiền (port ERP `bill_incomes`) — tên giữ NGUYÊN VĂN như ERP.
        // Bản ERP của 3 quyền này đã tồn tại trên DB gộp ở guard `web` (id 100178/100183/100184);
        // `ChecksEmployeePermission` so theo `name` không lọc guard nên 2 bản dùng lẫn được.
        // Quyền tạo/sửa phiếu thu dùng LẠI 'Kế toán thanh toán' (id 1152), không khai mới.
        Permission::create(['id' => 1500, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu thu của tổng công ty', 'display_name' => 'Xem tất cả phiếu thu của tổng công ty', 'group' => 'Phiếu thu tiền', 'type' => 8, 'sort_order' => 1]);
        Permission::create(['id' => 1501, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu thu của công ty', 'display_name' => 'Xem tất cả phiếu thu của công ty', 'group' => 'Phiếu thu tiền', 'type' => 8, 'sort_order' => 2]);
        Permission::create(['id' => 1502, 'guard_name' => 'api', 'name' => 'Thủ quỹ duyệt phiếu thu', 'display_name' => 'Thủ quỹ duyệt phiếu thu', 'group' => 'Phiếu thu tiền', 'type' => 8, 'sort_order' => 3]);
```

⚠️ Trước khi thêm, chạy `grep -n "'id' => 15[0-9][0-9]" file` để chắc 1500/1501/1502 chưa ai dùng. **KHÔNG chạy seeder.**

- [x] **Step 7: Verify**

```bash
php -l hrm-api/Modules/Finance/Entities/BillIncome/BillIncomeAccess.php
php -l hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php
php -l hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
cd hrm-api && php vendor/bin/phpunit --filter BillIncomeAccessTest
cd hrm-api && php artisan tinker --execute="\$b = Modules\Finance\Entities\BillIncome\BillIncome::where('status',3)->first(); var_dump(\$b->canEdit(), \$b->canDelete(), \$b->canApprove());"
```
Kỳ vọng: 3 file sạch; test OK; tinker in `false false false` (phiếu đã duyệt thì không sửa/xóa/duyệt được).

⚠️ `context()` cache theo tiến trình (trait `ChecksEmployeePermission`) — nếu test 2 tài khoản trong 1 lệnh tinker sẽ dùng chung danh tính. Muốn so 2 người thì chạy 2 lệnh riêng.

---

### Task 4: `BillIncomeService` — lọc danh sách 4 chế độ

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillIncomeService.php`

**Interfaces:**
- Consumes: `BillIncome`, `BillIncomeDetail` (Task 1); `BillIncomeRequest` (đã có).
- Produces: `BillIncomeService::searchByFilter(Request $request, string $mode = 'my'): LengthAwarePaginator` và `::meta(): array` (options cho dropdown lọc: `statuses`, `types`). Task 6 dùng.

- [x] **Step 1: Đọc bản đang có để bám đúng khuôn**

```bash
sed -n '1,120p' hrm-api/Modules/Finance/Services/BillIncomeRequestService.php
```
Bám đúng cách file này nhận `$request`, phân trang, và trả `meta()`.

- [x] **Step 2: Viết service**

```php
<?php

namespace Modules\Finance\Services;

use Illuminate\Http\Request;
use Modules\Finance\Entities\BillIncome\BillIncome;
use Modules\Finance\Entities\BillIncome\BillIncomeDetail;
use Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest;

/**
 * Đọc + lọc danh sách phiếu thu. Port ERP `BillIncome::searchByFilter()` (:167-275).
 *
 * 4 chế độ mirror `_type` + `type` của ERP:
 *   my       -> ERP `_type=index`      : chỉ phiếu mình lập
 *   all      -> ERP `_type=all`        : theo quyền, ẩn phiếu nháp của người khác
 *   pending  -> ERP `type=for-approved`: chờ duyệt, cùng công ty
 *   approved -> ERP `type=approved`    : phiếu chính mình đã duyệt
 */
class BillIncomeService
{
    public function searchByFilter(Request $request, string $mode = 'my')
    {
        $query = BillIncome::query()->with([
            'billIncomeRequest.employee_create.info',
            'employeeCreate.info',
            'details.customer',
        ]);

        $ctx = BillIncome::context();

        $this->applyMode($query, $mode, $ctx);
        $this->applyOrgFilters($query, $request);
        $this->applyFieldFilters($query, $request);
        $this->applySort($query, $request);

        $perPage = (int) $request->get('per_page', 10);

        return $query->paginate($perPage > 0 ? $perPage : 10);
    }

    /** Phạm vi dữ liệu theo chế độ + quyền. */
    private function applyMode($query, string $mode, array $ctx): void
    {
        $me = $ctx['employee_id'];

        if ($mode === 'all') {
            if (!$ctx['is_super_admin'] && !$ctx['view_all_company']) {
                if ($ctx['view_company'] && $ctx['company_id'] !== null) {
                    $query->where('company_id', $ctx['company_id']);
                } else {
                    $query->where('created_by', $me);
                }
            }

            // Phiếu nháp chỉ chủ nhân thấy.
            $query->where(function ($q) use ($me) {
                $q->where('status', '!=', BillIncome::STATUS_CREATING)
                    ->orWhere(function ($q1) use ($me) {
                        $q1->where('status', BillIncome::STATUS_CREATING)->where('created_by', $me);
                    });
            });

            return;
        }

        if ($mode === 'pending') {
            $query->where('status', BillIncome::STATUS_AWAITING_APPROVE);
            // ERP lọc cứng theo công ty người đăng nhập. Không xác định được công ty -> trả rỗng
            // (fail-closed), KHÔNG bỏ điều kiện.
            $query->where('company_id', $ctx['company_id'] ?? -1);

            return;
        }

        if ($mode === 'approved') {
            $query->where('approved_id', $me)->where('status', BillIncome::STATUS_APPROVED);

            return;
        }

        // mode 'my' (mặc định)
        $query->where('created_by', $me);
    }

    /** 3 ô lọc cấp tổ chức + loại thu — ERP lọc qua phiếu đề nghị, không phải qua phiếu thu. */
    private function applyOrgFilters($query, Request $request): void
    {
        $company = $request->get('company_id');
        $department = $request->get('department_id');
        $part = $request->get('part_id');
        $type = $request->get('bill_income_request_type');

        if (!$company && !$department && !$part && !$type) {
            return;
        }

        $query->whereHas('billIncomeRequest', function ($sql) use ($company, $department, $part, $type) {
            if ($company) {
                $sql->where('company_id', $company);
            }
            if ($department) {
                $sql->where('department_id', $department);
            }
            if ($part) {
                $sql->where('part_id', $part);
            }
            if ($type) {
                $sql->where('type', $type);
            }
        });
    }

    private function applyFieldFilters($query, Request $request): void
    {
        if ($code = $request->get('code')) {
            $query->where('code', 'like', '%' . $code . '%');
        }

        if ($status = $request->get('status')) {
            $query->where('status', $status);
        }

        if ($createdBy = $request->get('created_by')) {
            $query->where('created_by', $createdBy);
        }

        if ($requestCode = $request->get('code_bill_income_request')) {
            $query->whereIn('bill_income_request_id', function ($sub) use ($requestCode) {
                $sub->select('id')->from('bill_income_requests')
                    ->where('code', 'like', '%' . $requestCode . '%');
            });
        }

        if ($requester = $request->get('created_by_request')) {
            $query->whereIn('bill_income_request_id', function ($sub) use ($requester) {
                $sub->select('id')->from('bill_income_requests')->where('created_by', $requester);
            });
        }

        if ($customerId = $request->get('customer_id')) {
            $query->whereIn('id', function ($sub) use ($customerId) {
                $sub->select('parent_id')->from('bill_income_details')->where('customer_id', $customerId);
            });
        }

        if ($contractCode = $request->get('contract_code')) {
            // ERP dùng whereHasMorph 3 class. Ở đây tra thẳng theo từng bảng hợp đồng đã map để
            // không phải nạp toàn bộ morph; giữ đúng 3 loại ERP lọc.
            $parentIds = BillIncomeDetail::query()
                ->whereHasMorph('objectable', [
                    \Modules\Finance\Entities\Contract\FirmContract::class,
                    \Modules\Finance\Entities\Contract\WrServiceContract::class,
                    \Modules\Finance\Entities\Contract\OpeningContract::class,
                ], function ($sql) use ($contractCode) {
                    $sql->where('code', 'like', '%' . $contractCode . '%');
                })
                ->pluck('parent_id');

            $query->whereIn('id', $parentIds);
        }

        if ($from = $request->get('money_from')) {
            $query->where('sum_money', '>=', (float) str_replace(',', '', $from));
        }

        if ($to = $request->get('money_to')) {
            $query->where('sum_money', '<=', (float) str_replace(',', '', $to));
        }

        if ($dateFrom = $request->get('date_from')) {
            $query->whereDate('created_at', '>=', $this->toSqlDate($dateFrom));
        }

        if ($dateTo = $request->get('date_to')) {
            $query->whereDate('created_at', '<=', $this->toSqlDate($dateTo));
        }
    }

    /** FE gửi `dd/mm/yyyy`; chấp cả `yyyy-mm-dd` để gọi API bằng tay không vướng. */
    private function toSqlDate(string $value): string
    {
        if (preg_match('#^\d{2}/\d{2}/\d{4}$#', $value)) {
            return \Carbon\Carbon::createFromFormat('d/m/Y', $value)->format('Y-m-d');
        }

        return $value;
    }

    /** Sort mặc định: ngày tạo giảm dần (SRS). Chỉ cho sort cột có trong danh sách trắng. */
    private function applySort($query, Request $request): void
    {
        $allowed = ['code', 'sum_money', 'created_at'];
        $sortBy = $request->get('sort_by');
        $dir = strtolower($request->get('sort_dir', 'desc')) === 'asc' ? 'asc' : 'desc';

        if ($sortBy && in_array($sortBy, $allowed, true)) {
            $query->orderBy($sortBy, $dir);

            return;
        }

        $query->orderBy('created_at', 'desc');
    }

    /** Options cho dropdown lọc — FE lấy 1 lần cùng response danh sách. */
    public function meta(): array
    {
        return [
            'statuses' => BillIncome::STATUSES,
            'types' => BillIncomeRequest::typeForSelect(),
        ];
    }
}
```

- [x] **Step 3: Kiểm tên class hợp đồng dùng ở `contract_code`**

```bash
ls hrm-api/Modules/Finance/Entities/Contract/FirmContract.php hrm-api/Modules/Finance/Entities/Contract/WrServiceContract.php hrm-api/Modules/Finance/Entities/Contract/OpeningContract.php
```
Cả 3 phải tồn tại (đã liệt kê ở Task 2 Step 4). Nếu namespace khác thì sửa lại cho khớp.

- [x] **Step 4: Verify từng chế độ trả đúng số dòng**

```bash
php -l hrm-api/Modules/Finance/Services/BillIncomeService.php
cd hrm-api && php artisan tinker --execute="
\$svc = new Modules\Finance\Services\BillIncomeService();
\$req = new Illuminate\Http\Request();
foreach (['my','all','pending','approved'] as \$m) {
    echo \$m, ' = ', \$svc->searchByFilter(\$req, \$m)->total(), PHP_EOL;
}"
```
Kỳ vọng: chạy không lỗi, 4 dòng số. Chưa đăng nhập nên `my`/`approved` sẽ ra 0 — đúng (fail-closed), không phải bug. `pending` cũng 0 vì `company_id` null → `-1`.

- [x] **Step 5: Verify lọc theo mã + tiền chạy đúng SQL**

```bash
cd hrm-api && php artisan tinker --execute="
\$svc = new Modules\Finance\Services\BillIncomeService();
\$req = new Illuminate\Http\Request(['code' => 'PT', 'money_from' => '1000000', 'sort_by' => 'sum_money', 'sort_dir' => 'asc']);
\$p = \$svc->searchByFilter(\$req, 'all');
echo \$p->total(), ' dòng', PHP_EOL;"
```
Kỳ vọng: không lỗi SQL. Số dòng có thể 0 (chưa đăng nhập) — chỉ cần câu query không nổ.

---

### Task 5: Transformers — List + Detail Resource

**Files:**
- Create: `hrm-api/Modules/Finance/Transformers/BillIncomeResource/BillIncomeListResource.php`
- Create: `hrm-api/Modules/Finance/Transformers/BillIncomeResource/BillIncomeDetailResource.php`

**Interfaces:**
- Consumes: `BillIncome` + `BillIncomeDetail` (Task 1), `BillIncomeAccess` qua method entity (Task 3).
- Produces: 2 Resource class. `BillIncomeListResource` là **ResourceCollection** (nhận paginator) để Controller gọi `->additional([...])`; `BillIncomeDetailResource` nhận 1 model. Task 6 dùng.

- [x] **Step 1: Đọc khuôn có sẵn**

```bash
cat hrm-api/Modules/Finance/Transformers/BillIncomeRequestResource/BillIncomeRequestListResource.php
```
Bám đúng kiểu class (ResourceCollection hay JsonResource) và cách format tiền/ngày của file này.

- [x] **Step 2: Viết `BillIncomeListResource.php`**

Trả **đúng 18 khóa** trong spec §5.3. Quy tắc bắt buộc:

```php
    // Trạng thái: text + type lấy từ hằng STATUSES, KHÔNG map số -> chữ ở FE.
    'status_text' => collect(BillIncome::STATUSES)->firstWhere('id', (int) $item->status)['name'] ?? null,
    'status_type' => collect(BillIncome::STATUSES)->firstWhere('id', (int) $item->status)['type'] ?? 'danger',

    // Khách hàng lấy từ CHI TIẾT ĐẦU TIÊN (đúng ERP). Phiếu Thu NCC không có customer -> null,
    // FE in dấu gạch ngang.
    'customer_text' => $this->customerText($item),

    // Ngày BE format sẵn, FE không format lại.
    'created_at' => optional($item->created_at)->format('d/m/Y'),

    // Tiền: trả cả số thô (để sort/so sánh) và chuỗi đã format (để hiện).
    'sum_money' => (float) $item->sum_money,
    'sum_money_text' => number_format((float) $item->sum_money, 0, ',', '.'),

    // 3 cờ điều kiện hiện/ẩn nút — FE CHỈ đọc, không tự suy.
    'is_can_edit' => $item->canEdit(),
    'is_can_delete' => $item->canDelete(),
    'is_can_approve' => $item->canApprove(),
```

Helper:

```php
    private function customerText($item): ?string
    {
        $customer = optional($item->details->first())->customer;
        if (!$customer) {
            return null;
        }

        return trim(($customer->code ?? '') . ' - ' . ($customer->fullname ?? ''), ' -');
    }
```

- [x] **Step 3: Viết `BillIncomeDetailResource.php`**

Ngoài các khóa của List, thêm: `payer` · `account_dept` · `exchange_rate` · `note` · `date_accounting` (`d/m/Y`) · `is_can_view` · khối `bill_income_request` (`id`, `code`, `type`, `type_text`, `reason`, `type_money_id`, `type_money_name`, `is_foreign` = `type_money_id != 1`, `exchange_rate`, `employee_create_name`, `department_name`) · mảng `details`.

Mỗi phần tử `details`:

```php
            return [
                'id' => $d->id,
                'account_has' => $d->account_has,
                'account_name' => optional($d->accountHas)->name,
                'customer' => $d->customer ? ['id' => $d->customer->id, 'code' => $d->customer->code, 'fullname' => $d->customer->fullname] : null,
                'supplier' => $d->supplier ? ['id' => $d->supplier->id, 'code' => $d->supplier->code, 'fullname' => $d->supplier->fullname] : null,
                'employee' => $d->employee ? ['id' => $d->employee->id, 'code' => optional($d->employee->info)->code, 'fullname' => optional($d->employee->info)->fullname] : null,
                'objectable_id' => $d->objectable_id,
                'objectable_type' => $d->objectable_type,
                // Hợp đồng có thể đã bị xóa -> null, FE in dấu gạch ngang, KHÔNG được vỡ màn.
                'object_code' => optional($d->objectable)->code,
                'contract_type' => optional($d->objectable)->type,
                'is_income_begin' => (bool) $d->is_income_begin,
                'income_money_request' => (float) $d->income_money_request,
                'income_money_request_exchange' => (float) $d->income_money_request_exchange,
                'income_money_approve' => (float) $d->income_money_approve,
                'income_money_approve_exchange' => (float) $d->income_money_approve_exchange,
                'income_money_real' => (float) $d->income_money_real,
                'income_money_real_exchange' => (float) $d->income_money_real_exchange,
                'note' => $d->note,
                'product_export_requests' => $d->productExportRequests->map(function ($p) {
                    return [
                        'id' => $p->id,
                        'objectable_code' => optional($p->objectable)->code,
                        'allocated_value' => (float) $p->allocated_value,
                        'allocated_value_exchange' => (float) $p->allocated_value_exchange,
                    ];
                })->values(),
            ];
```

⚠️ `optional($d->objectable)` bọc bắt buộc: `objectable_type` không nằm trong morphMap sẽ nổ `Class not found` — bọc thêm try/catch trả `null` và `\Log::warning()` (spec §8).

- [x] **Step 4: Verify**

```bash
php -l hrm-api/Modules/Finance/Transformers/BillIncomeResource/BillIncomeListResource.php
php -l hrm-api/Modules/Finance/Transformers/BillIncomeResource/BillIncomeDetailResource.php
cd hrm-api && php artisan tinker --execute="
\$b = Modules\Finance\Entities\BillIncome\BillIncome::with(['details.customer','details.accountHas','billIncomeRequest','employeeCreate.info'])->where('status',3)->first();
echo json_encode((new Modules\Finance\Transformers\BillIncomeResource\BillIncomeDetailResource(\$b))->resolve(), JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);"
```
Kỳ vọng: in JSON đủ khối `bill_income_request` + mảng `details`, `status_text` = `Đã duyệt`, `is_can_edit` = false.

---

### Task 6: Controller `index` / `show` + routes + 2 endpoint phụ

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BillIncomeController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm 1 group, đặt cạnh group `bill-income-requests`)

**Interfaces:**
- Consumes: `BillIncomeService` (Task 4), 2 Resource (Task 5), `BillIncome` (Task 1/3).
- Produces: các endpoint `GET /v1/finance/bill-incomes`, `GET /{id}`, `GET /accounts`, `GET /search-income-requests`. Task 7/9/10 thêm method vào cùng Controller. FE Task 11-14 gọi.

- [x] **Step 1: Viết Controller (phần đọc)**

```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Modules\Finance\Entities\Account\Account;
use Modules\Finance\Entities\BillIncome\BillIncome;
use Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest;
use Modules\Finance\Services\BillIncomeService;
use Modules\Finance\Transformers\BillIncomeResource\BillIncomeDetailResource;
use Modules\Finance\Transformers\BillIncomeResource\BillIncomeListResource;

/**
 * Phiếu thu tiền (port ERP `bill_incomes`, phân hệ Tài chính).
 *
 * KHÔNG gắn middleware `checkPermission` cho route nào — cùng lý do đã ghi ở
 * `BillIncomeRequestController`: middleware chung resolve quyền qua spatie `getAllPermissions()`
 * nên bỏ sót role gán từ ERP (`model_type='App\Employee'`), người có quyền thật vẫn 403.
 * Phạm vi dữ liệu chặn trong `BillIncomeService::searchByFilter()`, quyền theo phiếu chặn bằng
 * `canView()/canEdit()/canDelete()/canApprove()` trên entity.
 */
class BillIncomeController extends ApiController
{
    private $service;

    public function __construct(BillIncomeService $service)
    {
        $this->service = $service;
    }

    /** Danh sách — 4 chế độ qua `?mode=my|all|pending|approved`. */
    public function index(Request $request)
    {
        $mode = $request->get('mode', 'my');
        if (!in_array($mode, ['my', 'all', 'pending', 'approved'], true)) {
            $mode = 'my';
        }

        // Chế độ chờ duyệt là màn của thủ quỹ -> gate bằng đúng quyền BE dùng.
        if ($mode === 'pending' && !BillIncome::isTreasurer()) {
            return $this->responseJson('Bạn không có quyền xem danh sách phiếu thu chờ duyệt', 403);
        }

        return $this->listResponse($this->service->searchByFilter($request, $mode));
    }

    public function show($id)
    {
        $bill = BillIncome::with([
            'details.customer', 'details.supplier', 'details.employee.info',
            'details.accountHas', 'details.objectable', 'details.productExportRequests',
            'billIncomeRequest.employee_create.info.department',
            'employeeCreate.info',
        ])->findOrFail($id);

        if (!$bill->canView()) {
            return $this->responseJson('Bạn không có quyền xem phiếu thu này', 403);
        }

        return new BillIncomeDetailResource($bill);
    }

    /**
     * Danh sách tài khoản cho 2 select (TK Nợ của phiếu, TK Có của từng chi tiết).
     *
     * Port ERP `Account::getAccountsForSelect()` (:230-266). KHÔNG trả về tất cả tài khoản:
     *   1. chỉ `status = 1` (đang hoạt động)
     *   2. **chỉ tài khoản LÁ** — tài khoản nào có con thì loại (ERP bỏ lv1 có lv2, bỏ lv2 có lv3).
     *      Tài khoản tổng hợp không được hạch toán trực tiếp; cho chọn là sai nguyên tắc kế toán.
     * Nhãn hiển thị `"{identify_number} - {name}"`, sắp theo `id` như ERP.
     *
     * `?include_id=` — trả kèm 1 tài khoản CỤ THỂ kể cả khi đã khóa hoặc không phải lá. Dùng cho
     * màn Sửa/Chi tiết: phiếu cũ có thể đang gắn tài khoản sau đó bị khóa, không trả kèm thì select
     * hiện rỗng và người dùng vô tình lưu đè mất giá trị cũ (quy tắc chung: dropdown chỉ liệt kê
     * mục đang hoạt động, nhưng bản ghi đang gắn mục đã khóa vẫn phải hiện đúng tên).
     */
    public function accounts(Request $request)
    {
        $all = Account::query()
            ->where('status', 1)
            ->orderBy('id')
            ->get(['id', 'identify_number', 'name', 'level', 'identify_number_parent']);

        // Tài khoản nào đang là cha của một tài khoản đang hoạt động khác thì không phải lá.
        $parentNumbers = $all->pluck('identify_number_parent')->filter()->unique()->all();

        $rows = $all->reject(function ($account) use ($parentNumbers) {
            return in_array($account->identify_number, $parentNumbers);
        })->values();

        if ($includeId = $request->get('include_id')) {
            if (!$rows->contains('id', (int) $includeId)) {
                $extra = Account::query()->find($includeId, ['id', 'identify_number', 'name', 'level', 'identify_number_parent']);
                if ($extra) {
                    $rows->prepend($extra);
                }
            }
        }

        return $this->responseJson('OK', 200, $rows->map(function ($account) {
            return [
                'id' => $account->id,
                'identify_number' => $account->identify_number,
                'name' => $account->identify_number . ' - ' . $account->name,
                'account_name' => $account->name,
            ];
        })->values());
    }

    /** Popup chọn phiếu đề nghị — CHỈ phiếu đang Chờ KT duyệt và CHƯA có phiếu thu. */
    public function searchIncomeRequests(Request $request)
    {
        $query = BillIncomeRequest::query()
            ->with('employee_create.info')
            ->where('status', BillIncomeRequest::STATUS_AWAITING_APPROVE)
            ->whereNotIn('id', function ($sub) {
                $sub->select('bill_income_request_id')->from('bill_incomes');
            });

        if ($code = $request->get('code')) {
            $query->where('code', 'like', '%' . $code . '%');
        }

        if ($createdBy = $request->get('created_by')) {
            $query->where('created_by', $createdBy);
        }

        return $this->paginatedResponse($query->orderBy('id', 'desc')->paginate((int) $request->get('per_page', 10)));
    }

    private function paginatedResponse($paginator)
    {
        return response()->json([
            'data' => $paginator->items(),
            'total' => $paginator->total(),
            'lastPage' => $paginator->lastPage(),
            'currentPage' => $paginator->currentPage(),
            'perPage' => (int) $paginator->perPage(),
        ]);
    }

    private function listResponse($items)
    {
        return (new BillIncomeListResource($items))->additional(array_merge([
            'total' => $items->total(),
            'lastPage' => $items->lastPage(),
            'currentPage' => $items->currentPage(),
            'perPage' => (int) $items->perPage(),
        ], $this->service->meta()));
    }
}
```

- [x] **Step 2: Thêm routes**

Trong `hrm-api/Modules/Finance/Routes/api.php`, ngay sau group `bill-income-requests` (dòng ~237):

```php
    // Phiếu thu tiền (bảng ERP `bill_incomes` trên DB gộp).
    // KHÔNG gắn middleware quyền — xem docblock BillIncomeController.
    Route::group(['prefix' => '/bill-incomes'], function () {
        Route::get('/', [BillIncomeController::class, 'index']);
        // 2 route TĨNH phải khai TRƯỚC /{id} để không bị route động nuốt.
        Route::get('/accounts', [BillIncomeController::class, 'accounts']);
        Route::get('/search-income-requests', [BillIncomeController::class, 'searchIncomeRequests']);
        Route::get('/{id}', [BillIncomeController::class, 'show']);
    });
```

Thêm `use Modules\Finance\Http\Controllers\V1\BillIncomeController;` vào đầu file.

- [x] **Step 3: Verify route đăng ký đúng thứ tự**

```bash
cd hrm-api && php artisan route:list --path=bill-incomes
```
Kỳ vọng: 4 route, và `accounts` + `search-income-requests` đứng **TRƯỚC** `{id}`. Nếu ngược lại → sửa thứ tự khai.

- [x] **Step 4: Verify gọi thật**

Chạy server: `cd hrm-api && php -S 127.0.0.1:8000 -t public` (nền riêng). Lấy token bằng cách user cung cấp, rồi:
```bash
curl -s -H "Authorization: Bearer <TOKEN>" "http://127.0.0.1:8000/api/v1/finance/bill-incomes?mode=all&per_page=3" | head -c 1200
curl -s -H "Authorization: Bearer <TOKEN>" "http://127.0.0.1:8000/api/v1/finance/bill-incomes/accounts" | head -c 400
```
Kỳ vọng: JSON có `data` (≤ 3 phần tử) + `total` + `statuses` + `types`. Nếu chưa có token thì **hỏi user**, đừng bịa.

⚠️ Nếu 403 ở mọi màn: nhớ tài khoản dev có thể **0 quyền** — đừng nghi code, đừng bơm quyền vào store; nhờ user cấp quyền hoặc test bằng tài khoản Super admin.

---

## Phase 2 — Backend ghi dữ liệu (Task 7-10)

### Task 7: FormRequest + `BillIncomeWriteService` (tạo / sửa / xóa nháp)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Requests/BillIncome/BillIncomeStoreRequest.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillIncome/BillIncomeUpdateRequest.php`
- Create: `hrm-api/Modules/Finance/Services/BillIncomeWriteService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillIncomeController.php` (thêm `store`/`update`/`destroy`)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm 3 route)

**Interfaces:**
- Consumes: `BillIncome`, `BillIncomeDetail`, `BillIncomeDetailProductExportRequest` (Task 1).
- Produces: `BillIncomeWriteService::store(array $data): BillIncome`, `::update(BillIncome $bill, array $data): BillIncome`, `::destroy(BillIncome $bill): void`, `::syncDetails(BillIncome $bill, array $details): float` (trả `sum_money`). Task 9 dùng lại `syncDetails`.

- [x] **Step 1: Viết `BillIncomeStoreRequest.php`**

```php
<?php

namespace Modules\Finance\Http\Requests\BillIncome;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Port ERP `BillIncomeStoreRequest` + siết thêm.
 * ERP bản Update thiếu `payer` và thiếu `min:0` -> HRM cho 2 bản giống nhau.
 */
class BillIncomeStoreRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'bill_income_request_id' => 'required|exists:bill_income_requests,id',
            'account_dept' => 'required|exists:accounts,id',
            'payer' => 'required|max:255',
            'exchange_rate' => 'required|numeric|min:0',
            'status' => 'required|in:1,2',
            'note' => 'nullable|max:1000',
            'details' => 'required|array|min:1',
            'details.*.account_has' => 'required|exists:accounts,id',
            'details.*.income_money_approve' => 'required|numeric|min:0',
        ];
    }

    public function messages()
    {
        return [
            'bill_income_request_id.required' => 'Bắt buộc nhập',
            'bill_income_request_id.exists' => 'Không tồn tại',
            'account_dept.required' => 'Bắt buộc nhập',
            'account_dept.exists' => 'Không tồn tại',
            'payer.required' => 'Bắt buộc nhập',
            'exchange_rate.required' => 'Bắt buộc nhập',
            'exchange_rate.numeric' => 'Phải là số',
            'details.required' => 'Bắt buộc nhập',
            'details.array' => 'Phải là mảng',
            'details.*.account_has.required' => 'Bắt buộc nhập',
            'details.*.account_has.exists' => 'Không tồn tại',
            'details.*.income_money_approve.required' => 'Bắt buộc nhập',
            'details.*.income_money_approve.numeric' => 'Phải là số',
        ];
    }
}
```

- [x] **Step 2: Viết `BillIncomeUpdateRequest.php`**

Nội dung **y hệt** Store (class name đổi thành `BillIncomeUpdateRequest`, docblock ghi rõ vì sao trùng: ERP tách 2 bản nhưng bản Update thiếu rule và có bug `$this->status = 4` gán thay vì so sánh — HRM cho 2 bản đồng nhất).

- [x] **Step 3: Viết `BillIncomeWriteService.php`**

```php
<?php

namespace Modules\Finance\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use Modules\Finance\Entities\BillIncome\BillIncome;
use Modules\Finance\Entities\BillIncome\BillIncomeDetail;
use Modules\Finance\Entities\BillIncome\BillIncomeDetailProductExportRequest;

/**
 * Ghi phiếu thu: tạo / sửa / xóa nháp. Port ERP `BillIncomeController::store/update/delete`
 * + `BillIncome::syncDetails()`.
 *
 * KHÔNG bắt `ValidationException` — để bay lên FE nhận 422 chuẩn (ERP catch `Exception` chung
 * nên nuốt mất, FE chỉ thấy "Thêm phiếu thu thất bại!").
 */
class BillIncomeWriteService
{
    public function store(array $data): BillIncome
    {
        return DB::transaction(function () use ($data) {
            $this->guardOneBillPerRequest($data['bill_income_request_id'], null);

            $bill = BillIncome::create(array_merge($data, [
                'code' => BillIncome::generateCode(),
                'sum_money' => 0,
            ]));

            $sum = $this->syncDetails($bill, $data['details']);
            $bill->sum_money = $sum;
            $bill->save();

            return $bill->refresh();
        });
    }

    public function update(BillIncome $bill, array $data): BillIncome
    {
        return DB::transaction(function () use ($bill, $data) {
            $this->guardOneBillPerRequest($data['bill_income_request_id'], $bill->id);

            $sum = $this->syncDetails($bill, $data['details']);
            $bill->fill($data);
            $bill->sum_money = $sum;
            $bill->save();

            return $bill->refresh();
        });
    }

    public function destroy(BillIncome $bill): void
    {
        DB::transaction(function () use ($bill) {
            $detailIds = BillIncomeDetail::where('parent_id', $bill->id)->pluck('id');
            BillIncomeDetailProductExportRequest::whereIn('bill_income_detail_id', $detailIds)->delete();
            BillIncomeDetail::whereIn('id', $detailIds)->delete();
            $bill->delete();
        });
    }

    /**
     * Xóa sạch chi tiết cũ rồi tạo lại, trả tổng `sum_money`.
     * Port ERP `BillIncome::syncDetails()` (:305-358).
     *
     * ⚠️ `sum_money` ĐỔI CÔNG THỨC THEO TRẠNG THÁI (ERP :347-351):
     *   status 1 hoặc 2 -> cộng `income_money_approve_exchange` (số duyệt thu)
     *   status 3        -> cộng `income_money_real_exchange`    (số thực thu)
     * Đây là cột mà màn danh sách hiện ở ô "Số tiền" và 2 ô lọc tiền từ/đến dùng. Cộng nhầm vế
     * thì phiếu đã duyệt hiện số duyệt thay vì số thực thu, và lọc theo tiền lệch theo.
     */
    public function syncDetails(BillIncome $bill, array $details): float
    {
        $oldIds = BillIncomeDetail::where('parent_id', $bill->id)->pluck('id');
        BillIncomeDetailProductExportRequest::whereIn('bill_income_detail_id', $oldIds)->delete();
        BillIncomeDetail::whereIn('id', $oldIds)->delete();

        $sum = 0.0;

        foreach ($details as $detail) {
            $row = BillIncomeDetail::create([
                'parent_id' => $bill->id,
                'account_has' => $detail['account_has'],
                'customer_id' => $detail['customer_id'] ?? null,
                'supplier_id' => $detail['supplier_id'] ?? null,
                'employee_id' => $detail['employee_id'] ?? null,
                'objectable_id' => $detail['objectable_id'] ?? null,
                'objectable_type' => $detail['objectable_type'] ?? null,
                'income_money_request' => $detail['income_money_request'] ?? 0,
                'income_money_request_exchange' => $detail['income_money_request_exchange'] ?? 0,
                'income_money_approve' => $detail['income_money_approve'] ?? 0,
                'income_money_approve_exchange' => $detail['income_money_approve_exchange'] ?? 0,
                'income_money_real' => $detail['income_money_real'] ?? 0,
                'income_money_real_exchange' => $detail['income_money_real_exchange'] ?? 0,
                'is_income_begin' => $detail['is_income_begin'] ?? 0,
                'note' => $detail['note'] ?? null,
            ]);

            // Vế cộng đổi theo trạng thái phiếu — xem docblock.
            $sum += (int) $bill->status === BillIncome::STATUS_APPROVED
                ? (float) ($detail['income_money_real_exchange'] ?? $detail['income_money_real'] ?? 0)
                : (float) ($detail['income_money_approve_exchange'] ?? $detail['income_money_approve'] ?? 0);

            foreach ($detail['product_export_requests'] ?? [] as $per) {
                BillIncomeDetailProductExportRequest::create([
                    'bill_income_detail_id' => $row->id,
                    'product_export_request_id' => $per['product_export_request_id'] ?? null,
                    'objectable_id' => $per['objectable_id'] ?? null,
                    'objectable_type' => $per['objectable_type'] ?? null,
                    // 2 cột NOT NULL — mặc định '' và 0 chứ KHÔNG để null.
                    'objectable_code' => $per['objectable_code'] ?? '',
                    'sum_amount_allocated_after_vat' => $per['sum_amount_allocated_after_vat'] ?? 0,
                    'allocated_value' => $per['allocated_value'] ?? 0,
                    'allocated_value_exchange' => $per['allocated_value_exchange'] ?? 0,
                ]);
            }
        }

        return $sum;
    }

    /**
     * 1 phiếu đề nghị chỉ lập được 1 phiếu thu (ERP kiểm ở Controller, HRM gom về đây).
     *
     * ⚠️ KHÓA DÒNG PHIẾU ĐỀ NGHỊ TRƯỚC KHI KIỂM. Bảng `bill_incomes` KHÔNG có unique index trên
     * `bill_income_request_id` (đã kiểm: chỉ có PRIMARY và unique `code`), nên `exists()` rồi
     * `create()` để trống một khoảng: 2 kế toán bấm Lưu cùng lúc thì request thứ 2 vượt qua
     * `exists()` trước khi request thứ 1 commit → sinh 2 phiếu thu cho cùng 1 đề nghị.
     * Hậu quả không dừng ở dữ liệu rác: tới bước duyệt, MỖI phiếu ghi 1 bộ bút toán vào sổ cái
     * dùng chung với ERP, và chốt "chặn duyệt lại" ở Task 9 KHÔNG cứu được vì nó khoá theo từng
     * phiếu, còn đây là 2 phiếu khác nhau.
     * `lockForUpdate()` của `generateCode()` chỉ serialize việc sinh mã, không serialize guard này.
     */
    private function guardOneBillPerRequest($requestId, $exceptBillId): void
    {
        // Khoá dòng phiếu đề nghị -> request thứ 2 phải chờ request thứ 1 commit rồi mới đọc.
        DB::table('bill_income_requests')->where('id', $requestId)->lockForUpdate()->value('id');

        $exists = BillIncome::where('bill_income_request_id', $requestId)
            ->when($exceptBillId, function ($q) use ($exceptBillId) {
                $q->where('id', '!=', $exceptBillId);
            })
            ->exists();

        if ($exists) {
            throw ValidationException::withMessages([
                'bill_income_request_id' => 'Đề nghị thu tiền đã lập phiếu thu tiền',
            ]);
        }
    }
}
```

- [x] **Step 4: Thêm 3 method vào Controller**

```php
    public function store(BillIncomeStoreRequest $request, BillIncomeWriteService $writer)
    {
        // Gate quyền lập phiếu thu. ERP gate ở màn `create`/`edit` bằng
        // `checkPermission:Kế toán thanh toán` (web.php:6530, :6532) nên thực tế chỉ kế toán vào
        // được form; HRM là API nên phải gate ngay tại endpoint ghi — defense-in-depth, không dựa
        // vào việc FE ẩn nút. Spec §4.1: "Kế toán thanh toán → tạo/sửa phiếu thu".
        if (!BillIncomeRequest::isAccountant()) {
            return $this->responseJson('Bạn không có quyền lập phiếu thu', 403);
        }

        $bill = $writer->store($request->validated());

        $message = $bill->status == BillIncome::STATUS_AWAITING_APPROVE
            ? 'Phiếu thu tiền tạo thành công! Phiếu thu tiền cần được duyệt trước khi có hiệu lực, vui lòng theo dõi thông báo'
            : 'Thêm phiếu thu tiền thành công!';

        return $this->responseJson($message, 200, ['id' => $bill->id]);
    }

    public function update(BillIncomeUpdateRequest $request, $id, BillIncomeWriteService $writer)
    {
        $bill = BillIncome::findOrFail($id);

        // Cùng gate với store() — xem docblock ở đó.
        if (!BillIncomeRequest::isAccountant()) {
            return $this->responseJson('Bạn không có quyền sửa phiếu thu', 403);
        }

        // Bản ghi đã khóa -> 423 LOCKED (ERP cho sửa thoải mái).
        if (!$bill->canEdit()) {
            return $this->responseJson('Phiếu thu đã gửi duyệt hoặc đã duyệt, không sửa được', 423);
        }

        $writer->update($bill, $request->validated());

        return $this->responseJson('Cập nhật phiếu thu tiền thành công!', 200, ['id' => $bill->id]);
    }

    public function destroy($id, BillIncomeWriteService $writer)
    {
        $bill = BillIncome::findOrFail($id);

        // ERP `delete()` xóa thẳng, không kiểm quyền lẫn trạng thái.
        if (!$bill->canDelete()) {
            return $this->responseJson('Phiếu thu đã gửi duyệt hoặc đã duyệt, không xóa được', 423);
        }

        if ($bill->created_by != auth()->id() && !BillIncome::context()['is_super_admin']) {
            return $this->responseJson('Bạn không có quyền xóa phiếu thu này', 403);
        }

        $writer->destroy($bill);

        return $this->responseJson('Xóa phiếu thu thành công!');
    }
```

Thêm import `BillIncomeStoreRequest`, `BillIncomeUpdateRequest`, `BillIncomeWriteService`.

- [x] **Step 5: Thêm route**

```php
        Route::post('/', [BillIncomeController::class, 'store']);
        Route::put('/{id}', [BillIncomeController::class, 'update']);
        Route::delete('/{id}', [BillIncomeController::class, 'destroy']);
```

- [x] **Step 5b: Gate `searchIncomeRequests()` (sửa method của Task 6)**

Method này liệt kê mã phiếu / người lập / số tiền của mọi phiếu đề nghị đang chờ duyệt. Bên ERP dữ liệu tương đương chỉ tới được qua màn `create` vốn đã gate `checkPermission:Kế toán thanh toán`; bản HRM hiện để auth-only nên **mọi nhân viên đăng nhập đều xem được**. Đây là popup chỉ dùng khi lập phiếu thu → gate cùng quyền với `store()`:

```php
    public function searchIncomeRequests(Request $request)
    {
        // Popup này chỉ phục vụ luồng lập phiếu thu -> cùng gate với store()/update().
        // ERP đạt hiệu quả tương đương bằng cách gate màn `create` (web.php:6530).
        if (!BillIncomeRequest::isAccountant()) {
            return $this->responseJson('Bạn không có quyền xem danh sách phiếu đề nghị thu', 403);
        }

        // ... phần thân giữ nguyên như Task 6 ...
    }
```

⚠️ Chỉ thêm đúng khối gate này, **không sửa gì khác** trong method — phần thân đã được review và duyệt ở Task 6.

- [x] **Step 6: Verify tạo → sửa → xóa 1 phiếu thật rồi dọn sạch**

```bash
php -l hrm-api/Modules/Finance/Services/BillIncomeWriteService.php
cd hrm-api && php artisan tinker --execute="
DB::beginTransaction();
\$req = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest::whereNotIn('id', function(\$q){ \$q->select('bill_income_request_id')->from('bill_incomes'); })->where('status',2)->first();
if (!\$req) { echo 'KHONG CO PHIEU DE NGHI TRONG -> bỏ qua, báo user', PHP_EOL; DB::rollBack(); return; }
\$w = new Modules\Finance\Services\BillIncomeWriteService();
\$acc = Modules\Finance\Entities\Account\Account::first()->id;
\$b = \$w->store(['bill_income_request_id'=>\$req->id,'account_dept'=>\$acc,'payer'=>'TEST','exchange_rate'=>1,'status'=>1,'details'=>[['account_has'=>\$acc,'income_money_approve'=>1000,'income_money_approve_exchange'=>1000]]]);
echo 'code=', \$b->code, ' sum=', \$b->sum_money, ' details=', \$b->details()->count(), PHP_EOL;
\$w->destroy(\$b);
echo 'sau xoa: ', Modules\Finance\Entities\BillIncome\BillIncome::where('id',\$b->id)->count(), PHP_EOL;
DB::rollBack();
echo 'ROLLBACK xong', PHP_EOL;"
```
Kỳ vọng: mã dạng `xxx.PT{mmyy}.00001`, `sum=1000`, `details=1`, sau xóa `0`, và **ROLLBACK** nên DB không đổi.

- [x] **Step 7: Verify chặn 1-đề-nghị-1-phiếu**

Chạy lại lệnh trên nhưng gọi `store()` 2 lần với cùng `$req->id`. Kỳ vọng: lần 2 ném `ValidationException` với message `Đề nghị thu tiền đã lập phiếu thu tiền`. Nhớ `DB::rollBack()`.

- [x] **Step 8: Verify baseline chưa đổi**

Chạy lại lệnh đếm ở Task 1 Step 2 — 4 con số phải **y hệt**.

---

### Task 8: `buildEntries()` — dựng bút toán, hàm thuần + unit test (task lõi)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillIncomeAccountingService.php`
- Create: `hrm-api/tests/Unit/BillIncomeEntriesTest.php`

**Interfaces:**
- Consumes: hằng `AccountDetailEntry::TYPE_DEBT` / `TYPE_HAS` (Task 2).
- Produces: `BillIncomeAccountingService::buildEntries(array $input): array` trả `['entries' => [...], 'refs' => [...]]`; `::persist(array $built, int $billId): int` (trả số dòng sổ cái đã ghi); `::syncIncomeMoneyReal(int $requestId, array $details): void`. Task 9 gọi cả 3.

**Bối cảnh bắt buộc đọc trước khi code:** spec §5.6 + §5.6.1, và ERP `App\Model\IncomeExpenditure\BillIncome::saveAccountsDetail()` (:395-500) + `App\Model\Accounting\AccountDetail::boot()` (:134-232). Đây là chỗ **ghi vào sổ cái thật dùng chung với ERP** — sai là lệch số liệu kế toán, không hoàn tác được.

- [x] **Step 1: Chốt hình dạng `$input` (viết vào docblock trước khi code)**

```
$input = [
  'bill'    => ['id','code','date_accounting','account_dept','exchange_rate'],
  'request' => ['type','type_money_id','exchange_rate'],
  'creator' => ['id','company_id','department_id','part_id'],   // người tạo PHIẾU THU (chỉ là fallback)
  'account_identify_numbers' => [account_id => identify_number],
  'details' => [[
      'account_has','customer_id','supplier_id','employee_id',
      'objectable_id','objectable_type','is_income_begin',
      'income_money_real','income_money_real_exchange',
      'contractable' => ['code','type','company_id','department_id','part_id','created_by','customer_id'] | null,
      // Người tạo HỢP ĐỒNG + đơn vị tổ chức của họ. ERP ưu tiên người này hơn người tạo phiếu thu
      // cho cả `created_by` lẫn 3 cột org (AccountDetail.php:142-145, 172). Null khi không có hợp đồng.
      'contract_creator' => ['id','company_id','department_id','part_id'] | null,
      'declare_debt_beginning_id' => int|null,   // chỉ dùng khi is_income_begin
      'product_export_requests' => [['allocated_value','allocated_value_exchange','billable_id','billable_type']],
  ]],
]
```

Việc tra DB (`accounts`, `contractable`, `ImplementEmployee`, `DeclareDebtBeginning`, chuỗi `ProductExportRequest → WarehouseExportRequest → WarehouseExport → ProductExport`) làm ở **Task 9**, không nằm trong hàm thuần này.

- [x] **Step 2: Viết test trước**

Tạo `hrm-api/tests/Unit/BillIncomeEntriesTest.php`:

```php
<?php

namespace Tests\Unit;

use Modules\Finance\Services\BillIncomeAccountingService;
use PHPUnit\Framework\TestCase;

/**
 * Unit test phần dựng bút toán của phiếu thu — hàm thuần, không DB.
 * Đối chiếu 1:1 với ERP `BillIncome::saveAccountsDetail()` + hook `AccountDetail::created`.
 */
class BillIncomeEntriesTest extends TestCase
{
    private function input(array $detailOverrides = [], array $billOverrides = []): array
    {
        return [
            'bill' => array_merge([
                'id' => 555,
                'code' => 'TPE.PT0826.00017',
                'date_accounting' => '2026-08-18',
                'account_dept' => 12,
                'exchange_rate' => 1,
            ], $billOverrides),
            'request' => ['type' => 1, 'type_money_id' => 1, 'exchange_rate' => 1],
            'creator' => ['id' => 100, 'company_id' => 9, 'department_id' => 50, 'part_id' => 60],
            'account_identify_numbers' => [12 => '1111', 34 => '1311'],
            'details' => [array_merge([
                'account_has' => 34,
                'customer_id' => 77,
                'supplier_id' => null,
                'employee_id' => null,
                'objectable_id' => 888,
                'objectable_type' => 'App\Model\Sale\Firm\Contract\FirmContract',
                'is_income_begin' => 0,
                'income_money_real' => 15000000,
                'income_money_real_exchange' => 15000000,
                'contractable' => [
                    'code' => 'HD-001', 'type' => 2, 'company_id' => 3,
                    'department_id' => 30, 'part_id' => 31,
                    'created_by' => 200, 'customer_id' => 77,
                ],
                'contract_creator' => [
                    'id' => 200, 'company_id' => 3, 'department_id' => 30, 'part_id' => 31,
                ],
                'declare_debt_beginning_id' => null,
                'product_export_requests' => [],
            ], $detailOverrides)],
        ];
    }

    private function build(array $input): array
    {
        return (new BillIncomeAccountingService())->buildEntries($input);
    }

    /**
     * 1 chi tiết -> 1 dòng Có + 1 dòng Nợ + **2 ref** (đối ứng đi cả 2 chiều).
     * Ref của dòng Có trỏ `account_dept`; ref của dòng Nợ trỏ `account_has` (ERP :471-474, :487-497).
     */
    public function test_one_detail_produces_two_entries_and_two_refs(): void
    {
        $out = $this->build($this->input());

        $this->assertCount(2, $out['entries']);
        $this->assertCount(2, $out['refs']);

        // ref chiều Có -> tài khoản Nợ của phiếu
        $this->assertSame(0, $out['refs'][0]['entry_index']);
        $this->assertSame(12, $out['refs'][0]['account_ref_id']);

        // ref chiều Nợ -> tài khoản Có của chi tiết
        $this->assertSame(1, $out['refs'][1]['entry_index']);
        $this->assertSame(34, $out['refs'][1]['account_ref_id']);
    }

    /** Dòng Nợ sinh 1 ref cho MỖI `account_has` riêng biệt, không phải mỗi chi tiết. */
    public function test_debit_refs_are_distinct_per_account_has(): void
    {
        $input = $this->input();
        // 3 chi tiết nhưng chỉ 2 tài khoản Có riêng biệt (34, 34, 56).
        $input['details'][] = array_merge($input['details'][0], ['account_has' => 34]);
        $input['details'][] = array_merge($input['details'][0], ['account_has' => 56]);
        $input['account_identify_numbers'][56] = '1312';

        $out = $this->build($input);

        $debitIndex = count($out['entries']) - 1;
        $debitRefs = array_values(array_filter($out['refs'], function ($ref) use ($debitIndex) {
            return $ref['entry_index'] === $debitIndex;
        }));

        $this->assertCount(2, $debitRefs);
        $this->assertSame([34, 56], array_column($debitRefs, 'account_ref_id'));
    }

    /**
     * Vòng lặp ref của dòng Nợ chạy qua TOÀN BỘ chi tiết, kể cả chi tiết 0 đồng đã bị bỏ qua
     * khi sinh dòng Có — giữ đúng hành vi ERP (`foreach ($details ...)` trên collection đầy đủ).
     */
    public function test_debit_refs_include_zero_money_details(): void
    {
        $input = $this->input();
        $input['details'][] = array_merge($input['details'][0], [
            'account_has' => 99,
            'income_money_real' => 0,
            'income_money_real_exchange' => 0,
        ]);

        $out = $this->build($input);

        // 1 dòng Có (chi tiết 0 đồng bị bỏ) + 1 dòng Nợ
        $this->assertCount(2, $out['entries']);
        // nhưng ref chiều Nợ vẫn có cả tài khoản 99
        $this->assertContains(99, array_column($out['refs'], 'account_ref_id'));
    }

    public function test_credit_entry_fields(): void
    {
        $credit = $this->build($this->input())['entries'][0];

        $this->assertSame(34, $credit['account_id']);
        $this->assertSame(2, $credit['type']);                       // TYPE_HAS
        $this->assertSame('1311', $credit['identify_number']);
        $this->assertEquals(15000000, $credit['money_value']);
        $this->assertSame(555, $credit['invoiceable_id']);
        $this->assertSame('App\Model\IncomeExpenditure\BillIncome', $credit['invoiceable_type']);
        $this->assertSame('TPE.PT0826.00017', $credit['invoiceable_code']);
        $this->assertSame('2026-08-18', $credit['invoiceable_date_accounting']);
        $this->assertSame(888, $credit['contractable_id']);
        $this->assertSame('HD-001', $credit['contractable_code']);
        $this->assertSame(1, $credit['invoice_type']);               // request.type
        $this->assertSame(200, $credit['contract_created_by']);
        $this->assertSame(77, $credit['contract_customer_id']);
        $this->assertNull($credit['billable_id']);
        $this->assertNull($credit['billable_type']);
    }

    /**
     * Đơn vị tổ chức ưu tiên của HỢP ĐỒNG, và `created_by` là NGƯỜI TẠO HỢP ĐỒNG (200)
     * chứ KHÔNG phải người lập phiếu thu (100) — ERP AccountDetail.php:142,172.
     */
    public function test_org_and_creator_come_from_contract_first(): void
    {
        $credit = $this->build($this->input())['entries'][0];

        $this->assertSame(3, $credit['company_id']);
        $this->assertSame(30, $credit['department_id']);
        $this->assertSame(31, $credit['part_id']);
        $this->assertSame(200, $credit['created_by']);
    }

    /** Hợp đồng thiếu cột org -> fallback theo info của NGƯỜI TẠO HỢP ĐỒNG, không phải người lập phiếu. */
    public function test_org_falls_back_to_contract_creator_not_bill_creator(): void
    {
        $credit = $this->build($this->input([
            'contractable' => [
                'code' => 'HD-001', 'type' => 2,
                'company_id' => null, 'department_id' => null, 'part_id' => null,
                'created_by' => 200, 'customer_id' => 77,
            ],
        ]))['entries'][0];

        $this->assertSame(3, $credit['company_id']);
        $this->assertSame(30, $credit['department_id']);
        $this->assertSame(31, $credit['part_id']);
        $this->assertSame(200, $credit['created_by']);
    }

    /** Không có hợp đồng -> rơi hẳn về người lập phiếu thu. */
    public function test_falls_back_to_bill_creator_when_no_contract(): void
    {
        $credit = $this->build($this->input([
            'contractable' => null,
            'contract_creator' => null,
        ]))['entries'][0];

        $this->assertSame(9, $credit['company_id']);
        $this->assertSame(50, $credit['department_id']);
        $this->assertSame(60, $credit['part_id']);
        $this->assertSame(100, $credit['created_by']);
        $this->assertNull($credit['contractable_code']);
    }

    /** `contract_type` CHỈ điền khi hợp đồng là FirmContract. */
    public function test_contract_type_only_for_firm_contract(): void
    {
        $firm = $this->build($this->input())['entries'][0];
        $this->assertSame(2, $firm['contract_type']);

        $other = $this->build($this->input([
            'objectable_type' => 'App\Model\Accounting\OpeningContract',
        ]))['entries'][0];
        $this->assertNull($other['contract_type']);
    }

    /** customer_id <-> supplier_id soi gương. */
    public function test_customer_supplier_mirror(): void
    {
        $fromCustomer = $this->build($this->input())['entries'][0];
        $this->assertSame(77, $fromCustomer['customer_id']);
        $this->assertSame(77, $fromCustomer['supplier_id']);

        $fromSupplier = $this->build($this->input([
            'customer_id' => null, 'supplier_id' => 42,
        ]))['entries'][0];
        $this->assertSame(42, $fromSupplier['customer_id']);
        $this->assertSame(42, $fromSupplier['supplier_id']);
    }

    public function test_debit_entry_totals_all_details(): void
    {
        $input = $this->input();
        $input['details'][] = array_merge($input['details'][0], [
            'income_money_real' => 5000000,
            'income_money_real_exchange' => 5000000,
        ]);

        $out = $this->build($input);

        $this->assertCount(3, $out['entries']);          // 2 Có + 1 Nợ
        // 2 ref chiều Có + 1 ref chiều Nợ (2 chi tiết cùng account_has 34 -> 1 ref distinct)
        $this->assertCount(3, $out['refs']);
        $debit = end($out['entries']);
        $this->assertSame(1, $debit['type']);            // TYPE_DEBT
        $this->assertSame(12, $debit['account_id']);
        $this->assertEquals(20000000, $debit['money_value']);
    }

    /** Chi tiết 0 đồng bị bỏ qua hoàn toàn — mirror `continue` của ERP. */
    public function test_zero_money_detail_is_skipped(): void
    {
        $out = $this->build($this->input([
            'income_money_real' => 0, 'income_money_real_exchange' => 0,
        ]));

        // Không có dòng nào -> cũng không có dòng Nợ, nên không có ref chiều Nợ.
        $this->assertSame([], $out['entries']);
        $this->assertSame([], $out['refs']);
    }

    /** Nhánh phân bổ theo phiếu xuất hàng: 1 dòng sổ cái cho MỖI phần tử, không phải 1 cho cả chi tiết. */
    public function test_product_export_allocation_branch(): void
    {
        $out = $this->build($this->input([
            'product_export_requests' => [
                ['allocated_value' => 9000000, 'allocated_value_exchange' => 9000000, 'billable_id' => 11, 'billable_type' => 'App\Model\Warehouse\ProductExport'],
                ['allocated_value' => 6000000, 'allocated_value_exchange' => 6000000, 'billable_id' => null, 'billable_type' => null],
            ],
        ]));

        $this->assertCount(3, $out['entries']);          // 2 Có + 1 Nợ
        // 2 ref chiều Có (mỗi dòng phân bổ 1 ref) + 1 ref chiều Nợ
        $this->assertCount(3, $out['refs']);
        $this->assertEquals(9000000, $out['entries'][0]['money_value']);
        $this->assertSame(11, $out['entries'][0]['billable_id']);
        $this->assertEquals(6000000, $out['entries'][1]['money_value']);
        $this->assertNull($out['entries'][1]['billable_id']);
        // Dòng Nợ vẫn dùng income_money_real của chi tiết, KHÔNG cộng theo allocated_value.
        $this->assertEquals(15000000, end($out['entries'])['money_value']);
    }

    /** Nhánh thu dư nợ đầu kỳ: billable trỏ DeclareDebtBeginning. */
    public function test_income_begin_branch_sets_billable(): void
    {
        $credit = $this->build($this->input([
            'is_income_begin' => 1,
            'declare_debt_beginning_id' => 321,
        ]))['entries'][0];

        $this->assertSame(321, $credit['billable_id']);
        $this->assertSame('App\Model\Accounting\DeclareDebtBeginning', $credit['billable_type']);
    }

    /** money_value_exchange làm tròn về số nguyên (ERP `round()`). */
    public function test_exchange_is_rounded(): void
    {
        $credit = $this->build($this->input([
            'income_money_real_exchange' => 15000000.6,
        ]))['entries'][0];

        $this->assertSame(15000001.0, (float) $credit['money_value_exchange']);
    }

    /** Ngoại tệ: currency_id và exchange_rate lấy từ PHIẾU ĐỀ NGHỊ, không phải phiếu thu. */
    public function test_currency_comes_from_request(): void
    {
        $input = $this->input();
        $input['request'] = ['type' => 2, 'type_money_id' => 5, 'exchange_rate' => 25000];
        $input['bill']['exchange_rate'] = 1;

        $credit = $this->build($input)['entries'][0];

        $this->assertSame(5, $credit['currency_id']);
        $this->assertEquals(25000, $credit['exchange_rate']);
        $this->assertSame(2, $credit['invoice_type']);
    }
}
```

- [x] **Step 3: Chạy test — phải FAIL**

```bash
cd hrm-api && php vendor/bin/phpunit --filter BillIncomeEntriesTest
```
Kỳ vọng: FAIL với `Class "Modules\Finance\Services\BillIncomeAccountingService" not found`.

- [x] **Step 4: Viết `buildEntries()` + `persist()` + `syncIncomeMoneyReal()`**

```php
<?php

namespace Modules\Finance\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Modules\Finance\Entities\Accounting\AccountDetailEntry;
use Modules\Finance\Entities\Accounting\AccountDetailRef;

/**
 * Ghi bút toán sổ cái cho phiếu thu.
 *
 * Port ERP `BillIncome::saveAccountsDetail()` (:395-500) **và** hook denormalize
 * `App\Model\Accounting\AccountDetail::boot()` (:134-232) — ERP chia làm 2 chỗ, HRM gom về 1.
 *
 * `buildEntries()` là hàm THUẦN (không DB, không auth) nên unit test được — đây là cơ chế kiểm
 * chứng chính của feature, xem spec §10. `persist()` chỉ insert, không tính toán gì.
 *
 * ⚠️ Ghi vào bảng DÙNG CHUNG với cổng ERP. Sai hoặc trùng là lệch số liệu kế toán thật, không
 * hoàn tác được.
 */
class BillIncomeAccountingService
{
    const INVOICEABLE_TYPE = 'App\Model\IncomeExpenditure\BillIncome';
    const FIRM_CONTRACT_TYPE = 'App\Model\Sale\Firm\Contract\FirmContract';
    const DECLARE_DEBT_TYPE = 'App\Model\Accounting\DeclareDebtBeginning';

    /**
     * @return array{entries: array, refs: array} `refs[i]['entry_index']` trỏ vị trí dòng Có
     *                                            trong `entries` (id thật gán lúc persist).
     */
    public function buildEntries(array $input): array
    {
        $bill = $input['bill'];
        $request = $input['request'];
        $creator = $input['creator'];
        $identifyNumbers = $input['account_identify_numbers'] ?? [];

        $entries = [];
        $refs = [];
        $totalReal = 0.0;
        $totalRealExchange = 0.0;

        foreach ($input['details'] as $detail) {
            $real = (float) ($detail['income_money_real'] ?? 0);
            $realExchange = (float) ($detail['income_money_real_exchange'] ?? 0);

            // ERP: `if ($real <= 0 && $realExchange <= 0) continue;`
            if ($real <= 0 && $realExchange <= 0) {
                continue;
            }

            $totalReal += $real;
            $totalRealExchange += $realExchange;

            $allocations = $detail['product_export_requests'] ?? [];

            if (count($allocations) > 0) {
                // Nhánh A — phân bổ theo phiếu xuất hàng (0 dòng dữ liệu thật, port theo yêu cầu).
                foreach ($allocations as $allocation) {
                    $entries[] = $this->creditEntry(
                        $bill, $request, $creator, $detail, $identifyNumbers,
                        (float) ($allocation['allocated_value'] ?? 0),
                        (float) ($allocation['allocated_value_exchange'] ?? 0),
                        $allocation['billable_id'] ?? null,
                        $allocation['billable_type'] ?? null
                    );
                    $refs[] = ['entry_index' => count($entries) - 1, 'account_ref_id' => $bill['account_dept']];
                }

                continue;
            }

            // Nhánh B — nhánh thực tế của 100% dữ liệu.
            $billableId = null;
            $billableType = null;
            if (!empty($detail['is_income_begin']) && !empty($detail['declare_debt_beginning_id'])) {
                $billableId = $detail['declare_debt_beginning_id'];
                $billableType = self::DECLARE_DEBT_TYPE;
            }

            $entries[] = $this->creditEntry(
                $bill, $request, $creator, $detail, $identifyNumbers,
                $real, $realExchange, $billableId, $billableType
            );
            $refs[] = ['entry_index' => count($entries) - 1, 'account_ref_id' => $bill['account_dept']];
        }

        if ($totalReal > 0) {
            $entries[] = $this->debitEntry($bill, $request, $creator, $identifyNumbers, $totalReal, $totalRealExchange);
            $debitIndex = count($entries) - 1;

            // Dòng Nợ cũng có đối ứng, chiều ngược lại: 1 ref cho MỖI `account_has` riêng biệt
            // (ERP :487-497). Vòng lặp của ERP chạy qua TOÀN BỘ chi tiết — kể cả chi tiết 0 đồng
            // đã bị `continue` bỏ qua ở trên — nên ở đây cũng duyệt `$input['details']` gốc.
            // Kiểm chứng dữ liệu thật: 2.304/2.304 dòng Nợ của phiếu thu đều có ref.
            $seenAccounts = [];
            foreach ($input['details'] as $detail) {
                $accountHas = $detail['account_has'] ?? null;
                if ($accountHas === null || in_array($accountHas, $seenAccounts)) {
                    continue;
                }

                $seenAccounts[] = $accountHas;
                $refs[] = ['entry_index' => $debitIndex, 'account_ref_id' => $accountHas];
            }
        }

        return ['entries' => $entries, 'refs' => $refs];
    }

    private function creditEntry(array $bill, array $request, array $creator, array $detail, array $identifyNumbers, float $value, float $valueExchange, $billableId, $billableType): array
    {
        $contract = $detail['contractable'] ?? null;

        // Người tạo hợp đồng nếu có, không thì người lập phiếu thu (ERP AccountDetail.php:142).
        $employeeCreate = $detail['contract_creator'] ?? $creator;

        // customer_id <-> supplier_id soi gương (ERP hook :173-177).
        $customerId = $detail['customer_id'] ?? null;
        $supplierId = $detail['supplier_id'] ?? null;
        if ($supplierId !== null) {
            $customerId = $supplierId;
        } elseif ($customerId !== null) {
            $supplierId = $customerId;
        }

        return [
            'account_id' => $detail['account_has'],
            'identify_number' => $identifyNumbers[$detail['account_has']] ?? null,
            'customer_id' => $customerId,
            'supplier_id' => $supplierId,
            'employee_id' => $detail['employee_id'] ?? null,
            'money_value' => $value,
            'money_value_exchange' => round($valueExchange),
            'type' => AccountDetailEntry::TYPE_HAS,
            'currency_id' => $request['type_money_id'],
            'exchange_rate' => $request['exchange_rate'],
            'invoiceable_id' => $bill['id'],
            'invoiceable_type' => self::INVOICEABLE_TYPE,
            'invoiceable_code' => $bill['code'],
            'invoiceable_date_accounting' => $bill['date_accounting'],
            'invoice_type' => $request['type'],
            'contractable_id' => $detail['objectable_id'] ?? null,
            'contractable_type' => $detail['objectable_type'] ?? null,
            'contractable_code' => $contract['code'] ?? null,
            'contract_type' => ($detail['objectable_type'] ?? null) === self::FIRM_CONTRACT_TYPE
                ? ($contract['type'] ?? null)
                : null,
            'contract_created_by' => $contract['created_by'] ?? null,
            'contract_customer_id' => $contract['customer_id'] ?? null,
            // ⚠️ Người "tạo" của dòng sổ cái là NGƯỜI TẠO HỢP ĐỒNG, không phải người lập phiếu thu.
            // ERP: `$employee_create = $contractable->employee_create ?? $invoiceable->employee_create`
            // (AccountDetail.php:142), rồi `created_by = $employee_create->id` (:172) và 3 cột org
            // fallback theo `$employee_create->info` (:143-145). Kiểm chứng dữ liệu thật:
            // 7.329/7.329 dòng bên Có có hợp đồng đều thỏa `created_by = contract_created_by`.
            'company_id' => $contract['company_id'] ?? $employeeCreate['company_id'] ?? null,
            'department_id' => $contract['department_id'] ?? $employeeCreate['department_id'] ?? null,
            'part_id' => $contract['part_id'] ?? $employeeCreate['part_id'] ?? null,
            'created_by' => $employeeCreate['id'] ?? null,
            // ERP hook đổi chuỗi rỗng thành null.
            'billable_id' => $billableId ?: null,
            'billable_type' => $billableType ?: null,
            'employee_company_id' => $detail['employee_company_id'] ?? null,
            'employee_department_id' => $detail['employee_department_id'] ?? null,
            'employee_part_id' => $detail['employee_part_id'] ?? null,
        ];
    }

    private function debitEntry(array $bill, array $request, array $creator, array $identifyNumbers, float $total, float $totalExchange): array
    {
        return [
            'account_id' => $bill['account_dept'],
            'identify_number' => $identifyNumbers[$bill['account_dept']] ?? null,
            'customer_id' => null,
            'supplier_id' => null,
            'employee_id' => null,
            'money_value' => $total,
            'money_value_exchange' => round($totalExchange),
            'type' => AccountDetailEntry::TYPE_DEBT,
            'currency_id' => $request['type_money_id'],
            'exchange_rate' => $request['exchange_rate'],
            'invoiceable_id' => $bill['id'],
            'invoiceable_type' => self::INVOICEABLE_TYPE,
            'invoiceable_code' => $bill['code'],
            'invoiceable_date_accounting' => $bill['date_accounting'],
            'invoice_type' => $request['type'],
            'contractable_id' => null,
            'contractable_type' => null,
            'contractable_code' => null,
            'contract_type' => null,
            'contract_created_by' => null,
            'contract_customer_id' => null,
            'company_id' => $creator['company_id'] ?? null,
            'department_id' => $creator['department_id'] ?? null,
            'part_id' => $creator['part_id'] ?? null,
            'created_by' => $creator['id'] ?? null,
            'billable_id' => null,
            'billable_type' => null,
            'employee_company_id' => null,
            'employee_department_id' => null,
            'employee_part_id' => null,
        ];
    }

    /** Chỉ insert. Trả số dòng sổ cái đã ghi. Phải gọi trong transaction của lệnh duyệt. */
    public function persist(array $built, int $billId): int
    {
        $ids = [];

        foreach ($built['entries'] as $row) {
            $ids[] = AccountDetailEntry::create($row)->id;
        }

        foreach ($built['refs'] as $ref) {
            AccountDetailRef::create([
                'account_detail_id' => $ids[$ref['entry_index']],
                'account_ref_id' => $ref['account_ref_id'],
            ]);
        }

        Log::info('[bill-income] ghi sổ cái', [
            'bill_income_id' => $billId,
            'account_details' => count($built['entries']),
            'account_detail_refs' => count($built['refs']),
            'total' => array_sum(array_column($built['entries'], 'money_value')),
        ]);

        return count($built['entries']);
    }

    /**
     * Đẩy số thực thu ngược về chi tiết phiếu đề nghị.
     * Port ERP `BillIncome::syncIncomeMoneyReal()` (:360) — khớp theo bộ 5 khóa.
     */
    public function syncIncomeMoneyReal(int $requestId, array $details): void
    {
        foreach ($details as $detail) {
            $query = DB::table('bill_income_request_details')->where('parent_id', $requestId);

            foreach (['objectable_id', 'objectable_type', 'customer_id', 'employee_id', 'supplier_id'] as $key) {
                if (isset($detail[$key])) {
                    $query->where($key, $detail[$key]);
                }
            }

            $query->update([
                'income_money_real' => $detail['income_money_real'] ?? 0,
                'income_money_real_exchange' => $detail['income_money_real_exchange'] ?? 0,
            ]);
        }
    }
}
```

- [x] **Step 5: Chạy test — phải PASS**

```bash
cd hrm-api && php vendor/bin/phpunit --filter BillIncomeEntriesTest
```
Kỳ vọng: `OK (15 tests, ...)`. Test nào fail thì sửa `buildEntries()`, **không** sửa test cho khớp code — test là bản dịch trực tiếp của ERP.

- [x] **Step 6: Đối chiếu thủ công với bút toán ERP có thật**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "
SELECT ad.account_id, ad.type, ad.money_value, ad.money_value_exchange, ad.identify_number,
       ad.invoiceable_code, ad.invoiceable_date_accounting, ad.contractable_code, ad.contract_type,
       ad.invoice_type, ad.customer_id, ad.supplier_id, ad.company_id, ad.department_id, ad.part_id,
       ad.created_by, ad.billable_type, r.account_ref_id
FROM account_details ad
LEFT JOIN account_detail_refs r ON r.account_detail_id = ad.id
WHERE ad.invoiceable_type = 'App\\\\Model\\\\IncomeExpenditure\\\\BillIncome'
ORDER BY ad.id DESC LIMIT 6;"
```
So từng cột với những gì `buildEntries()` sinh ra cho cùng phiếu đó. **Bất kỳ cột nào ERP có giá trị mà HRM trả `null` đều là lỗi** — sửa rồi bổ sung test cho cột đó.

- [x] **Step 7: Chạy toàn bộ test suite để chắc không phá gì**

```bash
cd hrm-api && php vendor/bin/phpunit
```
Kỳ vọng: OK, không test nào đỏ.

---

### Task 9: Duyệt / Hủy phiếu — chặn duyệt lại + ghi sổ cái + thông báo

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Requests/BillIncome/BillIncomeApproveRequest.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillIncome/BillIncomeCancelRequest.php`
- Create: `hrm-api/Modules/Finance/Services/BillIncomeApprovalService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillIncomeController.php` (thêm `approve`/`cancel`)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm 2 route)
- Modify: `hrm-api/Modules/Finance/Services/BillIncomeWriteService.php` (bắn thông báo khi `status = 2`)

**Interfaces:**
- Consumes: `BillIncomeAccountingService` (Task 8), `BillIncome` + cờ quyền (Task 3), `BillIncomeRequest` (đã có).
- Produces: `BillIncomeApprovalService::approve(int $billId, array $payload): BillIncome`, `::cancel(int $billId, string $note): BillIncome`, `::collectInput(BillIncome $bill): array` (dựng `$input` cho `buildEntries`), `::detailKeys(BillIncome $bill): array` (bộ khóa khớp chi tiết cho `syncIncomeMoneyReal`). Task 10/13 dùng.

**`detailKeys()`** — mảng 1 phần tử cho mỗi chi tiết, đúng các khóa mà `syncIncomeMoneyReal()` dùng để khớp dòng bên phiếu đề nghị:

```php
    private function detailKeys(BillIncome $bill): array
    {
        return $bill->details->map(function ($d) {
            return [
                'objectable_id' => $d->objectable_id,
                'objectable_type' => $d->objectable_type,
                'customer_id' => $d->customer_id,
                'employee_id' => $d->employee_id,
                'supplier_id' => $d->supplier_id,
                'income_money_real' => (float) $d->income_money_real,
                'income_money_real_exchange' => (float) $d->income_money_real_exchange,
            ];
        })->toArray();
    }
```

⚠️ `syncIncomeMoneyReal()` chỉ thêm điều kiện `where` cho khóa nào `isset()` — khóa giá trị `null` bị bỏ qua, đúng hành vi ERP. Giữ nguyên, đừng "sửa cho chặt hơn": siết lại sẽ khớp trượt dòng và làm số thực thu không đẩy về được.

- [x] **Step 1: Viết 2 FormRequest**

`BillIncomeApproveRequest`:
```php
    public function rules()
    {
        return [
            'date_accounting' => 'nullable|date_format:d/m/Y',
            'details' => 'required|array|min:1',
            'details.*.id' => 'required|integer',
            'details.*.income_money_real' => 'required|numeric|min:0',
            'details.*.income_money_real_exchange' => 'nullable|numeric|min:0',
        ];
    }
```
`BillIncomeCancelRequest`: `['note' => 'required|max:1000']`, message `note.required => 'Bắt buộc nhập lý do hủy'`.

- [x] **Step 2: Viết `BillIncomeApprovalService.php`**

Yêu cầu bắt buộc của `approve()`, theo đúng thứ tự:

```php
    public function approve(int $billId, array $payload): BillIncome
    {
        return DB::transaction(function () use ($billId, $payload) {
            // 1. KHÓA DÒNG rồi mới đọc trạng thái — chặn 2 người duyệt cùng lúc.
            //    ERP không có bước này: duyệt 2 lần là ghi trùng bút toán vào sổ cái thật.
            $bill = BillIncome::query()->lockForUpdate()->findOrFail($billId);

            // Tách 2 nguyên nhân, KHÔNG gộp vào 1 nhánh 409: thiếu quyền và phiếu đã bị xử lý là
            // hai chuyện khác nhau. Gộp lại thì người không có quyền thủ quỹ nhận được thông báo
            // "Phiếu thu tiền đã được duyệt!" — sai sự thật và khiến họ đi tìm phiếu đã duyệt
            // không tồn tại.
            if (!BillIncome::isTreasurer()) {
                throw new HttpResponseException(
                    response()->json(['code' => 403, 'message' => 'Bạn không có quyền duyệt phiếu thu'], 403)
                );
            }

            // Kiểm lại trạng thái SAU khi đã khoá dòng — đây mới là chốt chặn duyệt lại.
            if ((int) $bill->status !== BillIncome::STATUS_AWAITING_APPROVE) {
                throw new HttpResponseException(
                    response()->json(['code' => 409, 'message' => 'Phiếu thu tiền đã được duyệt!'], 409)
                );
            }

            // 2. Ghi số thực thu vào từng chi tiết.
            foreach ($payload['details'] as $row) {
                BillIncomeDetail::where('id', $row['id'])->where('parent_id', $bill->id)->update([
                    'income_money_real' => $row['income_money_real'],
                    'income_money_real_exchange' => $row['income_money_real_exchange'] ?? $row['income_money_real'],
                ]);
            }

            // 3. Đổi trạng thái phiếu thu.
            $bill->status = BillIncome::STATUS_APPROVED;
            $bill->date_accounting = isset($payload['date_accounting'])
                ? Carbon::createFromFormat('d/m/Y', $payload['date_accounting'])->format('Y-m-d')
                : now()->format('Y-m-d');
            $bill->approved_id = auth()->id();
            $bill->save();

            // 4. Phiếu đề nghị -> Đã hạch toán.
            BillIncomeRequest::where('id', $bill->bill_income_request_id)
                ->update(['status' => BillIncomeRequest::STATUS_APPROVED]);

            // 5. Ghi sổ cái (hàm thuần dựng, hàm mỏng insert).
            $bill->refresh()->load('details.objectable', 'billIncomeRequest', 'employeeCreate.info');
            $built = $this->accounting->buildEntries($this->collectInput($bill));
            $this->accounting->persist($built, $bill->id);

            // 6. Đẩy số thực thu ngược về phiếu đề nghị.
            $this->accounting->syncIncomeMoneyReal($bill->bill_income_request_id, $this->detailKeys($bill));

            // 7. Tính lại `sum_money` theo vế THỰC THU (ERP làm việc này bằng cách gọi lại
            //    syncDetails() lúc status đã = 3 — xem docblock BillIncomeWriteService::syncDetails).
            //    Thiếu bước này thì ô "Số tiền" của phiếu đã duyệt vẫn hiện số DUYỆT THU.
            $bill->sum_money = (float) $bill->details()->sum('income_money_real_exchange');
            $bill->save();

            return $bill;
        });
    }
```

`collectInput(BillIncome $bill): array` — đây là chỗ **tra DB** để dựng `$input` đúng hình dạng đã chốt ở Task 8 Step 1:

- `account_identify_numbers`: `Account::whereIn('id', [...])->pluck('identify_number', 'id')->toArray()`
- `creator`: `$bill->employeeCreate` + `->info` (company/department/part). ERP ưu tiên `contractable->employee_create` rồi mới tới người tạo chứng từ — giữ đúng thứ tự đó.
- mỗi detail: `contractable` = `optional($detail->objectable)` → mảng 7 khóa (`code`, `type`, `company_id`, `department_id`, `part_id`, `created_by`, `customer_id`), bọc try/catch trả `null` nếu morph không resolve được
- `declare_debt_beginning_id`: chỉ tra khi `is_income_begin` — `DB::table('declare_debt_beginning')->where('customer_id', ...)->where('account_id', 22)->where('deptable_id', ...)->where('deptable_type', ...)->value('id')`
- `product_export_requests`: mỗi phần tử tra `billable` theo chuỗi ERP `ProductExportRequest → WarehouseExportRequest → WarehouseExport (mới nhất) → ProductExport`, hoặc `BorrowSellRequest → BorrowSell`; không khớp loại nào thì `billable_id = null`
- `employee_company_id` / `employee_department_id` / `employee_part_id`: chỉ tra khi `employee_id` có giá trị (tra `implement_employees` → `implement_departments` → `departments`, fallback `employee->info`)

`cancel()`: khóa dòng, kiểm `canApprove()` (cùng điều kiện), set `status = STATUS_CANCEL` + `note`, phiếu đề nghị → `BillIncomeRequest::STATUS_CANCEL`. **Không** ghi sổ cái.

- [x] **Step 3: Thêm thông báo khi gửi duyệt**

Trong `BillIncomeWriteService::store()`/`update()`, khi `status == STATUS_AWAITING_APPROVE`:
1. `BillIncomeRequest::where('id', ...)->update(['status' => BillIncomeRequest::STATUS_CREATED, 'approved_id' => auth()->id()])`
2. Bắn thông báo tới người có quyền `Thủ quỹ duyệt phiếu thu`.

**Cơ chế đã xác định sẵn (đã tra, đừng tự chế cái khác):** HRM **KHÔNG có** `NotificationHelper::sendNotifyWithPermission` của ERP. Pattern chuẩn của HRM nằm ở `Modules/Finance/Services/ProductTransferRequestService.php` — copy đúng 2 hàm `notifyAccountants()` (:547) và `sendPortalNotification()` (:583):

- Người nhận lấy bằng `ProductTransferRequest::employeeInfoIdsHavingPermission(string $permissionName, ?int $companyId): array` (:601) — **copy nguyên hàm này sang `BillIncome`**, đừng gọi chéo entity. Nó query `permissions` → `employee_has_permissions` + `role_has_permissions` → `employee_has_roles` → join `employees`/`employee_infos`, trả về mảng **`employee_info_id`** (KHÔNG phải `employee_id`).
  ⚠️ Không dùng `Employee::permission()` của spatie — trên DB gộp sẽ thiếu người được gán role từ thời ERP (model_type mismatch).
  ⚠️ `$companyId = null` nghĩa là lọc `company_id IS NULL`, không phải "mọi công ty". Truyền `$bill->company_id`.
- Gửi bằng `EmployeeInfoService::sendNotification` (Modules/Timesheet — **chỉ gọi, không sửa**). `try/catch` **từng người nhận** vì helper publish Redis trước khi ghi DB và không tự catch — 1 người lỗi không được làm rớt cả danh sách.
- Bọc toàn bộ khối notify trong `try/catch \Throwable` + `Log::error` — thông báo lỗi không được làm rớt việc lưu phiếu.
- `url` trong payload phải là **path nội bộ HRM** (`/finance/bill-incomes/{id}`) vì FE `$router.push` giá trị đó.

Nội dung theo `.claude/skills/notification-convention/SKILL.md`, tên đối tượng in đậm bằng `<b>` (FE render `v-html`):
`[TC] Chờ duyệt phiếu thu: <b>{code}</b>. Người lập: {tên}` — ≤ 50 ký tự cho tên đối tượng, tổng ≤ 120 ký tự.

- [x] **Step 4: Thêm Controller + route**

```php
    public function approve($id, BillIncomeApproveRequest $request, BillIncomeApprovalService $service)
    {
        $bill = $service->approve((int) $id, $request->validated());

        return $this->responseJson('Duyệt phiếu thu thành công!', 200, ['id' => $bill->id]);
    }

    public function cancel($id, BillIncomeCancelRequest $request, BillIncomeApprovalService $service)
    {
        $bill = $service->cancel((int) $id, $request->validated()['note']);

        return $this->responseJson('Hủy phiếu thu thành công!', 200, ['id' => $bill->id]);
    }
```
Route: `Route::post('/{id}/approve', ...)` và `Route::post('/{id}/cancel', ...)`.

- [x] **Step 5: Verify duyệt 1 phiếu thật trong transaction rồi rollback**

```bash
cd hrm-api && php artisan tinker --execute="
DB::beginTransaction();
\$before = DB::table('account_details')->count();
\$bill = Modules\Finance\Entities\BillIncome\BillIncome::where('status',2)->first();
if (!\$bill) { echo 'KHONG CO PHIEU CHO DUYET', PHP_EOL; DB::rollBack(); return; }
\$svc = app(Modules\Finance\Services\BillIncomeApprovalService::class);
\$payload = ['details' => \$bill->details->map(function(\$d){ return ['id'=>\$d->id,'income_money_real'=>\$d->income_money_approve,'income_money_real_exchange'=>\$d->income_money_approve_exchange]; })->toArray()];
\$svc->approve(\$bill->id, \$payload);
echo 'sinh them ', DB::table('account_details')->count() - \$before, ' dong so cai', PHP_EOL;
DB::rollBack();
echo 'ROLLBACK', PHP_EOL;"
```
Kỳ vọng: số dòng sinh thêm = **số chi tiết có tiền + 1**. Nếu = 0 → kiểm `income_money_real` có được ghi trước khi `buildEntries()` không.

- [x] **Step 6: Verify CHẶN DUYỆT LẠI (điểm quan trọng nhất của task)**

Trong cùng 1 transaction, gọi `approve()` **2 lần** trên cùng phiếu.
Kỳ vọng: lần 2 ném lỗi **409** với message `Phiếu thu tiền đã được duyệt!`, và số dòng `account_details` **không tăng thêm lần nữa**. Rollback.

- [x] **Step 7: Verify baseline + test suite**

```bash
cd hrm-api && php vendor/bin/phpunit
```
Rồi chạy lại lệnh đếm baseline ở Task 1 Step 2 — 4 con số phải y hệt.

---

### Task 10: In 2 liên + Xuất Excel 1 phiếu

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillIncomePrintService.php`
- Create: `hrm-api/Modules/Finance/Exports/BillIncomeExport.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillIncomeController.php` (thêm `printData`/`export`)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm 2 route)

**Interfaces:**
- Consumes: `BillIncome` (Task 1), `Modules\Finance\Entities\ErpReportTemplate` (đã có).
- Produces: `BillIncomePrintService::render(BillIncome $bill): string` (HTML 2 liên đã fill), `::fill(BillIncome $bill, int $lien): string` (fill template cho 1 liên) và `::placeholders(BillIncome $bill, int $lien): array`. Task 14 (FE `print.vue`) tiêu thụ `render()` qua endpoint.

- [x] **Step 1: Đọc pattern in đã có**

```bash
grep -n "PRINT_TEMPLATE_ID\|ErpReportTemplate\|fillReport" -A 12 hrm-api/Modules/Finance/Services/ProductTransferRequestService.php | sed -n '1,60p'
```
Bám đúng cách file này nạp template và fill placeholder (hàm `fillReport()` / `clearNull()` là helper toàn cục port từ ERP — kiểm có chưa: `grep -rn "function fillReport" hrm-api/app`). Nếu HRM **chưa** có 2 helper này thì port vào `Modules/Finance/Helpers/` và ghi rõ trong plan checkpoint.

- [x] **Step 2: Viết `BillIncomePrintService`**

Chọn mẫu:
```php
    const TEMPLATE_SELL_ONE = 203;      // Thu bán hàng, 1 khách hàng
    const TEMPLATE_SELL_MANY = 204;     // Thu bán hàng, nhiều khách hàng
    const TEMPLATE_SUPPLIER_ONE = 205;  // Thu NCC, 1 nhà cung cấp
    const TEMPLATE_SUPPLIER_MANY = 206; // Thu NCC, nhiều nhà cung cấp

    private function templateId(BillIncome $bill): int
    {
        $type = optional($bill->billIncomeRequest)->type;
        $many = $bill->details->count() > 1;

        if ($type == BillIncomeRequest::TYPE_SELL) {
            return $many ? self::TEMPLATE_SELL_MANY : self::TEMPLATE_SELL_ONE;
        }

        if ($type == BillIncomeRequest::TYPE_SUPPLIER) {
            return $many ? self::TEMPLATE_SUPPLIER_MANY : self::TEMPLATE_SUPPLIER_ONE;
        }

        // ERP không có mẫu cho loại 3 (Thu khác) -> biến $templatePrint chưa khởi tạo, in là nổ
        // ErrorException. HRM chặn trước bằng 422.
        throw ValidationException::withMessages(['type' => 'Loại thu này chưa có mẫu in']);
    }
```

Placeholder (spec §5.8): `HEADER` · `NGUOI_NOP_TIEN` · `NGUOI_DE_NGHI` · `PHONG_BAN` · `LY_DO_THU` · `KHACH_HANG` · `NHA_CUNG_CAP` · `DON_HANG_HOP_DONG` · `SO_TIEN` · `NGAY` · `THANG` · `NAM` · `CHI_TIET` · `TY_GIA` · `LIEN` · `BANG_CHU`.

Ghép 2 liên đúng ERP:
```php
        $first = $this->fill($bill, 1);
        $second = $this->fill($bill, 2);

        // 1 chi tiết -> 2 liên cùng 1 trang A4; nhiều chi tiết -> ngắt trang.
        return $bill->details->count() == 1
            ? $first . str_repeat('<br>', 9) . $second
            : $first . '<br><div class="page-break active"></div>' . $second;
```

- [x] **Step 3: Viết `BillIncomeExport`**

Port `App\ExcelExports\BillIncomeExcel` của ERP. Bộ placeholder khác bản in đúng 2 chỗ (spec §5.8): `KHACH_HANG` chỉ lấy `fullname` (không kèm mã), `NGUOI_DE_NGHI` lấy **người tạo phiếu thu** chứ không phải người đề nghị. Tên file tải về: `phieu_thu.xlsx`.

- [x] **Step 4: Controller + route**

```php
    public function printData($id, BillIncomePrintService $printer)
    {
        $bill = BillIncome::with(['details.customer', 'details.supplier', 'details.objectable', 'billIncomeRequest.employee_create.info.department', 'employeeCreate.info.company'])->findOrFail($id);

        if (!$bill->canView()) {
            return $this->responseJson('Bạn không có quyền xem phiếu thu này', 403);
        }

        return $this->responseJson('OK', 200, ['html' => $printer->render($bill), 'code' => $bill->code]);
    }
```
Route: `Route::get('/{id}/print-data', ...)`, `Route::get('/{id}/export', ...)`.

- [x] **Step 5: Verify 4 mẫu tồn tại trên DB**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT id, name FROM report_templates WHERE id IN (203,204,205,206);"
```
Kỳ vọng: đủ 4 dòng. Thiếu dòng nào → báo user, **không** tự tạo template.

- [x] **Step 6: Verify render thật**

```bash
cd hrm-api && php artisan tinker --execute="
\$b = Modules\Finance\Entities\BillIncome\BillIncome::with(['details','billIncomeRequest'])->where('status',3)->first();
\$html = app(Modules\Finance\Services\BillIncomePrintService::class)->render(\$b);
echo strlen(\$html), ' ký tự', PHP_EOL;
echo (strpos(\$html, '{') === false ? 'KHONG CON PLACEHOLDER CHUA FILL' : 'CON PLACEHOLDER - KIEM LAI'), PHP_EOL;"
```
Kỳ vọng: độ dài > 1000 và in `KHONG CON PLACEHOLDER CHUA FILL`.

- [x] **Step 7: Verify chặn loại thu 3**

Tìm 1 phiếu có `billIncomeRequest.type = 3` (nếu có) và gọi `render()` — kỳ vọng ném `ValidationException` với message `Loại thu này chưa có mẫu in`, KHÔNG nổ `ErrorException`. Không có phiếu loại 3 thì ghi rõ vào checkpoint là chưa kiểm chứng được bằng dữ liệu thật.

---

## Phase 3 — Frontend (Task 11-16)

### Task 11: Màn danh sách `index.vue` — 4 chế độ

**Files:**
- Create: `hrm-client/pages/finance/bill-incomes/index.vue`

**Interfaces:**
- Consumes: `GET /v1/finance/bill-incomes?mode=...` (Task 6).
- Produces: màn `/finance/bill-incomes`. Task 15 (menu) trỏ tới.

- [x] **Step 1: Đọc bắt buộc trước khi code**

```bash
cat .claude/skills/list-page/SKILL.md
cat .claude/skills/button-convention/SKILL.md
sed -n '1,120p' .claude/skills/erp-to-hrm-screen/references/srs-quy-tac-chung.md
```

- [x] **Step 2: Copy khuôn**

Copy `hrm-client/pages/finance/bill-income-requests/index.vue` (790 dòng) làm khuôn — file này đã theo đúng base màn Danh mục khách hàng `pages/assign/customers/index.vue`. Giữ nguyên cấu trúc `V2BaseFilterPanel` + `V2BaseDataTable` + 4 mixin.

- [x] **Step 3: Đổi 3 khóa định danh (bắt buộc, không được trùng màn khác)**

```js
columnScreenKey: 'finance_bill_incomes',
localStorageKey: `finance_bill_incomes_${this.mode}`,   // tách theo mode, 4 chế độ không đè nhau
apiPath: 'finance/bill-incomes',
```
Kiểm trùng: `grep -rn "finance_bill_incomes" hrm-client/pages` — chỉ được ra file này.

- [x] **Step 4: Khai 11 cột đúng spec §6.4**

Bắt buộc:
- STT dùng `getNumericalOrder(currentPage, pageSize, index)` — KHÔNG `index + 1` (sai từ trang 2)
- Mã phiếu và Mã phiếu đề nghị thu là `<nuxt-link>` thật (chuột phải mở tab mới được), KHÔNG `@click` trên `<div>`
- Số tiền căn **phải**; STT / Trạng thái / Hành động căn **giữa**; còn lại căn trái
- Trạng thái dùng `V2BaseBadge` với `status_text` + `status_type` từ BE — KHÔNG map số→chữ ở FE
- Ô rỗng in `—`
- STT / Mã phiếu / Hành động **không tắt được** trong Cấu hình cột

- [x] **Step 5: Khai bộ lọc + popup "Cài đặt bộ lọc"**

13 ô theo spec §6.5. Placeholder đúng dạng `Chọn <X>` / `Nhập <X>` — không `Tất cả`, không `Chọn...`, không để trống. 3 ô cấp tổ chức **chỉ hiện khi `mode === 'all'`**. Bỏ prop `title` của `V2BaseFilterPanel` (dùng mặc định "Bộ lọc danh sách").

⚠️ Ô **Khách hàng** phải dùng đúng API tìm khách hàng mà màn Đề nghị thu tiền đang dùng — `customer_id` lưu trong `bill_income_details` là **id của ERP**, id khách hàng bên HRM lệch, chọn nhầm nguồn là lọc ra 0 kết quả trong khi dữ liệu vẫn có. Tìm API đúng bằng:
```bash
grep -n "customer" hrm-client/pages/finance/bill-income-requests/index.vue | head -20
```

⚠️ Ô **Số tiền từ/đến**: gửi lên BE dạng số thô (BE có `str_replace(',', '')` nhưng đừng dựa vào đó) và nút Làm mới phải xóa cả 2 ô.

- [x] **Step 6: Watcher chế độ**

```js
    watch: {
        // PHẢI theo fullPath: 4 lối vào menu chỉ khác nhau ở query `mode`, SaleHubSidebar điều
        // hướng theo path nên watch `$route.path` sẽ không bao giờ chạy.
        '$route.fullPath'() {
            this.mode = this.$route.query.mode || 'my'
            this.currentPage = 1
            this.loadData()
        },
    },
```

- [x] **Step 7: Cờ quyền fail-closed**

```js
        data() {
            return {
                // Fail-closed: KHỞI TẠO false, chỉ set từ $store.state.permissions.
                // Cấm gán literal true ở bất kỳ đâu.
                canApprove: false,
                canViewAllCompany: false,
            }
        },
```
Điều kiện hiện nút của TỪNG DÒNG đọc cờ BE `is_can_edit` / `is_can_delete` / `is_can_approve`, KHÔNG tự suy từ status.

- [x] **Step 8: Cột hành động**

6 hành động > 3 → 2 nút chính (Sửa, Xóa) + menu "…" (Duyệt, Hủy phiếu, In, Xuất Excel).
⚠️ `V2BaseRowActions` emit **chuỗi key** → so `action === 'edit'`, KHÔNG so `action.key`.
⚠️ `V2BaseButton` không có prop `disabled` → ẩn bằng `visible`/`v-if`, không hiện xám.

- [x] **Step 9: Verify parse + icon**

hrm-client không có ESLint (Node 14) — parse bằng `vue-template-compiler` + `@babel/parser`:
```bash
cd hrm-client && node -e "
const fs=require('fs'), c=require('vue-template-compiler'), b=require('@babel/parser');
const s=fs.readFileSync('pages/finance/bill-incomes/index.vue','utf8');
const p=c.parseComponent(s);
const t=c.compile(p.template.content); if(t.errors.length){console.log('TEMPLATE LỖI',t.errors);process.exit(1)}
b.parse(p.script.content,{sourceType:'module',plugins:['optionalChaining','nullishCoalescingOperator']});
console.log('PARSE OK');"
```
Kỳ vọng: `PARSE OK`.

Mọi icon dùng phải có thật:
```bash
grep -c "^\.ri-add-line:before" hrm-client/assets/scss/custom/plugins/icons/_remixicon.scss
```

- [x] **Step 10: Rà checklist A + B của skill**

Mở `.claude/skills/erp-to-hrm-screen/SKILL.md`, tick từng dòng mục **A. Màn danh sách** và **B. Nút & hành động**. Dòng nào không đạt → sửa ngay.

---

### Task 12: Form tạo/sửa — `BillIncomeForm.vue` + popup chọn phiếu đề nghị

**Files:**
- Create: `hrm-client/pages/finance/bill-incomes/components/BillIncomeForm.vue`
- Create: `hrm-client/pages/finance/bill-incomes/components/IncomeRequestSearchModal.vue`
- Create: `hrm-client/pages/finance/bill-incomes/create.vue`
- Create: `hrm-client/pages/finance/bill-incomes/_id/edit.vue`

**Interfaces:**
- Consumes: `POST /v1/finance/bill-incomes`, `PUT /{id}`, `GET /{id}`, `GET /accounts`, `GET /search-income-requests` (Task 6/7); `GET /v1/finance/bill-income-requests/{id}` (đã có).
- Produces: component `BillIncomeForm` nhận prop `value` (object phiếu) + `mode` (`create`/`edit`), emit `input` và `submit`. Task 13 dùng lại ở chế độ chỉ đọc.

- [x] **Step 1: Đọc bắt buộc**

```bash
cat .claude/skills/modal-popup/SKILL.md
cat .claude/skills/form-validate/SKILL.md
cat .claude/skills/unsaved-changes/SKILL.md
cat .claude/skills/select-and-input-state/SKILL.md
```

- [x] **Step 2: Khuôn form**

Khuôn form chuẩn là `hrm-client/pages/assign/customers/components/CustomerForm.vue`.
⚠️ Class `form-card` / `form-header` nằm trong khối `<style>` **riêng của màn nguồn**, không có ở `v2-styles` — copy kèm style, nếu không màn sẽ mất khung.

- [x] **Step 3: Khối Thông tin chung — 10 trường theo spec §6.7**

Bắt buộc:
- "Số phiếu đề nghị": `V2BaseInput` **readonly** + nút kính lúp mở `IncomeRequestSearchModal` — KHÔNG tự chế nút
- "Tỷ giá": khóa khi `type_money_id === 1` (VND)
- 5 trường lấy từ phiếu đề nghị (Loại thu, Loại tiền, Người đề nghị, Phòng ban, Lý do thu) đều **disabled**
- Select **trong modal** bắt buộc dùng `V2BaseSelectInModal`, không dùng `V2BaseSelect`
- ⚠️ `V2BaseSelect` là select2 — **không có** prop `reduce` / `label`
- ⚠️ Không đặt prop tên `errors` hoặc `fields` — vee-validate chiếm 2 tên này, prop sẽ bị che

- [x] **Step 4: Khối Chi tiết**

Bảng cột đổi theo `bill_income_request.type` (spec §6.7). Ngoại tệ (`type_money_id !== 1`) thì mỗi cột tiền tách 2 cột con. Dòng Tổng cộng ở cuối. Chưa chọn phiếu đề nghị → hiện "Chưa chọn phiếu đề nghị thu", không render bảng.

Bảng con phân bổ (`contract_type === 3 && !is_income_begin`) và checkbox "Thu dư nợ đầu kỳ" (`contract_type === 3 && is_income_begin`, disabled) — cả 2 nhánh **không có dữ liệu thật để test**, ghi rõ vào checkpoint.

- [x] **Step 5: Validate + cảnh báo chưa lưu**

- Lỗi hiện **ngay dưới ô nhập**: viền đỏ `is-invalid` + text `invalid-feedback`, dạng `Tên trường – Nội dung lỗi`
- Flag `touched` — chỉ hiện lỗi sau lần submit đầu
- Còn lỗi thì **không gọi API**; nhiều lỗi thì focus về ô lỗi đầu tiên
- Mixin cảnh báo chưa lưu — đây là màn kiểu **"trang vỏ render component form con"**, theo bảng mục 2b của skill thì gán **NGƯỢC với trực giác**:
  - `create.vue` và `_id/edit.vue` (trang vỏ) → **`unsavedChildFormMixin`**
  - `BillIncomeForm.vue` (component con) → **`unsavedChangesMixin`**

  Lý do: `beforeRouteLeave` chỉ chạy trên component của route nên trang vỏ phải là nơi chặn, còn phần theo dõi form bẩn (snapshot + watch) nằm ở con; trang vỏ uỷ quyền `isFormDirty()` cho con. Gán ngược lại thì **popup không bao giờ hiện**.
- Gọi `markFormSaved()` sau khi lưu thành công
- Chưa đổi gì mà bấm Hủy → **không** hiện popup

- [x] **Step 6: 3 nút form**

**Lưu** (gửi `status: 1`) · **Lưu và gửi duyệt** (gửi `status: 2`) · **Quay lại**. Đặt trong `V2Footer`, không tự dựng khối nút.
⚠️ Lưu dữ liệu dùng `apiPostMethod` với khóa `payload` (không phải `apiPost`).

- [x] **Step 7: `_id/edit.vue` chặn vào phiếu đã khóa**

`asyncData`/`mounted` gọi `GET /{id}`; nếu `is_can_edit === false` thì `redirect` về `/finance/bill-incomes/{id}` (màn chi tiết). Không dựa vào việc ẩn nút ở màn danh sách.

- [x] **Step 8: Verify parse cả 4 file**

Chạy lệnh parse ở Task 11 Step 9 cho từng file. Kỳ vọng: `PARSE OK` cả 4.

---

### Task 13: Màn chi tiết + popup duyệt

**Files:**
- Create: `hrm-client/pages/finance/bill-incomes/_id/index.vue`
- Create: `hrm-client/pages/finance/bill-incomes/components/ApproveBillIncomeModal.vue`

**Interfaces:**
- Consumes: `GET /{id}` (Task 6), `POST /{id}/approve`, `POST /{id}/cancel` (Task 9); component `BillIncomeForm` ở chế độ chỉ đọc (Task 12).
- Produces: màn `/finance/bill-incomes/{id}`.

- [x] **Step 1: Bố cục**

Tiêu đề `Chi tiết phiếu thu tiền: {mã phiếu}`, số phiếu hiện ngay dưới tiêu đề. Thân màn = `BillIncomeForm` ở chế độ chỉ đọc.

- [x] **Step 2: Nút trong `V2Footer`**

**Duyệt phiếu thu** (xanh lá) · **Hủy phiếu thu** (đỏ) — cả 2 `v-if="detail.is_can_approve"` · **In** · **Xuất Excel** · **Quay lại**.
⚠️ Danh sách nút và điều kiện ẩn/hiện phải **khớp hệt màn danh sách** — cùng đọc cờ BE, không gate thêm điều kiện riêng.

- [x] **Step 3: `ApproveBillIncomeModal`**

Bảng nhập **Số tiền thực thu** cho từng chi tiết, mặc định điền sẵn `= income_money_approve`, kèm dòng tổng cập nhật theo. Submit gọi `POST /{id}/approve` với `details: [{id, income_money_real, income_money_real_exchange}]`.
Select trong modal dùng `V2BaseSelectInModal`. Xác nhận cuối dùng `$confirm()` / `base-confirm-modal`, **không** tự khai `b-modal`.

- [x] **Step 4: Popup hủy**

Ô **Lý do hủy** bắt buộc (`required`), gọi `POST /{id}/cancel`.

- [x] **Step 5: Xử lý 409**

Duyệt trả **409** (người khác vừa duyệt) → hiện toast cảnh báo với message BE trả về rồi **tải lại chi tiết**, không giữ nguyên màn cũ.

- [x] **Step 6: Xuất Excel gắn token**

Request tải file phải tự gắn header `Authorization` — `$axios` tải file thiếu token là 401. Bám cách màn đã có làm: `grep -rn "Authorization" hrm-client/utils/export/ | head`.

- [x] **Step 7: Verify parse 2 file** (lệnh ở Task 11 Step 9).

---

### Task 14: Màn in `_id/print.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-incomes/_id/print.vue`

**Interfaces:**
- Consumes: `GET /{id}/print-data` (Task 10) → `{ html, code }`.

- [x] **Step 1: Đọc bắt buộc**

```bash
cat .claude/skills/print-page/SKILL.md
cat hrm-client/pages/finance/bill-income-requests/_id/print.vue
```

- [x] **Step 2: Dựng màn**

Render `html` BE trả về (`v-html`), layout in, tự bật hộp thoại in sau khi nạp xong (không bắt user Ctrl+P).

- [x] **Step 3: Rà đúng 6 lỗi in mà skill liệt kê**

Viền phải/dưới/trên khi sang trang · nội dung cột bị cắt · mất logo/letterhead · style khác preview · bảng ô gộp vỡ khi sang trang · viền ngang khác màu.

- [x] **Step 4: Verify parse** (lệnh ở Task 11 Step 9).

---

### Task 15: Menu phân hệ Tài chính

**Files:**
- Modify: `hrm-client/components/subsystem-menu/finance.js` (4 chỗ)

- [x] **Step 1: Sửa slot xám dòng 79**

```js
            { label: 'Phiếu thu', link: '/finance/bill-incomes?mode=all' },
```

- [x] **Step 2: Thêm 1 mục vào nhóm *Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi***

```js
            // Cùng màn với mục 'Phiếu thu' của nhóm Quản lý tiền, đổi chế độ bằng query `mode`.
            { label: 'Phiếu thu của tôi', link: '/finance/bill-incomes?mode=my' },
```

- [x] **Step 3: Thêm 2 mục vào nhóm *Phê duyệt - Công nợ - Thu - Chi***

```js
            {
                label: 'Phiếu thu chờ duyệt',
                link: '/finance/bill-incomes?mode=pending',
                // Màn của thủ quỹ -> gate bằng đúng quyền BE dùng để chặn `mode=pending`.
                isShow: ['Thủ quỹ duyệt phiếu thu'],
            },
            {
                label: 'Phiếu thu đã duyệt',
                link: '/finance/bill-incomes?mode=approved',
                // KHÔNG gate: BE lọc theo `approved_id = tôi`, không duyệt phiếu nào thì rỗng.
            },
```

- [x] **Step 4: Verify parse**

```bash
cd hrm-client && node -e "require('@babel/parser').parse(require('fs').readFileSync('components/subsystem-menu/finance.js','utf8'),{sourceType:'module'}); console.log('PARSE OK');"
```

---

### Task 16: Downstream — nút "Tạo phiếu thu" ở màn Đề nghị thu tiền

**Files:**
- Modify: `hrm-api/Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php` (thêm 1 method)
- Modify: `hrm-api/Modules/Finance/Transformers/BillIncomeRequestResource/BillIncomeRequestDetailResource.php` (thêm 1 khóa)
- Modify: `hrm-client/pages/finance/bill-income-requests/_id/index.vue` (thêm 1 nút)

**Interfaces:**
- Consumes: `BillIncome` (Task 1).
- Produces: cờ `is_can_create_bill_income` trong response chi tiết phiếu đề nghị.

⚠️ Đây là 3 file của **feature đã xong**. Chỉ THÊM, không sửa logic sẵn có. Nếu thấy cần đổi hàm dùng chung → **dừng, hỏi user** (CLAUDE.md).

- [x] **Step 1: Thêm method vào `BillIncomeRequest`**

```php
    /**
     * Đủ điều kiện lập phiếu thu từ phiếu đề nghị này chưa.
     *
     * Port ERP `BillIncome::canCreateBillIncome()` (:581) + BỔ SUNG điều kiện "chưa có phiếu thu"
     * mà ERP thiếu (ERP chỉ chặn ở lúc submit, nút vẫn hiện).
     */
    public function canCreateBillIncome(): bool
    {
        if ($this->status != self::STATUS_AWAITING_APPROVE) {
            return false;
        }

        if (!self::isAccountant()) {
            return false;
        }

        return !\Modules\Finance\Entities\BillIncome\BillIncome::where('bill_income_request_id', $this->id)->exists();
    }
```

- [x] **Step 2: Thêm cờ vào Detail Resource**

```php
            'is_can_create_bill_income' => $this->canCreateBillIncome(),
```

- [x] **Step 3: Thêm nút ở FE**

Trong `V2Footer` của `pages/finance/bill-income-requests/_id/index.vue`:
```html
                <V2BaseButton
                    v-if="detail.is_can_create_bill_income"
                    variant="primary"
                    icon="ri-add-line"
                    text="Tạo phiếu thu"
                    @click="$router.push(`/finance/bill-incomes/create?bill_income_request_id=${detail.id}`)"
                />
```
Đặt đúng thứ tự nút theo `button-convention`. Icon phải có trong `_remixicon.scss`.

- [x] **Step 4: `create.vue` nhận query**

Ở `hrm-client/pages/finance/bill-incomes/create.vue`, nếu có `?bill_income_request_id=` thì tự nạp phiếu đề nghị đó vào form ngay khi mở (không bắt user mở popup chọn lại).

- [x] **Step 5: Verify**

```bash
php -l hrm-api/Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php
php -l hrm-api/Modules/Finance/Transformers/BillIncomeRequestResource/BillIncomeRequestDetailResource.php
cd hrm-api && php artisan tinker --execute="
\$r = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest::where('status',2)->first();
var_dump(\$r ? \$r->canCreateBillIncome() : 'khong co phieu status=2');"
```
Rồi parse file Vue (lệnh Task 11 Step 9). Kỳ vọng: không lỗi. Giá trị `false` là bình thường nếu tài khoản chạy tinker không có quyền *Kế toán thanh toán*.

- [x] **Step 6: Verify không phá màn cũ**

```bash
cd hrm-api && php artisan tinker --execute="
\$r = Modules\Finance\Entities\BillIncomeRequest\BillIncomeRequest::with('details')->first();
echo json_encode(array_keys((new Modules\Finance\Transformers\BillIncomeRequestResource\BillIncomeRequestDetailResource(\$r))->resolve()), JSON_UNESCAPED_UNICODE);"
```
Kỳ vọng: danh sách khóa cũ **còn nguyên**, chỉ thêm `is_can_create_bill_income`.

---

### Task 17: Đối chiếu ngược ERP + checklist tự kiểm + dọn dẹp

**Files:** không sửa code (trừ khi lòi lỗi — sửa tại file liên quan rồi kiểm lại).

Đây là **Bước 5 + Bước 6** của `.claude/skills/erp-to-hrm-screen/SKILL.md`.

- [x] **Step 1: Đối chiếu cột**

Mở song song `resources/views/income_expenditure/bill_incomes/index.blade.php` (ERP) và `pages/finance/bill-incomes/index.vue`. Đủ 11 cột chưa? Cột ERP có mà HRM thiếu → thêm, mặc định **ẩn** trong Cấu hình cột nếu ít dùng.

- [x] **Step 2: Đối chiếu bộ lọc**

Đủ 10 ô `search_columns` của ERP + `search_by_info` + `search_by_time` chưa?

- [x] **Step 3: Đối chiếu hành động VÀ điều kiện ẩn/hiện**

Bảng đối chiếu bắt buộc điền:

| Hành động | Điều kiện ERP | Điều kiện HRM | Khớp? |
| --- | --- | --- | --- |
| In | luôn hiện | | |
| Xuất Excel | luôn hiện | | |
| Sửa | `canEdit()` = status 1 | | |
| Xóa | `canDelete()` = status 1 | | |
| Duyệt | `Thủ quỹ duyệt phiếu thu` + status 2 | | |
| Hủy | `Thủ quỹ duyệt phiếu thu` + status 2 | | |

Lệch dòng nào → sửa HRM cho khớp (trừ 6 chỗ HRM cố ý siết chặt hơn, đã liệt kê ở spec §9).

- [x] **Step 4: Chạy hết checklist A→H của skill**

Mở `.claude/skills/erp-to-hrm-screen/SKILL.md`, tick từng dòng 8 mục. Mục F (Import/Xuất) chỉ áp phần Xuất — màn này không có Import.

- [x] **Step 5: Chạy lại toàn bộ test + lint**

```bash
cd hrm-api && php vendor/bin/phpunit
for f in $(git -C hrm-api diff --name-only | grep '\.php$'); do php -l "hrm-api/$f"; done
```
Kỳ vọng: test OK, mọi file PHP sạch.

Parse lại toàn bộ file Vue mới:
```bash
cd hrm-client && for f in pages/finance/bill-incomes/index.vue pages/finance/bill-incomes/create.vue pages/finance/bill-incomes/_id/index.vue pages/finance/bill-incomes/_id/edit.vue pages/finance/bill-incomes/_id/print.vue pages/finance/bill-incomes/components/*.vue; do echo "== $f"; node -e "
const fs=require('fs'), c=require('vue-template-compiler'), b=require('@babel/parser');
const s=fs.readFileSync('$f','utf8'); const p=c.parseComponent(s);
const t=c.compile(p.template.content); if(t.errors.length){console.log('TEMPLATE LỖI',t.errors);process.exit(1)}
b.parse(p.script.content,{sourceType:'module',plugins:['optionalChaining','nullishCoalescingOperator']});
console.log('PARSE OK');"; done
```

- [x] **Step 6: Dọn dữ liệu test + xác nhận baseline**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT (SELECT COUNT(*) FROM bill_incomes) bi, (SELECT COUNT(*) FROM bill_income_details) bid, (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Kỳ vọng: **y hệt** 4 con số ghi ở Task 1 Step 2. Lệch → tìm bản ghi thừa theo `code LIKE '%PT%'` mới nhất và `invoiceable_type = 'App\Model\IncomeExpenditure\BillIncome'` mới nhất, xóa đúng phần mình tạo ra. **Không đụng dữ liệu nghiệp vụ có sẵn.**

- [x] **Step 7: Bàn giao cho user test trình duyệt**

Báo user: đã xong code, cần user tự mở trình duyệt kiểm 4 chế độ danh sách, tạo phiếu, gửi duyệt, duyệt, hủy, in, xuất Excel. Ghi rõ **những phần chưa kiểm chứng được**:
- nhánh phân bổ theo phiếu xuất hàng (0 dòng dữ liệu)
- nhánh thu dư nợ đầu kỳ (0 dòng dữ liệu)
- in phiếu loại thu 3 (nếu DB không có phiếu loại 3)
- việc ghi sổ cái mới chỉ chạy trong transaction rồi rollback, **chưa commit lần nào trên DB thật**

- [x] **Step 8: Cập nhật tài liệu**

Đánh `[x]` các task đã xong trong file này, ghi Checkpoint theo format CLAUDE.md, cập nhật `.plans/gop-db/STATUS.md`.

---

## Checkpoint

### Checkpoint — 2026-08-19 (Task 17 — đối chiếu ngược ERP + checklist tự kiểm)

**Vừa hoàn thành:** Task 17 — **XONG TOÀN BỘ 18/18 TASK**.

1. **Vá 2 món nợ về câu lỗi 422** (Ruling T14-b + 1 chỗ cùng lỗi tự tìm ra):
   - `components/ApproveBillIncomeModal.vue` — nhánh 422 mà `applyServerErrors()` không map được
     vào ô nào giờ dùng `extractErrorMessage()`, không còn hiện "The given data was invalid.".
   - `components/BillIncomeForm.vue` — cùng lỗi ở nhánh lưu phiếu (vd BE trả key `details` cấp mảng).
2. **Ô "Số phiếu đề nghị"**: bỏ `style="cursor: pointer"` (rơi vào `.v2-input__wrapper`, thẻ
   `<input>` bên trong không nhận) → dùng class `.picker-input` + `--readonly` **y hệt màn Đề nghị
   thu tiền** (`BillIncomeRequestForm.vue:969`). Khuôn ô vẫn là `CustomerBlock` (không nút, dấu hiệu
   bấm được nằm ở placeholder) như user yêu cầu.
3. **Đối chiếu ngược ERP** (bảng chi tiết bên dưới): 11/11 cột khớp, 10/10 ô lọc + `search_by_info`
   + `search_by_time` khớp, hành động khớp với 2 chỗ HRM **cố ý khác** (thêm Duyệt/Hủy vào dòng
   danh sách · ẩn nút In với loại thu 3 vì ERP nổ ErrorException).
4. **Checklist A→H**: phát hiện + sửa 2 lệch:
   - Màn chi tiết THIẾU nút **Sửa / Xóa** trong khi màn danh sách có (checklist B bắt buộc 2 màn
     khớp nhau). Đã thêm vào `V2Footer` theo đúng cờ BE `is_can_edit` / `is_can_delete`, dùng
     `menu.edit` + `BaseConfirmModal` như màn Đề nghị thu tiền; xóa xong về danh sách, 403/423 thì
     nạp lại chi tiết.
   - Màn danh sách tự dò `$store.state.permissions` bằng tay → chuyển sang mixin **`CheckPermission`**
     (`hasAPermission`), đúng checklist A "đủ 4 mixin" và đúng nguyên tắc dùng helper có sẵn.
5. **Verify**: `phpunit` **OK (36 tests, 103 assertions)** · `php -l` sạch mọi file PHP · parse
   **8/8 file Vue** của màn PASS · SCSS 2 file vừa sửa biên dịch OK (node-sass) · 8/8 icon có thật
   trong `_remixicon.scss` · baseline DB **khớp tuyệt đối**: `bill_incomes` 2.347 (max id 2347) ·
   `bill_income_details` 7.401 · `account_details` 971.973 (max id 1.001.370) ·
   `account_detail_refs` 1.024.988 — không có phiếu test sót.
6. **Ruling U4 (user chốt 2026-08-19)**: đồng bộ ngược trạng thái sang Phiếu đề nghị **GIỮ NGUYÊN
   LOGIC ERP** — 3 điểm hở đã biết không phải bug (xem `design.md` mục "Đồng bộ ngược…").

**Đang làm dở:** không.

**Bước tiếp theo:** user mở trình duyệt nghiệm thu (danh sách 1 màn · tạo/sửa/xóa nháp · gửi duyệt ·
duyệt · hủy · in · xuất Excel · nút Sửa/Xóa mới ở màn chi tiết). Sau đó: 1 lượt review tổng toàn
nhánh + phân loại ~45 minor đã park trong `.superpowers/sdd/finance-bill-income/progress.md`.

**Blocked:** không.

**Trạng thái git:** cả 2 repo đã có commit **"Phiếu thu"** của user (`hrm-api d274fde77`,
`hrm-client fe18da749`). Working tree API sạch; client còn **4 file sửa trong Task 17**:
`pages/finance/bill-incomes/index.vue` · `_id/index.vue` · `components/ApproveBillIncomeModal.vue` ·
`components/BillIncomeForm.vue`. Chưa commit (đúng quy tắc dự án).

**Chưa kiểm chứng được (bàn giao user):**
- Nhánh *phân bổ theo phiếu xuất hàng* và *thu dư nợ đầu kỳ*: DB 0 dòng → chỉ verify bằng đọc code.
- In phiếu **loại thu 3**: DB không có phiếu loại 3 để render thật.
- Ghi sổ cái mới chỉ chạy **trong transaction rồi rollback**, chưa commit lần nào trên DB thật.
- Toàn bộ giao diện: chưa mở trình duyệt trong lượt này (parse + SCSS + icon là mức verify tĩnh).

---

## Đối chiếu ngược ERP (Task 17 — Bước 5 của skill `erp-to-hrm-screen`)

### Cột (ERP `index.blade.php:41-53` — 11 cột)

| # | ERP | HRM `index.vue` | Khớp |
| --- | --- | --- | --- |
| 1 | STT | `index` (locked, center) | ✅ |
| 2 | Mã phiếu | `code` (locked, `<nuxt-link>`, sort) | ✅ |
| 3 | Mã phiếu đề nghị thu | `requestCode` (link sang chi tiết đề nghị) | ✅ |
| 4 | Loại thu | `typeText` | ✅ |
| 5 | Khách hàng | `customerText` | ✅ |
| 6 | Số tiền | `sumMoney` (căn phải, sort) | ✅ |
| 7 | Người đề nghị | `requesterName` | ✅ |
| 8 | Ngày lập | `createdAt` (sort) | ✅ |
| 9 | Người lập | `createdByName` | ✅ |
| 10 | Trạng thái | `billStatus` (V2BaseBadge) | ✅ |
| 11 | Hành động | `actions` (locked) | ✅ |

ERP chỉ cho sort cột `sum_money`; HRM mở thêm `code` + `created_at` (BE whitelist đúng 3 cột này) —
đúng quy tắc chung màn danh sách HRM.

### Bộ lọc (ERP `search_columns` — 10 ô + 2 cờ)

| ERP | HRM | Khớp |
| --- | --- | --- |
| `code` (text) | ô **tìm nhanh** `filters.code`, chờ bấm Tìm kiếm (`ignoredFields`) | ✅ |
| `code_bill_income_request` (text) | field `code_bill_income_request` | ✅ |
| `bill_income_request_type` (select) | field `bill_income_request_type` | ✅ |
| `created_by` (select-ajax) | field `created_by` | ✅ |
| `money_from` / `money_to` (currency) | field gộp `money_range` (2 ô `V2BaseCurrencyInput`) | ✅ |
| `customer_id` (select-ajax) | slot `field-customer_id` — nguồn KH **ERP** `assign/customers` | ✅ |
| `contract_code` (text) | field `contract_code` | ✅ |
| `created_by_request` (select-ajax) | field `created_by_request` | ✅ |
| `status` (select) | field `status` | ✅ |
| `search_by_info` (chỉ `_type=all`) | slot `field-org` — Công ty/Phòng ban/Bộ phận, luôn khai | ✅ |
| `search_by_time: true` | field `created_range` (2 datepicker) | ✅ |

### Hành động + điều kiện ẩn/hiện

| Hành động | Điều kiện ERP | Điều kiện HRM | Khớp? |
| --- | --- | --- | --- |
| In | luôn hiện (`BillIncomeController:90`) | `Number(item.type) !== 3` | ⚠️ **HRM chặt hơn có chủ ý** — loại "Thu khác" không có mẫu in, ERP bấm vào là `ErrorException` |
| Xuất Excel | luôn hiện (`:92`) | luôn hiện | ✅ |
| Sửa | `canEdit()` = status 1 (`:94`) | cờ BE `is_can_edit` (= status 1) — cả danh sách **và** màn chi tiết | ✅ |
| Xóa | `canDelete()` = status 1 (`:98`) | cờ BE `is_can_delete` (= status 1) — cả danh sách **và** màn chi tiết | ✅ |
| Duyệt | ERP chỉ có ở **màn chi tiết**: `Thủ quỹ duyệt phiếu thu` + status 2 (`show.blade.php:18`) | cờ BE `is_can_approve` (cùng 2 điều kiện) — HRM đưa **thêm** vào dòng danh sách (điều hướng sang chi tiết) | ⚠️ HRM **mở rộng có chủ ý**, điều kiện y hệt |
| Hủy | như trên (`show.blade.php:22`) | như trên | ⚠️ như trên |

Ngoài ra HRM siết chặt hơn ERP 6 chỗ đã liệt kê ở spec §9 (`delete` có gate + 423, khóa dòng khi
duyệt, `generateCode` có `lockForUpdate`, rethrow `ValidationException`, `canView` không coi
`null == null` là cùng công ty, chặn duyệt lại 409).

### Checklist A→H — kết quả

| Mục | Kết quả |
| --- | --- |
| A. Màn danh sách | ✅ sau khi thêm mixin `CheckPermission`. 4 mixin đủ · `localStorageKey`/`columnScreenKey` = `finance_bill_incomes` không trùng màn nào · STT qua `getNumericalOrder` · Mã là `<nuxt-link>` · sort mặc định `created_at desc` (BE) · rỗng hiện "Không có dữ liệu phù hợp bộ lọc." · popup "Cài đặt bộ lọc" (>3 ô) |
| B. Nút & hành động | ✅ sau khi thêm Sửa/Xóa ở màn chi tiết. Mọi nút có icon + text · 6 hành động → `V2BaseRowActions` cắt 2 nút chính + menu "…" · nút không dùng được **ẩn hẳn** bằng `visible`/`v-if` · nút màn chi tiết nằm trong `V2Footer` · màu: Duyệt xanh lá, Hủy/Xóa đỏ, Xuất Excel xanh nhạt |
| C. Hiển thị dữ liệu | ✅ `V2BaseBadge` + `status_text` BE · tiền `number_format(…, ',', '.')` căn phải · ngày `d/m/Y` BE trả · ô rỗng in `—` · chữ `font-weight-normal` |
| D. Form | ✅ lỗi inline dưới từng ô (`V2BaseError`) · required do BE trả 422 · `unsavedChangesMixin` + `markFormSaved()` · datepicker `dd/mm/yyyy` |
| E. Chi tiết | ✅ tiêu đề `Chi tiết phiếu thu tiền: <mã>`, số phiếu hiện trong khối Thông tin chung. Mục "Lịch sử" **ngoài scope** (design.md) |
| F. Import/Xuất | ✅ phần áp dụng: không có Import (đúng ERP); Xuất là **xuất 1 phiếu** nên không có popup chọn trường (ERP cũng vậy) |
| G. Thông báo & xác nhận | ✅ toast dùng câu ERP (spec §5.5) · xác nhận bằng `BaseConfirmModal` / `V2BaseModal` · chuông đúng template `[TC] Chờ duyệt phiếu thu: <b>MÃ</b>. Người lập: …` + deep-link kèm id |
| H. Bản ghi đã khóa | ✅ BE trả **423** ở `update`/`destroy` · FE ẩn nút · vào `/edit` bằng URL trực tiếp bị `$router.replace` về chi tiết. Không có cơ chế Khóa/Mở khóa (màn này không dùng) |



### Checkpoint — 2026-08-18 15:2x

**Vừa hoàn thành:** 16/17 task đã code xong. Task 1-11, 13-16 đã review sạch (verdict Approved,
0 Critical còn mở). Backend hoàn chỉnh; frontend còn đúng 1 lượt sửa đang chạy.

**Đang làm dở:**
- Task 12 `BillIncomeForm.vue` — **fix round 2 đang chạy**: đổi ô "Số phiếu đề nghị" sang khuôn
  `assign/prospective-projects/components/CustomerBlock.vue:22-32` theo yêu cầu trực tiếp của user
  (bỏ `.source-picker` + nút "Chọn", dùng placeholder "Nhấn vào đây để chọn…" + `V2BaseError`).
  Fix round 1 của task này đã re-review ADDRESSED (8 khối `V2BaseError` + `V2BaseCheckbox` an toàn).
- **Task 17 CHƯA CHẠY** — đối chiếu ngược ERP + checklist A→H + dọn dữ liệu + bàn giao.

**Bước tiếp theo:**
1. Chờ Task 12 fix round 2 xong → re-review phạm vi hẹp cho đúng ô picker.
2. Chạy Task 17, kèm 1 việc vá còn nợ: `components/ApproveBillIncomeModal.vue:267` vẫn đọc
   `.message` cho nhánh 422 → phải dùng helper `extractErrorMessage` như 2 file kia
   (Ruling T14-b đã giao việc này cho Task 17).
3. Bàn giao user test trình duyệt.

**Blocked:** không.

**Trạng thái DB:** baseline 2347 / 7401 / 971973 / 1024988 giữ nguyên suốt 16 task, chưa commit
dòng dữ liệu nào. Chưa git commit bất cứ gì (đúng quy tắc dự án).

**⚠️ Cần user xác nhận trước khi commit:** working tree `hrm-client` có 2 file
`pages/finance/bill-adjust-dept-requests/**` bị sửa KHÔNG thuộc feature này (mtime tăng theo thời
gian thực trong lúc chạy → nghi phiên song song của người khác). Đừng `git add .`, xem
`.superpowers/sdd/finance-bill-income/progress.md` mục "BẤT THƯỜNG NGOÀI PHẠM VI".

---

### Checkpoint — 2026-08-18 (lúc lên plan)
Vừa hoàn thành: chốt design + viết spec đầy đủ + lên plan 17 task.
Đang làm dở: chưa bắt đầu code.
Bước tiếp theo: Task 1 — dựng 3 entity `BillIncome` / `BillIncomeDetail` / `BillIncomeDetailProductExportRequest`.
Blocked:

---

## Bugfix 2026-08-20 — Cột "Người/Ngày cập nhật" + đổi nhãn "lập" → "tạo"

**Hiện tượng (user báo):** popup *Cấu hình cột tùy chỉnh* của màn `/finance/bill-incomes` thiếu
2 trường **Người cập nhật** / **Ngày cập nhật**; 2 cột **Ngày lập** / **Người lập** phải đổi nhãn
về **Ngày tạo** / **Người tạo**.

**Nguyên nhân gốc:** màn được port 1:1 theo ERP (spec §6.4 chốt đúng 11 cột, dùng nguyên văn nhãn
ERP "Ngày lập/Người lập") nên bỏ qua quy tắc chung màn danh sách HRM
(`.claude/skills/list-page/SKILL.md` mục 6: cột **Người tạo/Ngày tạo** bắt buộc, ngày hiện
**d/m/Y H:i** width 140px; màn anh em `bill-income-requests` đã có đủ 4 cột). Kéo theo BE:
`BillIncomeListResource` không trả `updated_at`/`updated_by_name`, entity `BillIncome` chưa có
quan hệ `employeeUpdate` (dù hook `saving` vẫn ghi `updated_by` → dữ liệu có sẵn, không cần migration).

### Task

- [x] B1. `BillIncome`: thêm quan hệ `employeeUpdate()` (belongsTo Employee, `updated_by`)
- [x] B2. `BillIncomeService::searchByFilter`: eager load `employeeUpdate.info` (chặn N+1);
      thêm `updated_at` vào whitelist sắp xếp của `applySort()`
- [x] B3. `BillIncomeListResource`: trả thêm `updated_by_name`, `updated_at` (`d/m/Y H:i`);
      đổi `created_at` sang `d/m/Y H:i` cho khớp quy tắc mục 6 skill list-page
- [x] B4. `pages/finance/bill-incomes/index.vue`: đổi tiêu đề cột `Ngày lập`→`Ngày tạo`,
      `Người lập`→`Người tạo`; xếp lại `Người tạo` → `Ngày tạo` (đúng thứ tự skill);
      thêm 2 cột `updatedByName` / `updatedAt` + template ô; `SORT_FIELD_MAP` thêm `updatedAt`

### Checkpoint — 2026-08-20

**Vừa hoàn thành:** bugfix B1-B4 (cột Người/Ngày cập nhật + đổi nhãn "lập" → "tạo" ở màn danh sách
Phiếu thu).

Đã sửa 4 file:
- `hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php` — thêm quan hệ `employeeUpdate()`
- `hrm-api/Modules/Finance/Services/BillIncomeService.php` — eager load `employeeUpdate.info`,
  whitelist sort thêm `updated_at`
- `hrm-api/Modules/Finance/Transformers/BillIncomeResource/BillIncomeListResource.php` — trả thêm
  `updated_by_name` + `updated_at`; `created_at` đổi sang `d/m/Y H:i`
- `hrm-client/pages/finance/bill-incomes/index.vue` — 13 cột, nhãn Ngày tạo / Người tạo /
  Người cập nhật / Ngày cập nhật, template ô + `SORT_FIELD_MAP.updatedAt`

**Kiểm chứng:** `php -l` sạch 3 file BE · SFC parse sạch (vue-template-compiler + @babel/parser) ·
tinker trên DB thật: 2347/2347 phiếu có `updated_by`, quan hệ trả đúng tên người + ngày giờ.
Chưa mở trình duyệt (user tự test).

**Đang làm dở:** không.

**Bước tiếp theo:** user xác nhận có đổi luôn nhãn bộ lọc "Ngày lập từ/đến" (`index.vue:64,75`) và
ô lọc "Người lập" (`:425`), cùng 2 nhãn trong `IncomeRequestSearchModal.vue` (`:36,:69` — cột này
là người lập PHIẾU ĐỀ NGHỊ, có thể giữ nguyên) sang "tạo" hay không.

**Blocked:** không.

---

## Bugfix 2026-08-20 (2) — Màn in `/finance/bill-incomes/{id}/print` chưa giống ERP

**Hiện tượng (user báo):** font chữ, bảng, chữ in đậm của bản in khác bên ERP.

**Nguyên nhân gốc:** BE trả đúng HTML mẫu in ERP (`report_templates` 203-206) nhưng **môi trường CSS
khác hẳn**. ERP (`resources/views/print.blade.php` → `printPDF()`) chỉ nạp **`public/css/pdf.css`**;
HRM lại nạp `/css/print-app.css` + `/ckeditor/css/editor.css` rồi tự "mô phỏng lại" pdf.css bằng
`printContentStyles()`. Đối chiếu từng rule trên HTML thật của phiếu 2347:

| Chỗ lệch | ERP (pdf.css) | HRM (print-app + editor.css) |
| --- | --- | --- |
| Giãn dòng | mặc định trình duyệt (~1.2) | `line-height: 1.6 !important` (editor.css `body.document-editor`) |
| `<p>` ngoài bảng | margin mặc định 1em | `margin/padding: 0 !important` (editor.css) |
| Ô bảng `.no-border` (letterhead, khối chữ ký) | `padding: 5px 8px !important` | `.table td { padding: .75rem !important }` |
| Mọi `table.table` | không có rule | `margin-bottom: 1rem !important` → hở thêm 16px giữa các khối |
| Bảng nhỏ *Liên số/Số/Nợ/Có* (`class="table table-bordered"` **lồng trong** `<table class="no-border">`) | `.no-border td { border: none!important }` thắng → **KHÔNG viền** | rule mô phỏng `#content table:not(.no-border) td` specificity cao hơn → **có viền đen** (sai) |

**Cách sửa:** dựng lại **đúng môi trường CSS của ERP** thay vì mô phỏng — copy nguyên
`erp/public/css/pdf.css` sang `hrm-client/static/css/pdf-erp.css`, iframe in chỉ nạp file này +
đúng khối style inline của `printPDF()`. Không đặt tên `pdf.css` vì plugin dùng chung
`plugins/print-content.js` tự nạp `/css/pdf.css` cho **mọi** màn in → đổi font/viền toàn hệ thống.

### Task

- [x] C1. Thêm `hrm-client/static/css/pdf-erp.css` (bản sao `erp/public/css/pdf.css`)
- [x] C2. `print.vue` — iframe in: bỏ `print-app.css` + `editor.css` + `body.document-editor`,
      chỉ nạp `pdf-erp.css`; `printBaseStyles()` rút về đúng khối inline ERP; xóa `printContentStyles()`
- [x] C3. `print.vue` — preview: bỏ `print-app.css` khỏi `head()`, style scoped mô phỏng đúng
      pdf.css (kể cả quirk bảng lồng `.no-border` mất viền) để xem trước khớp bản in

### Checkpoint — 2026-08-20 (màn in)

**Vừa hoàn thành:** C1-C3 — bản in `/finance/bill-incomes/{id}/print` chạy đúng môi trường CSS ERP.

Đã sửa 2 file:
- `hrm-client/static/css/pdf-erp.css` (MỚI) — bản sao nguyên văn `erp/public/css/pdf.css`,
  kèm docblock giải thích vì sao KHÔNG đặt tên `pdf.css` (plugin `plugins/print-content.js:15`
  nạp `/css/pdf.css` cho mọi màn in → đổi tên đó là đổi font/viền toàn hệ thống)
- `hrm-client/pages/finance/bill-incomes/_id/print.vue` — iframe in chỉ nạp `pdf-erp.css` +
  khối style inline của `printPDF()` (`@page`, `body{margin:0}`, `.MsoBodyTextIndent`,
  `div.page-break.active`); bỏ `print-app.css`, `editor.css`, class `document-editor` và toàn bộ
  `printContentStyles()`; `head()` không nạp stylesheet toàn cục nữa; `<style scoped>` của preview
  chép lại đúng rule pdf.css để xem trước khớp bản in

**Kiểm chứng:** dump HTML mẫu in thật của phiếu 2347 (`BillIncomePrintService::render`) rồi đối
chiếu từng rule ERP ↔ HRM — 5 điểm lệch đã liệt kê ở bảng trên. SFC parse sạch
(vue-template-compiler + @babel/parser). **Chưa mở trình duyệt** — cần user so bản in HRM với ERP.

**Bước tiếp theo:** user in thử phiếu 2347 ở cả 2 cổng và so. Nếu khớp thì cân nhắc áp cùng cách
cho các màn in v-html chị em (`bill-income-requests`, `bill-payments`, `bill-payment-requests`,
`product-transfer-requests`) — hiện vẫn dùng lối mô phỏng pdf.css cũ.

**Blocked:** không.

- [x] C4. Preview mất chữ đậm: `assets/scss/custom/components/_reboot.scss:21` đặt
      `b, strong { font-weight: 500 }` toàn hrm-client, Times New Roman không có nét 500 →
      trình duyệt vẽ như chữ thường. Trả `font-weight: bold` trong `<style scoped>` của màn in
      (KHÔNG sửa file reboot dùng chung). Bản in trong iframe không dính lỗi này vì không nạp CSS app.

- [x] C5. **"Bằng chữ: … đồng đồng"** — `BillIncomePrintService:155` chép nguyên câu ERP
      `ucfirst(convertNumberToWords($x)) . ' đồng'`. Bên ERP helper gọi `n2c($number, '')` (tham số
      2 là đơn vị tiền, truyền rỗng) nên trả chữ số trần; trên HRM `n2c()` là của gói
      `phpviet/laravel-number-to-words` và ĐÃ tự gắn "đồng" → thừa 1 chữ. Thêm
      `moneyInWords()` (cắt hậu tố rồi gắn lại đúng 1 lần) y hệt `BillPaymentPrintService` —
      KHÔNG sửa helper dùng chung. Kiểm chứng phiếu 2347: đếm "đồng" = 1.
- [x] C6. **Hàng chữ ký lệch mép trang** — 2 bảng cuối của mẫu in 203-206 khai cứng
      `style="width:827px"` trong khi vùng in chỉ 180mm (A4 210mm − lề 20mm + 10mm) ≈ 680px →
      tràn phải, cột cuối bị cắt, không thẳng hàng với bảng chi tiết (`width:100%`). Thêm
      `#content table { max-width: 100% !important }` vào `printBaseStyles()` + `<style scoped>`
      của màn in. **Khác ERP có chủ ý** (ERP cũng tràn) vì mẫu in nằm trong `report_templates`
      dùng chung 2 cổng, không tự sửa.

**Còn tồn (nằm trong `report_templates`, dùng chung với ERP — cần user chốt mới đụng):**
hàng chữ ký có **6 ô** `width:20%` (tổng 120%) trong đó ô thứ 6 là bản nhân đôi "THỦ QUỸ" cỡ chữ
1px → 5 tiêu đề nhìn thấy chỉ chiếm 5/6 bề ngang, dôi khoảng trống bên phải; mẫu cũng đang gõ
thiếu dấu "BAN GIAM ĐỐC".

- [x] C7. **Hàng chữ ký dồn trái ở preview + so le cao thấp khi in** (user báo 2026-08-20, sau C6).
      Đo bằng trình duyệt trên bản dựng tĩnh (pdf-erp.css + style in thật, khổ 180mm):
      - *Dồn trái ở preview*: `#content` của màn preview giãn hết bề ngang màn hình, trong khi 2
        bảng cuối mẫu in khai cứng `width:827px` → bảng nằm nép trái, chừa khoảng trắng lớn bên phải.
        Fix: dựng `#content` thành TỜ A4 (`width: 210mm`, `box-sizing: border-box`, padding = ĐÚNG
        lề in `15mm 10mm 15mm 20mm`, nền trắng + viền + đổ bóng như preview ERP) → bề ngang chỗ chữ
        đúng 680px, khớp y hệt bản in.
      - *So le cao thấp khi in*: ô rộng 20% (~132px) hẹp hơn nhãn nên "KẾ TOÁN TRƯỞNG",
        "NGƯỜI NỘP TIỀN", "NGƯỜI LẬP PHIẾU" xuống 2 dòng; ô 1 dòng lại bị canh giữa theo chiều dọc
        (`vertical-align` mặc định của `td` là `middle`) → chữ cao chữ thấp. Fix:
        `#content table.block td { white-space: nowrap; vertical-align: top; padding: 2px 4px }`
        (class `block no-border` chỉ có ở đúng 2 bảng này — đếm trên HTML thật: 4 lần = 2 bảng × 2 liên).
      - Kiểm chứng sau fix (đo lại): bảng 679px/680px (tràn 0), 5 nhãn mỗi nhãn 1 dòng
        (111 / 132 / 120 / 129 / 72 px), mọi nhãn bắt đầu cùng mức (textTop 2-3px).

---

## Rà nút theo `.claude/skills/button-convention` — màn chi tiết/duyệt phiếu thu (2026-08-20)

Rà toàn bộ nút của `/finance/bill-incomes/{id}` (V2Footer + popup Duyệt + popup Hủy).

**MÀU đã đúng chuẩn, không phải sửa** (đối chiếu mục 2b):
Sửa `primary` (teal) · Duyệt `primary status="success"` · Hủy phiếu thu `primary status="danger"` ·
In `secondary` (info) · Xuất Excel `secondary status="success"` · Xóa `primary status="danger"` ·
Quay lại / Đóng `tertiary`. Mọi nút đều có icon `#prefix` + `size="sm"`, không nút nào dùng
`type="primary"`, không dùng `light` trong modal.

**Lệch chuẩn phát hiện được:**

- [x] D1. **Thứ tự nút sai** (mục 5): "Hủy phiếu thu" (danger) đang đứng TRƯỚC nhóm phụ
      (In, Xuất Excel). Chuẩn: chính → phụ → nguy hiểm → thoát. Xếp lại thành
      Duyệt → In → Xuất Excel → Hủy phiếu thu → Xóa (Sửa do V2Footer render trước slot, Quay lại sau).
- [x] D2. **Chữ "Duyệt phiếu thu"** ≠ bảng text chuẩn mục 4.2 (`Duyệt`) — popup duyệt cũng đang
      dùng đúng chữ "Duyệt" nên 2 chỗ đang lệch nhau. Đổi về `Duyệt`.
- [x] D3. **Icon nút "Xác nhận"** trong popup Hủy đang là `ri-close-circle-line`; bảng icon mục 3
      quy định `Xác nhận / Duyệt → ri-check-line` (icon `ri-close-circle-line` dành cho "Từ chối").
      Header popup vẫn giữ icon đỏ `ri-close-circle-line` nên vẫn đọc ra là thao tác hủy.

**Không đụng:** `components/V2Footer.vue` (component dùng chung — nút Sửa/Quay lại render từ đây).

### Checkpoint — 2026-08-20 (rà nút màn chi tiết)

**Vừa hoàn thành:** D1-D3 trong `pages/finance/bill-incomes/_id/index.vue`. Thứ tự nút cuối cùng
trên màn: Sửa (primary) → Duyệt (primary success) → In (secondary) → Xuất Excel (secondary success)
→ Hủy phiếu thu (primary danger) → Xóa (primary danger) → Quay lại (tertiary).
MÀU không đổi — đã đúng chuẩn từ trước; chỉ đổi thứ tự, chữ "Duyệt phiếu thu" → "Duyệt" và icon
nút "Xác nhận" của popup Hủy → `ri-check-line`.

**Kiểm chứng:** SFC parse sạch (vue-template-compiler + @babel/parser). Chưa mở trình duyệt.

**Còn cân nhắc (chưa làm, chờ user):** chữ "Hủy phiếu thu" không có trong bảng text chuẩn mục 4.2;
giữ nguyên vì rút thành "Hủy" sẽ lẫn với nút hủy thao tác. Nếu team muốn thống nhất thì đổi 1 lượt
cho cả Phiếu chi / Đề nghị thu / Đề nghị chi.

**Blocked:** không.

### Đổi chuẩn màu nhóm Duyệt — 2026-08-20 (user chốt)

Nhóm **Duyệt · Gửi duyệt · Hoàn thành · Kích hoạt** chuyển từ `primary status="success"` (#16A34A)
sang **`primary` không kèm status (#1ABC9C teal)**; **Gửi duyệt** rời nhóm `warning` (cam) sang
nhóm này. Lý do: teal vốn đã là màu nút Duyệt / Lưu và duyệt / Trưởng phòng duyệt / BGĐ duyệt mặc
định của `components/V2Footer.vue` — component dùng chung của hầu hết màn chi tiết; thống kê thực tế
43 nút liên quan tới duyệt trong `pages/` + `components/` thì đa số đang teal, chỉ 4 nút của
Phiếu thu / Phiếu chi để `success`.

- [x] E1. Sửa `.claude/skills/button-convention/SKILL.md` mục 2b (bảng "Các nhóm còn lại" + ghi chú
      giải thích lựa chọn). ⚠️ Skill là **tài sản chung** — theo quy tắc team phải đưa qua PR, chưa commit.
- [x] E2. Đồng bộ bảng tra nhanh `.plans/gop-db/list-page-action-column/quy-tac-mau-button.xlsx`
      (2 dòng: nhóm Duyệt đổi màu ô XEM THỬ sang #1ABC9C; dòng cam còn lại "Khóa / Cảnh báo").
- [x] E3. Áp chuẩn mới cho màn Phiếu thu: bỏ `status="success"` ở nút Duyệt tại
      `pages/finance/bill-incomes/_id/index.vue` và `components/ApproveBillIncomeModal.vue`.

**Chưa làm — chờ user chốt** (nằm ngoài feature Phiếu thu):
`pages/finance/bill-payments/_id/index.vue` + `components/ApproveBillPaymentModal.vue` (2 nút Duyệt
còn `success`) · `pages/assign/quotations/_id/index.vue` ("BGĐ duyệt" `success`) ·
`components/V2Footer.vue` ("Hoàn thành" `success` — component dùng chung) ·
`pages/finance/bill-payments/components/BillPaymentForm.vue` ("Lưu và gửi KT trưởng duyệt" `warning`) ·
`components/assign/quotation/QuotationLowPriceWarningModal.vue` ("Tiếp tục gửi duyệt" `warning`).

- [x] E4. Xếp **Duyệt phiếu thu** và **Hủy phiếu thu** đứng cạnh nhau (user yêu cầu 2026-08-20).
      Thứ tự cuối: Sửa → Duyệt phiếu thu → Hủy phiếu thu → In → Xuất Excel → Xóa → Quay lại.
      **Cố ý lệch** skill button-convention mục 5 (chính → phụ → nguy hiểm → thoát) — đã ghi chú
      ngay trên khối nút trong `_id/index.vue` để lượt review sau không "sửa lại cho đúng skill".
      Ghi nhận: file `_id/index.vue` có bản sửa ngoài phiên (nút Duyệt gộp 1 dòng, giữ chữ
      "Duyệt phiếu thu" thay vì "Duyệt") — tôn trọng bản đó, không áp lại đề xuất đổi chữ ở D2.

- [x] E5. Màn Thêm phiếu thu (`finance/bill-incomes/create`): luôn hiện **bảng Chi tiết** kể cả khi
      chưa chọn phiếu đề nghị thu (user yêu cầu 2026-08-20). Trước đó section Chi tiết chỉ hiện dòng
      chữ "Chưa chọn phiếu đề nghị thu". Nay bỏ nhánh `v-if/v-else`, bảng render luôn với cột mặc
      định (chưa có phiếu → `typeNumber` = NaN nên partyLabel = "Khách hàng", có cột Số đơn hàng/Hợp
      đồng, tiền VND 1 cột), tbody hiện 1 dòng trống với text từ computed mới `emptyDetailText`
      ("Chưa chọn phiếu đề nghị thu" / "Không có dữ liệu"). File:
      `pages/finance/bill-incomes/components/BillIncomeForm.vue`.

- [x] E6. Bảng Chi tiết khi trống phải **ngắn gọn** như bảng ở `customer-care/warranty-repair-requests/create`
      (user yêu cầu 2026-08-20). Nguyên nhân bảng cao lênh khênh: class `.table-responsive` dính rule
      toàn cục `assets/scss/default.scss:85` (`min-height: 50vh`). Sửa: đổi wrapper sang
      `V2BaseTableScroll` (đúng khuôn màn tham chiếu, lại có thêm thanh cuộn ngang phía trên);
      dòng trống bỏ `py-3` và đổi `.text-muted` → class riêng `.v2-empty-row` (#6b7280) vì SCSS toàn
      cục ép `.text-muted` thành ĐỎ như lỗi validate.

### Checkpoint — 2026-08-20
Vừa hoàn thành: E5 + E6 — bảng Chi tiết luôn hiện và gọn khi trống ở màn Thêm phiếu thu.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra hiển thị bảng khi chưa chọn phiếu đề nghị.
Blocked:

### Sửa lỗi file Excel xuất phiếu thu — 2026-08-20 (user báo)

3 lỗi trên file `.xlsx` tải về từ nút "Xuất Excel" (cả màn danh sách lẫn chi tiết đều gọi
`GET /finance/bill-incomes/{id}/export`):

1. **Thiếu logo (letterhead) công ty ở đầu file** — `BillIncomePrintService::excelPlaceholders()`
   đã dựng sẵn `HEADER` (URL tuyệt đối ảnh letterhead theo công ty người tạo phiếu) nhưng blade
   `finance::exports.bill_income` không dùng tới. Bản IN có logo, bản Excel thì không.
2. **Cột quá hẹp** — HTML reader của PhpSpreadsheet đọc `width: 10px/48px/20px` trong thẻ `<td>`
   ra bề rộng 1.43 / 6.86 / 2.86 ký tự. Cùng nguyên nhân đã xử lý ở `BillPaymentRequestExport` /
   `ProductTransferRequestExport`: phải dùng `WithColumnWidths`, không đặt `width` px trong HTML.
3. **Cột số tiền báo "The number in this cell is formatted as text"** — service in tiền bằng
   `number_format()` ("2,135,916") nên PhpSpreadsheet lưu kiểu chuỗi. Phải xuất SỐ THÔ + đặt
   `NumberFormat` như `BillPaymentExport::registerEvents()` đang làm cho Phiếu chi.

- [x] F1. `BillIncomePrintService`: 3 hàm dựng bảng bản EXCEL (`billIncomeExcelTable`,
      `billIncomeExcelWithExchangeRateTable`, `excelProductExportRequestsTable`) + `SO_TIEN` xuất
      SỐ THÔ thay cho `number_format()`. KHÔNG đụng 3 hàm bản IN (bản in là HTML cho trình duyệt,
      vẫn cần chuỗi có dấu phân cách).
- [x] F2. `BillIncomeExport` implement `WithColumnWidths` — bộ bề rộng riêng cho 2 bố cục
      (1 chi tiết = khối nhãn/giá trị; nhiều chi tiết = bảng 8/9 cột).
- [x] F3. `BillIncomeExport` implement `WithDrawings` — nhúng ảnh `HEADER` vào ô A1, nới chiều cao
      dòng 1. Ảnh nằm trên server ERP → tải bằng HTTP, hỏng/timeout thì BỎ QUA (không chặn export).
- [x] F4. `registerEvents()`: thêm `NumberFormat` cho vùng ô tiền (giữ nguyên phần kẻ viền cũ).
- [x] F5. Kiểm chứng: dựng lại file cho 1 phiếu 1 chi tiết + 1 phiếu nhiều chi tiết, đọc lại bằng
      PhpSpreadsheet xác nhận ô tiền kiểu `n`, bề rộng cột đúng, có drawing.

**Kết quả kiểm chứng (dựng file thật ở local, đọc lại bằng PhpSpreadsheet):**

| | Trước | Sau |
| --- | --- | --- |
| Ô tiền 1 chi tiết (C8) | `[s] "2,135,916"` | `[n] 2135916`, format `#,##0` → hiện `2,135,916` |
| Cột tiền nhiều chi tiết (G10+) | `[s]` | `[n]`, kể cả dòng **Tổng cộng** (`100,277,000`) |
| Bề rộng cột (phiếu nhiều dòng) | A=1.43 · B=6.86 · C=2.86 · G=2.86 | A=6 · B=36 · C=26 · G=18 · H=18 · I=18 |
| Logo | không có | drawing `A1` 463×72 px, dòng 1 cao 58pt |

Phiếu ngoại tệ: DB gộp **0 phiếu** (đếm 2026-08-20) → chạy thử bằng cách ép `type_money_id = 2`
TRONG BỘ NHỚ (không `save()`), xác nhận cả cột G (nguyên tệ) và H (quy đổi VND) ra kiểu số.

Bản IN không đụng tới: `placeholders()` + `render()` chạy lại vẫn ra `2,135,916` như cũ.

**Chưa kiểm chứng:** ảnh letterhead thật — máy local không với tới `erp.test:8080/uploads/...`
(404), nên logo test bằng ảnh PNG dựng tạm qua `file://`. Trên môi trường có ERP thật, nếu URL
chết thì file vẫn xuất bình thường, chỉ không có logo (đã chủ ý nuốt lỗi).

### Checkpoint — 2026-08-20 (F1-F5)
Vừa hoàn thành: sửa 3 lỗi file Excel phiếu thu (logo · bề rộng cột · số tiền là text).
Đang làm dở: không có.
Bước tiếp theo: user tải lại file Excel trên môi trường dev để xác nhận logo công ty hiện đúng.
Blocked: không.

**Việc cùng loại chưa làm (ngoài phạm vi yêu cầu):** `BillPaymentExport` (Phiếu chi) đang cố ý bỏ
logo và chưa có `WithColumnWidths`; số tiền bản Phiếu chi vẫn là chuỗi `number_format()` (chỉ có
NumberFormat áp lên ô, không đổi được kiểu ô) → cùng 3 triệu chứng. Hỏi user có làm luôn không.

### Sửa lại F4 — 2026-08-20 (khi làm Phiếu chi thì tìm ra cách tốt hơn)

Bỏ cách đặt `NumberFormat` theo vùng ô trong `registerEvents()`, chuyển sang khai
`data-format="#,##0"` trên TỪNG thẻ `<td>` tiền (HTML reader của PhpSpreadsheet có đọc thuộc tính
này). Lý do: vùng ô phải tự tính theo số dòng, mà bảng chi tiết có thể nở thêm dòng do bảng phân bổ
phiếu xuất hàng (rowspan) → trỏ trượt. Ô "Số tiền" của phiếu 1 chi tiết gắn `data-format` trong
blade, có điều kiện `$typeMoneyId == 1` (ngoại tệ in kèm tên tiền tệ nên là chuỗi).

Phần nhúng letterhead tách sang trait dùng chung `Exports/Concerns/EmbedsCompanyLetterhead.php`.
Kiểm chứng lại sau khi đổi: C8 `[n] #,##0`, G10+ `[n] #,##0`, dòng Tổng cộng `100,277,000`,
drawing A1 463×72 — y như trước.

Quy tắc rút ra đã gói vào `.claude/skills/export-excel/SKILL.md`.

---

## Phase G — Logo (letterhead) bản in phiếu thu dùng chung cách của màn Báo giá (2026-08-21)

**Yêu cầu user:** "tham khảo màn báo giá, xem cách dùng logo ở màn in, sửa lại giống vậy — vì sau
này sẽ dùng chung bên HRM cả."

**Cách của Báo giá** (`pages/assign/quotations/_id/index.vue:1200` → `QuotationPrintPreview.vue:21`):
lấy `companies.header` rồi **dùng NGUYÊN giá trị**, không bịa host — `startsWith('http')` thì trả
thẳng, còn lại trả nguyên path. Chạy được vì DB HRM lưu header là **URL TUYỆT ĐỐI**
(`https://tanphat.s3.cloud.cmctelecom.vn/...` hoặc `https://erp.eteksofts.com/uploads/...`).

**Vì sao phiếu thu trống:** `gop_db` dùng bảng `companies` bản ERP → header là path TƯƠNG ĐỐI
`/uploads/...`, nên `headerUrl()` phải ghép `ERP_URL`; `ERP_URL` rỗng/sai là ra chuỗi rỗng → mất
logo. Cộng thêm: header lấy theo công ty NGƯỜI TẠO phiếu (ERP làm vậy), mà 133 phiếu `TPSG.*` do
NV 785 lập có `employee_infos.company_id = NULL` → mất logo dù phiếu ghi rõ `company_id = 4`.

- [x] G1 — `BillIncomePrintService::headerUrl()`: lấy công ty theo `bill_incomes.company_id` trước,
      fallback công ty người tạo (fix 133 phiếu TPSG + 364 phiếu logo lệch công ty)
- [x] G2 — Header đã là URL tuyệt đối / `data:` → trả nguyên trạng (đúng nhánh `startsWith('http')`
      của báo giá) — đã có, giữ nguyên
- [x] G3 — Header tương đối + KHÔNG có `ERP_URL` → trả **nguyên path tương đối** thay vì `''`
      (đúng nhánh `return company.header_url || h` của báo giá). Sau này HRM tự phục vụ `/uploads`
      là chạy luôn, không phải sửa code
- [x] G4 — Áp dụng cho cả bản IN và bản EXCEL (2 chỗ đều gọi `headerUrl()`)
- [x] G5 — Verify: render HTML thật + đối chiếu số phiếu ra được logo trước/sau

**CHƯA làm (phải hỏi trước vì là code dùng chung):** `BillPaymentPrintService::companyHeader()`
(Phiếu chi) và 3 bản sao cùng logic — `FormatHelper::erpCompanyHeader()`,
`AccountService::companyHeader()`, `ServiceService::companyHeader()`.

### Checkpoint - 2026-08-21 (G1-G5)
Vua hoan thanh: logo ban in + Excel phieu thu dung chung cach cua man Bao gia.
Chi sua 1 file `Modules/Finance/Services/BillIncomePrintService.php` (`headerUrl()` + 2 docblock).

Do lai tren du lieu that (2.347 phieu):

| | Truoc | Sau |
| --- | --- | --- |
| Phieu KHONG ra logo | 133 (toan bo `TPSG.*`) | **0** |
| Phieu doi logo sang dung cong ty ghi tren phieu | - | 497 |
| `ERP_URL` rong | `HEADER=''` -> mat logo | tra `/uploads/xxx.png` (trinh duyet tu phan giai) |

Kiem chung bang `render()` that: `TPV.PT0726.00057` -> `.../cn-vinh.png`,
`TPSG.PT0726.00001` (truoc trong) -> `.../tpsg.png`, `TPHP.PT0726.00020` (truoc ra logo cty 1)
-> `.../cn-hp.png`. Ban Excel dung chung `headerUrl()` nen ra y het.

**Chua kiem chung:** anh hien that tren trinh duyet - may local khong co thu muc
`erp/public/uploads` (404 moi letterhead). Tren server co ERP that
(`https://erp.eteksofts.com/uploads/...` tra 200) thi hien binh thuong.

Buoc tiep theo: user mo lai ban in tren dev de xac nhan logo hien.
Blocked: khong.

## Phase H - Chuan hoa companies.header / companies.logo thanh URL tuyet doi (2026-08-21)

**User chot:** "chuan hoa du lieu di, lam luon ca logo" - ca ERP lan HRM gio dung chung DB `gop_db`,
nen dia chi anh phai la URL DUNG DUOC O MOI DOMAIN, khong the la path tuong doi cua rieng ERP.

**Vi sao path tuong doi khong con dung:** file anh nam tren dia ERP, KHONG nam trong DB - gop DB
khong keo file sang. Do tren dev: `https://erp.eteksofts.com/uploads/<file>` tra **200**, con
`https://dev-hrm.eteksofts.com/uploads/<file>` tra **404** (`{"code":404,"message":"Route Not Found!"}`).
=> Man in mo tren domain HRM bat buoc phai co URL tuyet doi. Day cung la ly do man **Bao gia** dang
mat logo tren `gop_db` (no dung nguyen gia tri header, truoc kia chay vi DB HRM luu san URL tuyet doi).

- [x] H1 - Sinh file rollback `rollback-companies-header-logo.sql` (8 dong, gia tri cu)
- [x] H2 - `UPDATE companies SET header = CONCAT('https://erp.eteksofts.com', header) WHERE header LIKE '/uploads/%'` - 8 dong
- [x] H3 - Lam tuong tu cho cot `logo` - 8 dong
- [x] H4 - Verify lai ban in + Excel phieu thu, va anh huong sang cac man dung chung

**An toan cho ERP:** ra soat 454 cho ERP dung `company->header`, KHONG cho nao boc `asset()`/`url()`,
model `Company` khong co accessor - deu nhet thang vao `{{HEADER}}`. URL tuyet doi chay y het.
Chinh DB HRM production cung dang luu kieu nay cho cong ty id 2/3/4.

### Checkpoint - 2026-08-21 (H1-H4)
Vua hoan thanh: chuan hoa 8 dong `companies.header` + 8 dong `companies.logo` tren `gop_db` local.

Verify sau khi chuan hoa (render that, khong con ghep ERP_URL):

| Phieu | src trong ban IN va file EXCEL |
| --- | --- |
| TPV.PT0726.00057 | `https://erp.eteksofts.com/uploads/1751696460cn-vinh.png` |
| TPSG.PT0726.00001 | `https://erp.eteksofts.com/uploads/1751696416tpsg.png` |
| TPHP.PT0726.00020 | `https://erp.eteksofts.com/uploads/1751696363cn-hp.png` |

File Excel: `BillIncomeExport::drawings()` tra **1 drawing** `letterhead 549x72 @A1` - truoc khi
chuan hoa la 0 (URL `erp.test:8080` tren may local 404). Nghia la **ban Excel gio co logo ngay ca
tren local**.

**Con lai (chua lam):**
1. Dev / production phai chay 2 cau UPDATE nay tren DB that (local da chay). File rollback:
   `.plans/gop-db/finance-bill-income/rollback-companies-header-logo.sql`.
2. Van nen dat `ERP_URL=https://erp.eteksofts.com` trong `.env` cac moi truong lam luoi an toan:
   man Sua cong ty ben ERP (`CompaniesController.php:275,601`) luu thang `$request->header` tu
   file picker, tuc la ai sua lai anh cong ty se ghi de ve path tuong doi `/uploads/...`.
   Code `headerUrl()` da xu ly san truong hop do.
3. Cac ban sao cung logic chua gom: `BillPaymentPrintService::companyHeader()` (Phieu chi),
   `FormatHelper::erpCompanyHeader()`, `AccountService::companyHeader()`,
   `ServiceService::companyHeader()` - sau khi du lieu chuan hoa thi ca 4 deu tra URL tuyet doi
   nguyen trang, khong con phu thuoc ERP_URL.

Buoc tiep theo: user mo lai ban in phieu thu + man Bao gia tren dev de xac nhan logo hien.
Blocked: khong.

## Phase I — Ô "Số tiền duyệt thu" xoá trắng phải về 0 (2026-08-21)

User báo ở `finance/bill-incomes/2352/edit`: xoá hết nội dung ô **Số tiền duyệt thu** thì ô rơi về
placeholder (nhìn như chưa nhập gì), trong khi cột tiền phải luôn có số.

- [x] I1 — Nguyên nhân: `V2BaseCurrencyInput.onInput()` emit **null** khi chuỗi rỗng, `formatCurrency(null)`
      trả `''` → ô trống. (`formatCurrency(0)` trả `'0'`, nên chỉ cần giá trị là 0 thì hiện đúng.)
- [x] I2 — `BillIncomeForm.vue::onApproveChange()`: `income_money_approve` là `null`/`''` → gán `0`
      trước khi `recalcApprove()`. Không đụng `V2BaseCurrencyInput` (component dùng chung).
- [x] I3 — Verify: compile template + babel parse 0 lỗi; chạy lại đúng hàm `formatCurrency`:
      `null` → `''` (đúng triệu chứng), `0` → `'0'`, gõ tiếp `'05'` → `'5'` (không dính số 0 thừa,
      nên quy về 0 không cản việc nhập số mới).
- [ ] I4 — User mở trình duyệt xác nhận.

**Chưa đụng:** các ô tiền khác của màn (phân bổ theo phiếu xuất hàng, tỷ giá) vẫn giữ hành vi cũ —
user chỉ yêu cầu cột Số tiền duyệt thu.

## Phase J — Duyệt phiếu thu xong thì về màn danh sách (2026-08-21)

User báo ở `finance/bill-incomes/2345`: duyệt xong vẫn đứng lại màn chi tiết. Phiếu đã duyệt thì
không còn việc gì làm ở đó (nút Duyệt/Hủy biến mất theo cờ `is_can_approve`).

- [x] J1 — `_id/index.vue`: `<ApproveBillIncomeModal @approved>` đổi từ `reloadDetail` sang `onApproved()`
      → `this.$router.push('/finance/bill-incomes')`. Modal tự `close()` TRƯỚC khi emit `approved`
      nên không sót backdrop khi chuyển trang.
- [x] J2 — `onApproved()` gọi `this.$refs.form?.markFormSaved?.()` trước khi push: form con
      (`BillIncomeForm`) gắn `unsavedChangesMixin`, thiếu bước này có nguy cơ bị hỏi
      "Thông tin chưa lưu" ngay sau khi vừa duyệt.
- [x] J3 — Nhánh **409** (người khác vừa duyệt/hủy trước) GIỮ NGUYÊN `reloadDetail`: ở lại màn để
      user thấy trạng thái thật, không đá về danh sách khi thao tác không thành.
- [x] J4 — Nút **Hủy phiếu thu**: user chốt 2026-08-21 cho về danh sách luôn → `submitCancel()` gọi
      `goToList()` sau khi đóng modal, thay cho `reloadDetail()`. Tách `goToList()` dùng chung cho cả
      Duyệt và Hủy (markFormSaved + push). Nhánh 409 của Hủy vẫn ở lại + tải lại như J3.
- [x] J5 — Verify: compile template + babel parse 0 lỗi; `markFormSaved()` có thật trong
      `unsavedChangesMixin` (dòng 137) và `ref="form"` đúng là `BillIncomeForm`.
- [ ] J6 — User mở trình duyệt xác nhận.

### Task K — Bản in phiếu thu không hiện "Người nộp tiền" (2026-08-22)
User báo màn in phiếu thu (`finance/bill-incomes`) bỏ trống ô "Người nộp tiền". Không phải lỗi mẫu in:
4 mẫu 203-206 đều có placeholder `NGUOI_NOP_TIEN`. Nguyên nhân là **nguồn dữ liệu sai** —
`BillIncomePrintService` đọc `bill_income_requests.payer` (payer của phiếu ĐỀ NGHỊ) thay vì
`bill_incomes.payer` (ô kế toán nhập trên form Phiếu thu). Đây là port nguyên si lỗi ERP
(`BillIncome.php:619,683`): cột `bill_income_requests.payer` không có ô nhập nào ghi vào —
0/2.414 phiếu đề nghị thật có dữ liệu — nên bản in ra trống; phiếu nào trùng dữ liệu seed thì
in ra SAI tên người nộp.

- [x] K1 — Thêm `payerName(BillIncome $bill, $request)`: `bill_incomes.payer` trước,
      `bill_income_requests.payer` chỉ là fallback cho dữ liệu cũ, luôn trả `string` (không null).
- [x] K2 — `placeholders()` (bản in) và `excelPlaceholders()` (file Excel) cùng gọi `payerName()`.
- [x] K3 — Verify trên dữ liệu thật: `TPE.PT0826.00001` — trước in `'Người nộp 6'` (payer của phiếu
      đề nghị, dữ liệu seed), sau in `'jklljh'` (đúng ô kế toán nhập). HTML thật:
      `<td>Người nộp tiền: jklljh</td>`. 30 phiếu mới nhất: **30/30 có người nộp, 0 rỗng, 0 lỗi**
      (trước đó phụ thuộc payer của phiếu đề nghị, gần như luôn trống).
      2 nhánh fallback: phiếu thu trống → lấy phiếu đề nghị; cả hai trống → `''`, không nổ.
      `php -l` sạch. `bill_incomes.payer` rỗng 0/2.348 nên đường chính luôn có dữ liệu.
- [x] K4 — Rà phiếu chi: `BillPaymentPrintService.php:218` đã đọc `$bill->receiver` của chính phiếu
      chi → **không dính lỗi cùng loại**, không cần sửa.
- [ ] K5 — User mở trình duyệt xác nhận.

### Task L — Preview màn in phiếu thu lệch bản in ở khối "Liên số" (2026-08-22)
User báo `/finance/bill-incomes/2346/print`: khối **Liên số / Số / Nợ / Có** các dòng so le trên
màn xem trước, nhưng bấm In ra thì bình thường. Đo tận nơi (Playwright, chặn tự bật hộp thoại in
bằng cách nuốt `frame.onload`, ép iframe in về đúng bề ngang vùng in 180mm):

| | Preview (trước) | Cửa sổ in |
| --- | --- | --- |
| Bề rộng bảng Liên số | 210px (bị bóp bằng ô cha) | 263px |
| Chiều cao mỗi ô | 58px = **2 dòng** | 28px = 1 dòng |

Nguyên nhân: rule preview `#content ::v-deep td, th` có thêm `word-break: break-word` +
`overflow-wrap: break-word` — **pdf.css của ERP KHÔNG có 2 thuộc tính này**. Bảng Liên số cần 263px
mới đủ 1 dòng nhưng nằm trong ô rộng 210px của bảng cha `table-layout: fixed`; cho ngắt từ thì
`max-width: 100%` bóp được bảng lại → mã phiếu + số tiền rớt xuống 2 dòng → so le. Cửa sổ in không
cho ngắt từ nên bảng giữ nguyên bề ngang, tràn nhẹ khỏi ô đúng như ERP.

- [x] L1 — Bỏ `word-break`/`overflow-wrap` khỏi rule `td, th` của khối `<style scoped>` (giữ lại
      chú thích cảnh báo tại chỗ để lần sau không ai thêm lại).
- [x] L2 — Thêm `line-height: normal` cho `#content`: pdf.css không đặt line-height nên cửa sổ in
      dùng `normal`, còn preview thừa hưởng `1.5` của Bootstrap → mỗi dòng cao thêm ~6px.
- [x] L3 — Verify bằng số đo, preview vs iframe in ép đúng 180mm: bảng Liên số **263px ở cả hai**,
      mọi ô **28px = 1 dòng ở cả hai**, nội dung 4 dòng khớp từng chữ. Compile template + babel
      parse sạch.
- [ ] L4 — User mở trình duyệt xác nhận.

**Ghi nhận, CHƯA sửa (không phải lỗi mới):** bảng Liên số rộng 263px trong khi cột chứa nó chỉ
226px → tràn ~45px sang phải, **giống hệt nhau ở cả preview lẫn bản in** vì mẫu 203-206 khai cứng
như vậy. Sửa tận gốc phải đụng `report_templates` (dùng chung với cổng ERP) → chờ user quyết.

### Task M — Mã phiếu đề nghị thu ở danh sách phiếu thu mở TAB MỚI (2026-08-22)
User yêu cầu: ở `finance/bill-incomes`, bấm vào ô **Mã phiếu đề nghị thu tiền** thì mở tab mới.
Khớp ERP — `BillIncomeController.php:60` render ô này với `target="_blank"`.

- [x] M1 — `pages/finance/bill-incomes/index.vue`, slot `#cell-requestCode`: thêm `target="_blank"`
      + `rel="noopener"` cho `<nuxt-link>`. vue-router (`guardEvent`) tự bỏ qua click khi thẻ có
      `target="_blank"` nên trình duyệt điều hướng thật, không chuyển trang trong SPA.
- [x] M2 — Ô **Mã phiếu thu** (`#cell-code`) GIỮ NGUYÊN điều hướng trong tab hiện tại: đó là phiếu
      của chính màn này, ERP cũng không để `_blank`.
- [x] M3 — Verify trên trình duyệt thật (localhost:3000): 10/10 link mã phiếu đề nghị render
      `target="_blank" rel="noopener"`; bấm thử `TPV.DNTT0726.00054` → mở tab mới
      `/finance/bill-income-requests/2436`, tab danh sách phiếu thu đứng yên (không mất bộ lọc).
      Link mã phiếu thu vẫn `target = null` như cũ.
- [ ] M4 — User xác nhận.


### Checkpoint — 2026-08-22 (đợt sửa theo phản hồi user)
Vừa hoàn thành: **Task K, L, M** (nhánh `gop_db`, chưa commit).
· K — bản in/Excel phiếu thu bỏ trống "Người nộp tiền": đọc nhầm `bill_income_requests.payer`
  (0/2.414 phiếu thật có dữ liệu) thay vì `bill_incomes.payer`. Thêm `payerName()` dùng chung cho
  `placeholders()` + `excelPlaceholders()`. 30/30 phiếu mới nhất giờ có người nộp.
· L — preview màn in lệch bản in ở khối "Liên số": bỏ `word-break/overflow-wrap` (pdf.css ERP không
  có) + đặt `line-height: normal`. Đo lại: bảng 263px và ô 28px **giống hệt** ở cả preview lẫn bản in.
· M — mã phiếu đề nghị ở danh sách phiếu thu mở **tab mới** (`target="_blank"`, khớp ERP).
Đang làm dở: không có.
Bước tiếp theo: user xác nhận trên trình duyệt (K5 · L4 · M4).
Blocked: không. Ghi nhận chưa sửa: bảng "Liên số" tràn ~45px khỏi cột — giống nhau ở ERP, sửa tận
gốc phải đụng `report_templates` dùng chung 2 cổng.

## Phase N — Bản in tràn khỏi lề phải (2026-08-22)

**User báo:** "màn phiếu thu phần in đang bị tràn ra lề".

**Cách đo (không cần đăng nhập):** render HTML in thật của 1 phiếu mỗi mẫu bằng
`BillIncomePrintService::render()` qua tinker, dựng lại đúng môi trường cửa sổ in
(`static/css/pdf-erp.css` + `printBaseStyles()` lấy thẳng từ `print.vue`), ép body đúng bề ngang
vùng in **180mm = 680px** (A4 210mm − lề trái 20mm − lề phải 10mm), chạy Chromium headless và so
`getBoundingClientRect().right` của mọi phần tử với mép phải trang.

**Kết quả đo TRƯỚC khi sửa:**

| Mẫu | Phần tử tràn | Tràn |
| --- | --- | --- |
| 203 | bảng "Liên số / Số / Nợ / Có" (rộng 264px) | **44.8px ≈ 11.8mm** |
| 204 | như trên (272px) | **52.8px ≈ 14mm** |
| 205 | như trên (264px) + hàng chữ ký (688px) | **44.8px** / 7.2px |

Tràn 12-14mm **vượt cả lề phải 10mm** → máy in cắt mất, đúng triệu chứng user thấy.

**Root cause:** `{{LIEN}}` là bảng nằm trong **ô cuối** của bảng đầu trang (`table-layout: fixed`,
3 cột đều nhau ⇒ ô 227px, trừ padding còn **211px**), nhưng nội dung cần 264-272px ở cỡ chữ 16px.
Không nới cột được: muốn tiêu đề "PHIẾU THU" còn nằm **giữa trang** thì 2 cột hai bên phải bằng
nhau, mà cột giữa cần ~225px cho dòng "Ngày … Tháng … Năm …" ⇒ 227px đã là mức tối đa.
Đã đo và loại 3 phương án khác: `table-layout: auto` (hết tràn nhưng tiêu đề lệch trái 340px→173px),
`word-break` (bảng bị bóp còn 211px, mọi hàng rớt 2 dòng — đúng cái user bác ngày 2026-08-22),
giảm padding đơn thuần (vẫn tràn 14-23px).

- [x] N1 — Khối Liên số: `font-size: 12px`, `padding: 0 2px`, `margin: 0 -8px` (lấy lại padding
      của ô chứa), `white-space: nowrap` để mỗi hàng giữ 1 dòng
- [x] N2 — Hàng chữ ký mẫu 205 (6 ô nowrap, rộng 688px): siết `table.block td` padding còn 2px
- [x] N3 — Áp cả `printBaseStyles()` (bản in) lẫn `<style scoped>` (preview) để xem trước khớp in

**Đo lại SAU khi sửa — tràn = 0px ở cả 3 mẫu**, mỗi hàng của khối Liên số vẫn 1 dòng (cao 60px).
Kiểm thêm 2 ca biên dựng từ dữ liệu thật: mã phiếu dài nhất trong DB (**21 ký tự**,
`DTTDETEK.PT0326.00001`, 13 phiếu) + số tiền lớn nhất (**877.651.200**) → **tràn 0px**.
Ca giả định 1,2 tỷ (chưa từng có) tràn 9px ≈ 2,4mm — vẫn nằm trong lề 10mm, không bị cắt.

### Checkpoint — 2026-08-22 (N1-N3)
Vừa hoàn thành: bản in phiếu thu hết tràn lề phải (đo bằng Chromium headless, không cần đăng nhập).
Đang làm dở: không.
Bước tiếp theo: user mở bản in xác nhận cỡ chữ khối Liên số 12px có chấp nhận được không.
Chưa kiểm chứng bằng mắt: chỉ đo hình học, chưa xem thẩm mỹ trên trình duyệt.
Blocked: không.

### Sửa lại Phase N — trả khối Liên số về cỡ chữ 16px của ERP (2026-08-22)

**User phản hồi:** "sao lại cho font chữ ở chỗ liên số nhỏ vậy?" — đúng. Bản N1 thu nhỏ CẢ KHỐI
xuống 12px chỉ để cover 13 phiếu mã 21 ký tự (0,55% dữ liệu), làm xấu 2.335 phiếu còn lại.

**Đo lại từng ô mới thấy:** thứ duy nhất không vừa 211px là **MÃ PHIẾU** — nó nằm ở cột giữa
vốn hẹp (cột này còn phải chứa số tài khoản). Các ô còn lại (Liên số / Nợ / Có / số tiền) vừa
thoải mái ở 16px.

- [x] N5 — Bỏ `font-size: 12px` trên cả khối → giữ nguyên 16px của ERP
- [x] N6 — Chỉ ô mã phiếu: `font-size: 12px` + cho phép xuống dòng (`word-break: break-all`)

Đã sweep cỡ chữ ô mã phiếu để chọn: **12px** là mức lớn nhất mà mã 16/17 ký tự vẫn nằm gọn
1 dòng ở CẢ 6 mẫu. Từ 13px trở lên thì mẫu 204 (nhiều khách hàng, cột tài khoản dài hơn) đã bị
xuống dòng. Chỉ 13 phiếu mã 21 ký tự (DTTDETEK) xuống 2 dòng — thay vì chạy ra khỏi trang.

Đo lại toàn bộ: **tràn = 0px** ở 203/204/205/211/217/236 + 2 ca biên; khối Liên số `font=16px`,
riêng ô mã phiếu `font=12px`.

---

## Phase O — Bỏ nút "Hủy phiếu" ở màn danh sách (2026-08-24)

**Yêu cầu user:** ở danh sách, nút "Duyệt" và "Hủy phiếu" đều chỉ điều hướng sang màn chi tiết rồi
mới thao tác thật → bỏ hẳn "Hủy phiếu" khỏi danh sách. Màn chi tiết giữ nguyên đầy đủ Duyệt/Hủy.

Phạm vi: chỉ FE, 1 file `hrm-client/pages/finance/bill-incomes/index.vue`. Không đụng BE
(API hủy + cờ `is_can_approve` giữ nguyên), không đụng màn chi tiết.

- [x] O1 — Xóa mục `key: 'cancel'` ("Hủy phiếu") trong `getRowActions()`
- [x] O2 — Bỏ `case 'cancel'` trong `handleRowAction()`, sửa 2 comment ghi "6 hành động" /
      "Duyệt, Hủy phiếu" cho khớp thực tế
- [x] O3 — Verify: parse lại file bằng `vue-template-compiler` + đọc lại diff

### Checkpoint — 2026-08-24 (O1-O3)
Vừa hoàn thành: bỏ nút "Hủy phiếu" khỏi cột thao tác màn danh sách Phiếu thu
(`hrm-client/pages/finance/bill-incomes/index.vue`, -13/+6 dòng). Danh sách còn 5 thao tác:
Sửa, Xóa, Duyệt, In, Xuất Excel. Màn chi tiết + BE không đụng gì.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt xác nhận menu "…" của dòng phiếu không còn "Hủy phiếu".
Chưa kiểm chứng bằng mắt: chỉ parse template + script (vue-template-compiler / babel), chưa mở trình duyệt.
Blocked: không.

## Đồng nhất icon nút Duyệt (2026-08-27)

- [x] **FE-x** `pages/finance/bill-incomes/index.vue` — cột hành động: icon "Duyệt" đổi
      `ri-check-line` → `ri-checkbox-circle-line` cho giống `finance/prepick-cancel-requests` và
      `finance/bill-payments`. Chỉ đổi icon; vị trí nút, chữ, cờ `is_can_approve` và nút
      "Duyệt phiếu thu" ở màn chi tiết giữ nguyên (màn chi tiết dùng `ri-check-line` đúng chuẩn
      V2Footer).

### Checkpoint — 2026-08-27
Vừa hoàn thành: đồng nhất icon nút Duyệt ở cột hành động màn danh sách phiếu thu.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-incomes` xem lại icon trong menu ⋮.
Chưa kiểm chứng bằng mắt: chỉ compile template + script, chưa mở trình duyệt.
Blocked: không.

## Bỏ popup duyệt — nhập số thực thu inline như ERP (2026-08-27)

User hỏi lại vì sao HRM bấm Duyệt lại bật popup nhập "Số tiền thực thu" trong khi ERP không có.
**Đối chiếu ERP (`D:\laragon\www\erp`)**: trường này ERP CÓ, nhưng không phải popup —

| Nơi | Code ERP | Hành vi |
| --- | --- | --- |
| Cột "Số tiền thực thu" trong bảng chi tiết màn xem phiếu | `resources/views/income_expenditure/bill_incomes/formShow.blade.php:267-273` | Thành **ô nhập tại chỗ** khi có quyền `Thủ quỹ duyệt phiếu thu` **và** phiếu đang Chờ duyệt; ngoài ra chỉ hiện chữ |
| Nút "Duyệt phiếu thu" | `show.blade.php:18-21` + `submitAndApprove()` :100-103 | Chỉ set `status = 3` rồi PUT cả form — không popup |
| BE bắt buộc | `BillIncomeUpdateRequest.php:38` — `income_money_real` `requiredIf(status == 3)` | ERP không cho duyệt nếu bỏ trống thực thu |

→ Nghiệp vụ 2 bên giống nhau, chỉ khác UX. User chốt **bỏ popup, chuyển sang nhập inline như ERP**.

- [x] **FE-1** `components/BillIncomeForm.vue` — thêm nhóm cột `Số tiền thực thu` (+ cột quy đổi VND
      khi ngoại tệ) vào bảng chi tiết, CHỈ hiện ở chế độ `readonly` (màn xem) đúng như ERP chỉ có ở
      `formShow`. Ô nhập khi cờ BE `is_can_approve` (cờ `billCanApprove` fail-closed, mặc định
      `false`), còn lại hiện chữ. `totalCols` + dòng Tổng cộng tính thêm cột mới.
- [x] **FE-2** `BillIncomeForm.vue` — giữ `id` dòng chi tiết khi nạp (payload duyệt cần
      `details.*.id`); điền sẵn thực thu `= income_money_approve` khi ô đang 0; `onRealChange()` /
      `recalcReal()` (xóa trắng → 0, quy đổi VND theo tỷ giá, watch tỷ giá tính lại).
- [x] **FE-3** `BillIncomeForm.vue` — 3 hàm cho màn chi tiết gọi qua ref: `approveDetails()`,
      `validateApproveDetails()`, `applyApproveErrors()`. Lỗi hiện inline dưới ô sai.
- [x] **FE-4** `_id/index.vue` — nút "Duyệt phiếu thu" gọi thẳng `approveBill()` (`$confirm` →
      `POST /{id}/approve`), chống double-submit bằng `approving` + `interactable`, `$safeLoadingStart/Finish`;
      giữ nguyên xử lý 409 (tải lại) / 403 (toast) / 422 (map inline).
- [x] **FE-5** Xóa `components/ApproveBillIncomeModal.vue` (không còn nơi dùng — đã grep toàn `pages/`
      + `components/`).
- [x] **BE** KHÔNG đổi: endpoint `POST /{id}/approve` + `BillIncomeApproveRequest` giữ nguyên.

**Verify (HTTP kernel + JWT, transaction rồi rollback — phiếu 2355 `TPE.PT0826.00004` về đúng
status 2 / thực thu 0 / 972.042 bút toán như trước):**

| Luồng | Kết quả |
| --- | --- |
| GET phiếu 2355 | 200 · status 2 (Chờ duyệt) · `is_can_approve = true` · 1 dòng: duyệt thu 4.540, thực thu 0 |
| POST `/2355/approve` payload y hệt FE mới gửi | **200** "Duyệt phiếu thu thành công!" · status → 3 · ghi `income_money_real = 4540` · sinh **2 bút toán** |
| POST `/2355/approve` thiếu số thực thu | **422** `details.0.income_money_real: Bắt buộc nhập` — đúng key mà ô inline đang bắt |
| Compile FE | `_id/index.vue` · `BillIncomeForm.vue` · `_id/edit.vue` · `create.vue` — template + script sạch 4/4 |

### Checkpoint — 2026-08-27
Vừa hoàn thành: bỏ popup duyệt phiếu thu, chuyển ô "Số tiền thực thu" vào bảng chi tiết màn xem
(đúng ERP); xóa `ApproveBillIncomeModal.vue`.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-incomes/2355` bấm Duyệt phiếu thu để xác nhận luồng mới.
Chưa kiểm chứng bằng mắt: FE chỉ compile, chưa mở trình duyệt; BE đã gọi thật 3 luồng.
Blocked: không.

## 🐛 Cột "Số tiền" ở danh sách lệch ERP sau khi duyệt (2026-08-27)

User báo: danh sách HRM hiện **số thực thu** cho phiếu đã duyệt, ERP hiện **số duyệt thu**
(dẫn chứng `erp-crm.eteksofts.com/.../bill_incomes/2374/show` — danh sách 22.000.000).

**Nguyên nhân — đọc công thức ERP mà không đọc THỨ TỰ GỌI:**
`BillIncome::syncDetails()` :347-351 của ERP có 2 vế (`status 1/2` → duyệt thu · `status 3` → thực
thu). Nhưng `BillIncomeController::update()` gọi `syncDetails()` ở **:199 — TRƯỚC**
`$bill_income->update($data)` ở **:201**, nên lúc cộng tiền `$this->status` vẫn là trạng thái CŨ
(2 = Chờ duyệt) → luôn rơi vào vế duyệt thu. Phiếu đã ở status 3 thì :195-197 chặn thẳng
("Phiếu thu tiền đã được duyệt!"). ⇒ **nhánh status 3 là code chết, `sum_money` bên ERP LUÔN là
tổng duyệt thu.**

HRM `BillIncomeApprovalService::approve()` bước 7 lại chủ động tính lại
`sum_money = SUM(income_money_real_exchange)` → lệch.

**Đo dữ liệu thật** (5 phiếu đã duyệt có duyệt thu ≠ thực thu — số còn lại 2 vế bằng nhau nên không
lộ được lỗi):

| id | Mã phiếu | Lập lúc | sum_money | Duyệt thu | Thực thu | Đang theo vế |
| --- | --- | --- | --- | --- | --- | --- |
| 295 | TPE.PT0925.00039 | 2025-09-15 | 8.424.000 | 8.424.000 | 4.212.000 | DUYỆT THU ✔ |
| 1008 | TPE.PT1225.00058 | 2025-12-23 | 19.882.800 | 19.882.800 | 1.988.280 | DUYỆT THU ✔ |
| 1082 | TPE.PT1225.00096 | 2025-12-31 | 877.651.200 | 877.651.200 | 87.635.120 | DUYỆT THU ✔ |
| 2354 | TPE.PT0826.00003 | 2026-08-27 | 300.600.000 | 470.820.000 | 300.600.000 | **THỰC THU ✘** |
| 2356 | TPE.PT0826.00005 | 2026-08-27 | 41.000.000 | 50.000.000 | 41.000.000 | **THỰC THU ✘** |

3 phiếu ERP lập năm 2025 giữ vế duyệt thu; đúng 2 phiếu duyệt bằng HRM hôm nay bị lệch.

- [x] **BE-1** `BillIncomeApprovalService::approve()` — **bỏ bước 7** (không tính lại `sum_money`),
      thay bằng khối comment ghi lại bằng chứng thứ tự gọi của ERP + số liệu đo, kèm cảnh báo đừng
      "sửa lại cho đúng công thức".
- [x] **BE-2** `BillIncomeWriteService::syncDetails()` — đính chính docblock: nhánh `status 3` là
      code chết bên ERP, `sum_money` luôn = tổng duyệt thu; cột này còn là cột 2 ô lọc tiền + sort.
- [x] **DATA** 2 phiếu 2354 · 2356 đang giữ `sum_money` = thực thu → **user chốt 2026-08-27: KHÔNG
      sửa**, để nguyên số cũ, chỉ cần phiếu duyệt từ nay trở đi hiện đúng. Danh sách vẫn hiện
      300.600.000 / 41.000.000 cho 2 phiếu này (đúng ra là 470.820.000 / 50.000.000) — đây là dữ
      liệu cũ, KHÔNG phải lỗi code còn sót.

**Verify (HTTP kernel + JWT, transaction rồi rollback — phiếu 2355 về đúng status 2 / sum_money 8.989,2):**

| Luồng | Kết quả |
| --- | --- |
| Duyệt phiếu 2355 với thực thu = **một nửa** duyệt thu (2.270 vs 8.989,2) | 200 · status → 3 · `sum_money` **giữ nguyên 8.989,2 = DUYỆT THU** (trước khi sửa sẽ thành 2.270) |
| API danh sách sau khi duyệt | `sum_money_text = 8,989` — đúng vế duyệt thu |

### Checkpoint — 2026-08-27
Vừa hoàn thành: sửa lệch cột "Số tiền" ở danh sách phiếu thu — duyệt phiếu KHÔNG còn tính lại
`sum_money` theo vế thực thu, giữ đúng hành vi ERP.
Đang làm dở: không.
Bước tiếp theo: user mở màn danh sách phiếu thu xác nhận phiếu duyệt MỚI hiện đúng tổng duyệt thu
(2 phiếu 2354 · 2356 giữ số cũ theo quyết định của user).
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; BE đã gọi thật.
Blocked: không.

## Bổ sung "Phân bổ nhanh" số tiền thực nhận (2026-08-27)

User thấy bên ERP màn duyệt có ô *Số tiền phân bổ* + nút *Phân bổ* mà HRM không có, yêu cầu bổ sung.

**Chức năng ERP** (`bill_incomes/formShow.blade.php:143-161`, logic ở
`partials/classes/IncomeExpenditure/BillIncome.blade.php:107-119`): thủ quỹ gõ TỔNG số tiền thực tế
nhận được rồi bấm Phân bổ → rải xuống cột "Số tiền thực nhận" theo thứ tự trên xuống, mỗi dòng lấy
`min(số duyệt thu, số còn lại)`. Dùng khi khách trả THIẾU, khỏi bấm máy tính chia tay từng dòng.
Thuần FE — không gọi API, số chỉ xuống DB khi bấm Duyệt. Hiện cùng điều kiện với ô nhập thực thu
(quyền *Thủ quỹ duyệt phiếu thu* + phiếu Chờ duyệt).

- [x] **FE-1** `BillIncomeForm.vue` — khối *Số tiền phân bổ* (`V2BaseCurrencyInput`) + nút *Phân bổ*
      (`V2BaseButton secondary`, icon `ri-list-check-2`) ngay trên bảng chi tiết, `v-if="canApproveBill"`.
- [x] **FE-2** `allocateRealMoney()` port `BillIncome.allocated()`; mỗi dòng gọi `recalcReal()` +
      `clearFieldError()` để cột quy đổi VND và lỗi inline cập nhật theo.
- [x] **FE-3** Import + đăng ký `V2BaseButton` (form này trước đó chưa dùng nút nào ngoài V2Footer).

🔶 **LỆCH ERP 1 ĐIỂM CÓ CHỦ Ý:** ERP `if (allocate_money === 0) return` chỉ thoát khi còn ĐÚNG 0, nên
các dòng phía sau **giữ nguyên số thực thu cũ**. Ở HRM số đó đã được điền sẵn = duyệt thu, nên phân
bổ 10tr cho phiếu 35tr sẽ vẫn ra tổng 35tr — sai ý người dùng. HRM ghi `0` cho các dòng không còn
tiền. (Bên ERP số cũ thường là 0 nên không lộ ra khác biệt.)

**Verify — chạy chính vòng lặp đã port với 2 dòng của phiếu trong ảnh (16.750.000 + 19.100.000):**

| Số tiền phân bổ | Dòng 1 | Dòng 2 | Tổng |
| --- | --- | --- | --- |
| 35.850.000 (thu đủ) | 16.750.000 | 19.100.000 | 35.850.000 |
| 20.000.000 (thu thiếu) | 16.750.000 | 3.250.000 | 20.000.000 |
| 10.000.000 | 10.000.000 | 0 | 10.000.000 |
| 40.000.000 (gõ dư) | 16.750.000 | 19.100.000 | 35.850.000 — không vượt số duyệt thu |
| 0 | 0 | 0 | 0 |

Compile `BillIncomeForm.vue`: template + script sạch.

### Checkpoint — 2026-08-27
Vừa hoàn thành: bổ sung ô "Số tiền phân bổ" + nút "Phân bổ" ở màn duyệt phiếu thu (port ERP).
Đang làm dở: không.
Bước tiếp theo: user mở màn chi tiết 1 phiếu Chờ duyệt, gõ số rồi bấm Phân bổ xem cột thực thu.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; logic phân bổ đã chạy thử bằng Node với số thật.
Blocked: không.

## Chặn thực thu vượt duyệt thu (2026-08-27)

User: ô "Số tiền thực thu" gõ lớn hơn số duyệt thu thì kéo về bằng duyệt thu, giống ERP.
Đối chiếu ERP `resources/views/partials/classes/IncomeExpenditure/BillIncomeDetail.blade.php:66-72`
— setter `income_money_real` làm đúng vậy:
`if (this._income_money_real > this._income_money_approve) this._income_money_real = this._income_money_approve;`
(Cùng file :15-19 cũng xác nhận luật điền sẵn: màn xem + phiếu chưa duyệt → `income_money_real = income_money_approve`.)

- [x] **FE** `BillIncomeForm.vue` — thêm `clampReal(detail)` gọi trong `onRealChange()`: `> duyệt thu`
      → kéo về đúng bằng duyệt thu, `< 0` → 0 (khớp `min:0` của `BillIncomeApproveRequest`, cùng
      khuôn `BillPaymentForm::clampApprove()`). So sánh trong cùng đơn vị NGOẠI TỆ; cột VND vẫn do
      `recalcReal()` quy đổi.
- [x] **BE** KHÔNG đổi — ERP cũng chỉ chặn ở FE (`BillIncomeStoreRequest` chỉ có `numeric|min:0`),
      HRM giữ nguyên `BillIncomeApproveRequest`. Ai gọi thẳng API vẫn ghi được số lớn hơn duyệt thu,
      **đúng bằng hành vi ERP** — muốn siết thì phải chốt riêng vì lệch ERP.

### Checkpoint — 2026-08-27
Vừa hoàn thành: chặn ô "Số tiền thực thu" vượt số duyệt thu ở màn chi tiết phiếu thu.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-incomes/2344` (duyệt thu 10.000.000) gõ thử số lớn hơn.
Chưa kiểm chứng bằng mắt: chỉ compile template + script, chưa mở trình duyệt.
Blocked: không.

### Sửa tiếp — ô vẫn hiện số to hơn trần (2026-08-27, cùng ngày)

User báo: kẹp rồi mà **vẫn gõ được số to hơn**. Đúng — bản kẹp đầu tiên (`clampReal()` ở handler
`@input` của màn) chỉ sửa được DỮ LIỆU, không sửa được Ô HIỂN THỊ:

`V2BaseCurrencyInput` giữ chuỗi hiển thị riêng (`displayValue`) và chỉ vẽ lại khi **giá trị ngoài
đổi** (watcher `currentValue` :58-64). Ô này mở ra đã điền sẵn ĐÚNG BẰNG số duyệt thu, nên khi gõ
thêm, cha kẹp về đúng giá trị ô **đang giữ** → Vue coi là "không đổi" → watcher không chạy →
`displayValue` vẫn là chuỗi vừa gõ. Rời ô thì `onBlur` mới vẽ lại đúng. Tức số gửi đi khi bấm Duyệt
vẫn đúng, chỉ hiển thị sai — nhưng không đạt yêu cầu.

**Cách sửa (user duyệt 2026-08-27 vì đụng component dùng chung):** kẹp NGAY TRONG ô nhập, giống ERP
kẹp trong setter của model (`BillIncomeDetail.blade.php:66-72`).

- [x] **FE-chung** `components/V2BaseCurrencyInput.vue` — thêm prop **`max`** (mặc định `null` =
      không giới hạn, **thuần thêm**, màn không khai thì hành vi y nguyên) + hàm `clampToMax()`.
      `onInput()` kẹp trước nhánh "gõ dở thập phân", tự đặt `displayValue` + `event.target.value` +
      emit số đã kẹp ⇒ KHÔNG phụ thuộc watcher/re-render nữa.
- [x] **FE** `BillIncomeForm.vue` — ô "Số tiền thực thu": `:max="Number(detail.income_money_approve || 0)"`.
      Giữ `clampReal()` làm lớp phòng thủ cho giá trị đặt bằng code (không qua bàn phím).
- [x] **FE** `BillPaymentForm.vue` + `BillPaymentAuthorizationForm.vue` — ô "Số tiền duyệt chi" khai
      `:max="Number(detail.payment_money_request || 0)"`: 2 màn này dính **đúng cùng bệnh** (cũng kẹp
      ở handler cha, cũng điền sẵn bằng trần), chỉ chưa ai báo.

**Verify — chạy thẳng `onInput()` trên Node** (không cần trình duyệt; script:
`scratchpad/test_max.js`, nạp SFC bằng `vue-template-compiler` rồi gọi method với event giả):

| Ca | Gõ | Ô hiện | Emit |
| --- | --- | --- | --- |
| **Ô đang = đúng trần rồi gõ thêm số** (ca user báo) | `100000000` | `10,000,000` | 10000000 |
| Ô đang nhỏ hơn trần, gõ vượt | `50000000` | `10,000,000` | 10000000 |
| Gõ đúng bằng trần | `10000000` | `10,000,000` | 10000000 |
| Gõ nhỏ hơn trần | `9000000` | `9,000,000` | 9000000 |
| Xóa trắng ô | `` | `` (rỗng) | null |
| Gõ dở phần thập phân dưới trần | `123.` | `123.` | 123 |
| Vượt trần khi đang gõ thập phân | `50000000.` | `10,000,000` | 10000000 |
| **KHÔNG khai `max`** → hành vi cũ | `999999999` | `999,999,999` | 999999999 |
| `max = 0` (dòng chưa có số duyệt) | `5000` | `0` | 0 |

9/9 ca đúng. Đã grep toàn `pages/` + `components/`: chỉ 3 chỗ vừa thêm là có truyền `max` cho
`V2BaseCurrencyInput` → không đụng màn nào khác.

### Checkpoint — 2026-08-27 (cuối phiên)
Vừa hoàn thành: kẹp trần ô tiền ngay trong `V2BaseCurrencyInput` (prop `max`) — sửa tận gốc lỗi
"gõ vẫn ra số to hơn"; áp cho 3 ô của Phiếu thu / Phiếu chi / Ủy nhiệm chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-incomes/2344` gõ quá 10.000.000 xem ô có bật về ngay không.
Chưa kiểm chứng bằng mắt: chưa mở trình duyệt; đã chạy `onInput()` thật trên Node 9/9 ca.
Blocked: không.

### Màn in — dòng "Ngày …" đầu phiếu bị xuống 2 dòng (2026-08-27)

Phát hiện ở màn Phiếu chi (user báo qua ảnh), rà sang Phiếu thu thì dính y hệt. Đo bằng Chromium
headless ở đúng bề ngang vùng in (180mm = 680px), trên phiếu thật đại diện **cả 4 mẫu**
203/204/205/206 (`BillIncomePrintService::render()` của các phiếu id 2343 / 2357 / 2355 / 2356):

| Mẫu | span "Ngày … Tháng … Năm …" trước | sau |
| --- | --- | --- |
| 203 (bán hàng, 1 KH) | `lines=2` | `lines=1` |
| 204 (bán hàng, nhiều KH) | `lines=2` | `lines=1` |
| 205 (nhà cung cấp, 1 NCC) | `lines=2` | `lines=1` |
| 206 (nhà cung cấp, nhiều NCC) | `lines=2` | `lines=1` |

- [x] **FE** `pages/finance/bill-incomes/_id/print.vue` — thêm rule vào **CẢ 2 nơi**
      (`printBaseStyles()` cho cửa sổ in **và** `<style scoped>` cho preview):
      `table.no-border[style*="table-layout"] > tbody > tr > td:nth-child(2)` → `white-space: nowrap`
      + bỏ padding ngang. Ô giữa 227px, trừ padding 8px×2 của pdf.css còn 211px, chuỗi ngày cỡ 18px
      cần 214px → gãy dòng. Bỏ padding là vừa, **giữ nguyên cỡ 18px của ERP**.
      Đã loại phương án `table-layout: auto` (đo ở màn Phiếu chi: cột trái co còn 32px, tiêu đề hết
      nằm giữa trang).
      Rule bám `td:nth-child(2)` nên **không đụng bảng "Liên số / Số / Nợ / Có"** — bảng đó ở ô thứ
      ba; đo lại sau khi sửa: vẫn 211px, `overflowRight = -16` y như trước.
      Đo ở 620 và 680px, cả 4 mẫu: `overflowRight = 0`.

**KHÔNG dính lỗi nhãn hàng ký** (khác màn Phiếu chi): mẫu 203-206 chỉ có MỘT dòng nhãn nên
`table.block td { white-space: nowrap }` đặt từ 2026-08-20 đã đủ — đo ra cả 5-6 nhãn `labelLines=1`.
Bên Phiếu chi ô ký có 3 dòng nên phải nowrap riêng span nhãn 15px, xem
`.plans/gop-db/finance-bill-payment/plan.md`.

### Checkpoint — 2026-08-27
Vừa hoàn thành: sửa dòng "Ngày …" đầu phiếu ở màn in phiếu thu (bản in + preview khớp nhau).
Đang làm dở: không.
Bước tiếp theo: user mở màn in 1 phiếu thu xem lại dòng ngày dưới chữ "PHIẾU THU".
Chưa kiểm chứng bằng mắt: đo bằng Chromium headless trên cả 4 mẫu + compile
(vue-template-compiler / babel / node-sass), chưa mở trình duyệt thật.
Blocked: không.


## Đợt sửa — Số tiền thực thu vượt Số tiền duyệt thu: báo lỗi + chặn duyệt (2026-08-28)

User: *"tương tự sửa màn phiếu thu cũng bị lỗi đó, khi nhập số lớn hơn thì cảnh báo và không cho lưu"*
(làm sau khi sửa y hệt cho ô "Số tiền duyệt chi" màn Ủy nhiệm chi — xem
`.plans/gop-db/finance-bill-payment-authorization/plan.md`).

Hiện trạng: ô **Số tiền thực thu** (thủ quỹ gõ ở màn Chi tiết khi duyệt) bị kẹp CỨNG ở 2 lớp —
prop `:max` của `V2BaseCurrencyInput` (kẹp ngay lúc gõ, `:113-124`) và `clampReal()`. Giống hệt ERP:
setter `income_money_real` của `BillIncomeDetail.blade.php` :66-72 gán thẳng
`_income_money_real = _income_money_approve` khi vượt. Số người dùng gõ biến mất không lời giải thích.

- [x] **FE** `bill-incomes/components/BillIncomeForm.vue` — bỏ prop `:max`; `clampReal()` chỉ còn
      chặn số ÂM (giữ khớp luật `min:0` của `BillIncomeApproveRequest`).
- [x] **FE** thêm `isRealOverApprove(detail)` + `realErrorText(detail, index)`: ô `:invalid` -> viền
      đỏ, chữ đỏ dưới ô *"Không được lớn hơn số tiền duyệt thu (<số>)"*, hiện NGAY LÚC GÕ.
      Chỉ so khi duyệt thu > 0 (duyệt thu 0 đồng thì không có mốc). So trong CÙNG đơn vị nguyên tệ —
      cột VND là cột quy đổi, đừng đem ra so.
- [x] **FE** `validateApproveDetails()` thêm nhánh chặn -> `_id/index.vue::approveBill()` KHÔNG gọi
      API, mixin cuộn về ô sai (cùng khuôn 2 luật "Bắt buộc nhập" / "Không được âm" đã có).
- [x] **BE** `BillIncomeApproveRequest` + luật closure `realNotOverApproveRule()`.
      ⚠️ **Mốc so KHÔNG nằm trong payload**: lệnh duyệt chỉ gửi `id` + `income_money_real`, còn
      `income_money_approve` là số đã chốt trong DB ⇒ không dùng được `lte:` (luật đó chỉ so field
      trong CÙNG payload, và ném `InvalidArgumentException` -> **500** khi field vắng mặt). Phải tự
      đọc `bill_income_details`, nạp MỘT lần cho cả mảng (`approveLimit()`), không truy vấn từng dòng.
      Nới `+0.01` để không bắt lỗi vì sai số làm tròn của `double(16,2)`. `id` không có trong DB ->
      bỏ qua luật (để service xử, câu `update` kèm `parent_id` sẽ không khớp dòng nào).

**Verify (tinker, dựng `Validator` thật từ FormRequest, trên dòng chi tiết THẬT id=28,
duyệt thu = 1.666.500):** vượt +1 -> *"Không được lớn hơn số tiền duyệt thu"* · bằng -> không lỗi ·
thấp hơn -> không lỗi · âm -> *"Không được âm"* · id không tồn tại -> không lỗi (không nổ 500).
`php -l` sạch · template parse sạch · 3 hàm mới đều nằm đúng trong `methods`, không trùng tên ·
grep xác nhận đã hết `:max` trên ô thực thu. ⚠️ Chưa mở trình duyệt.

📌 Ô **"Số tiền duyệt thu"** KHÔNG đụng tới: nó vốn không bị kẹp (ERP cũng không kẹp duyệt thu theo
đề nghị thu), user chỉ nói về ô đang tự nhảy số.

### Checkpoint — 2026-08-28
Vừa hoàn thành: ô Số tiền thực thu cho gõ vượt, báo đỏ dưới ô và chặn duyệt ở cả FE lẫn BE.
Đang làm dở: không.
Bước tiếp theo: user mở 1 phiếu thu đang "Chờ duyệt" bằng tài khoản thủ quỹ, gõ số thực thu lớn hơn
số duyệt thu -> phải thấy viền đỏ + chữ đỏ, bấm "Duyệt phiếu thu" phải KHÔNG gọi API.
Blocked: không.


## Phase L — Lịch sử thay đổi phiếu thu (user yêu cầu 2026-09-03)

User: *"bổ sung chức năng lịch sử thay đổi màn phiếu thu, làm theo skill và màn danh sách khách hàng"*.

Chốt với user trước khi code (skill `entity-history` §0):
- **Phạm vi**: đầy đủ như màn Phiếu báo có — Tạo mới · Thay đổi thông tin · Bảng chi tiết theo
  TỪNG DÒNG · Duyệt · Hủy (kèm lý do) · Xóa. (Không theo bản rút gọn của Phiếu chi tiền
  `bill_payments` — màn đó chỉ log trạng thái.)
- **Số thực thu lúc thủ quỹ Duyệt**: CÓ log, tách 2 dòng (`change_status` + `update`) theo §3a.
- **Quyền xem**: không gắn quyền riêng — ai vào được màn thì xem được (mặc định của skill).

Không có migration: dùng bảng CHUNG `catalog_histories` + trait `LogsCatalogHistory`, đúng cách 4
phiếu tài chính chị em đã làm (`bill_income_requests`, `bill_income_reports`,
`bill_payment_requests`, `bill_adjust_dept_requests`).

### BE

- [x] `app/Services/CatalogHistoryService::TABLES` — khai `bill_incomes` + nhãn cột tiếng Việt,
      kèm 2 khoá ẢO dạng BẢNG: `details_rows` (dòng chi tiết) và `export_request_rows`
      (phân bổ phiếu YCXH — bảng con CẤP 2, tách khoá riêng theo §3, không nhét vào dòng cha)
- [x] `Modules/Finance/Services/BillIncomeHistoryService.php` — trait `LogsCatalogHistory`,
      khuôn `BillIncomeReportHistoryService`:
      · `catalogColumns()` KHÔNG chứa `status` (§3a — trạng thái luôn đi dòng riêng)
      · `catalogDisplay()` đổi id → chữ (TK nợ, mã phiếu đề nghị, ngày, số tiền)
      · `__key` của dòng chi tiết dùng khoá TỰ NHIÊN (TK có|KH|NCC|NV|đối tượng), KHÔNG dùng id —
        `syncDetails()` xoá-tạo-lại mỗi lần lưu
      · truy cập `objectable` phải qua guard try/catch (dữ liệu cũ có class ngoài morphMap)
- [x] `BillIncomeWriteService::store()` — `logCreate()`
- [x] `BillIncomeWriteService::update()` — snapshot TRƯỚC `syncDetails()`, sau lưu ghi
      `logUpdate()` + `logStatusChanged()` (2 dòng riêng khi bấm "Lưu và gửi duyệt")
- [x] `BillIncomeWriteService::destroy()` — `logDelete()` (snapshot trước khi xóa dòng con)
- [x] `BillIncomeApprovalService::approve()` — snapshot trước khi ghi số thực thu →
      1 dòng `change_status` (Chờ duyệt → Đã duyệt) + 1 dòng `update` (Thực thu từng dòng,
      Ngày hạch toán)
- [x] `BillIncomeApprovalService::cancel()` — 1 dòng `change_status` (Chờ duyệt → Hủy) kèm
      `note` = LÝ DO HỦY (§4.1). Không ghi thêm dòng `update` cho cột Diễn giải vì chính lý do
      hủy đang được ghi đè vào cột đó → 2 dòng sẽ trùng nội dung.
- [x] Bọc mọi lời gọi ghi log trong try/catch + `Log::error`: lỗi lịch sử KHÔNG được làm rớt
      giao dịch nghiệp vụ (khuôn `BillIncomeRequest::logStatusHistory()`)

### FE — ĐỦ 2 NƠI (§5.1)

- [x] `pages/finance/bill-incomes/index.vue` — thêm mục `Lịch sử` (icon `ri-history-line`,
      KHÔNG gắn cờ quyền) vào `getRowActions()` + nhánh `handleRowAction` + đặt
      `<CatalogHistoryModal ref="historyModal" modal-id="history-bill-income" record-prefix="Phiếu" />`
- [x] `pages/finance/bill-incomes/_id/index.vue` — khối `<SystemInfoSection entity-type="bill_incomes"
      endpoint-base="catalog-histories">` trong THÂN TRANG (không phải nút ở `V2Footer`)

### Verify

- [x] `php -l` + tinker: tạo/sửa/duyệt/hủy/xóa phiếu thật → đọc `getLogs()` kiểm đúng số dòng,
      đúng nhóm, đúng subset; sửa 1 ô của 1 dòng chi tiết → chỉ 1 dòng "sửa thông tin"
- [x] `getFilterOptions('bill_incomes', $id)` trả đúng 3 nhóm + danh sách người thực hiện không rỗng
- [x] Compile FE (vue-template-compiler + babel)
- [x] Dọn sạch log test, khôi phục dữ liệu đã đụng

### Ghi chú kỹ thuật phát sinh khi verify

**Lỗi đã bắt được và sửa** — log "Xóa" in ra rác. `CatalogHistoryService::changesOf()` đọc log
`delete` bằng cách diff `old_value` với mảng rỗng; khoá dạng BẢNG **không có dòng nào** được lưu là
`[]`, mà `isRowList()` CỐ Ý trả false cho mảng rỗng ⇒ nó rơi xuống nhánh trường thường và DTO trả
`old` là một **MẢNG** thay vì chuỗi (giao diện in thẳng giá trị đó → rác). Phiếu thu hầu như không
có phân bổ phiếu YCXH nên gần như MỌI log "Xóa" đều dính. Đã chặn tại
`BillIncomeHistoryService::forFullLog()` (lọc khoá bảng rỗng TRƯỚC khi ghi log toàn bộ) — KHÔNG
lọc trong `snapshot()` vì `logUpdate()` cần `[]` có mặt cả 2 phía mới phát hiện được "xoá sạch dòng
chi tiết".

⚠️ **Đây là bẫy CHUNG, không riêng màn này**: mọi màn dùng `catalog_histories` có khoá dạng BẢNG mà
bảng con rỗng lúc xóa đều dính (`bill_income_reports`, `bill_payment_requests`,
`addition_accounting_requests`…). Sửa gốc thì phải đụng `changesOf()` — hàm DÙNG CHUNG, chưa sửa,
cần hỏi ý kiến trước (CLAUDE.md).

**Đã CỐ Ý giữ nguyên, không phải thiếu sót:**
- `action = 'delete'` rơi vào nhóm lọc "Thay đổi trạng thái" (`groupOfAction()` mặc định) — hành vi
  dùng chung của mọi màn, skill §0a chấp nhận.
- Log `create` không liệt kê từng trường (chỉ 1 dòng "Tạo mới") — `changesOf()` trả `[]` cho action
  `create` ở MỌI màn.
- Nhãn nhóm ra "Bảng chi tiết thêm mới / đã xóa / sửa thông tin": `rowItemLabel()` chỉ cắt tiền tố
  "Danh sách ". Đổi cho xuôi tai phải sửa hàm dùng chung → lệch 4 màn phiếu chị em, không làm.

### Kiểm chứng đã chạy (tinker, toàn bộ trong transaction rồi ROLLBACK — không đụng dữ liệu thật)

Kịch bản 1 (phiếu dựng từ đề nghị thu thật TPE.DNTT0826.00003):
tạo → 1 dòng `create` · sửa ghi chú + người nộp + số duyệt thu dòng 1 + thêm dòng 2 → **1 dòng**
`update` liệt kê đúng 3 trường + 1 dòng thêm + 1 dòng sửa ĐÚNG CỘT · lưu lại y nguyên → **không sinh
log rác** · gửi duyệt → **dòng `change_status` RIÊNG** (Đang tạo → Chờ duyệt) · duyệt → **2 dòng**
(`update`: Ngày hạch toán + Thực thu từng dòng · `change_status`: Chờ duyệt → Đã duyệt kèm ghi chú) ·
hủy → `change_status` kèm LÝ DO HỦY · xóa → snapshot đầy đủ + 2 dòng chi tiết đã xóa.
Thứ tự trả về **mới → cũ** ở mọi bước.

Kịch bản 2 (bảng con CẤP 2): sửa 1 ô "Giá trị phân bổ" + thêm 1 phiếu YCXH → đúng 1 dòng `+` và
1 dòng `~` chỉ nêu cột đã đổi · xóa sạch dòng chi tiết → in đủ dòng đã xóa của CẢ 2 cấp · xóa phiếu
khi không còn dòng con → không còn giá trị mảng lọt vào DTO.

Bộ lọc: `getFilterOptions('bill_incomes', $id)` trả **đúng 3 nhóm cố định** (Tạo mới / Thay đổi
thông tin / Thay đổi trạng thái) và **783 người thực hiện** (không rỗng, không suy từ log).

Sau test: `catalog_histories` cho `bill_incomes` = 0 dòng, `bill_incomes` id ≥ 2358 = 0 bản ghi,
phiếu đề nghị 2536 vẫn status 2 — sạch.

`php -l` sạch 4 file BE · compile FE (vue-template-compiler + babel) sạch 3 file.

### Kiểm chứng TRÊN TRÌNH DUYỆT bằng Playwright (2026-09-03, user yêu cầu)

Cách làm: gieo 5 dòng log mẫu vào **bảng audit** `catalog_histories` cho phiếu THẬT
`TPE.PT0826.00006` (id 2357) rồi xem giao diện — **không tạo/sửa phiếu qua UI**, nên không đụng dữ
liệu nghiệp vụ. Test xong xoá đúng 5 dòng đã chèn (id 243-247); đối chiếu lại: `catalog_histories`
cho `bill_incomes` = 0, phiếu 2357 giữ nguyên `updated_at = 2026-08-27 11:03:19`, `payer`, `note`,
`status`, 3 dòng chi tiết.

Kết quả:
- **Màn danh sách**: nút "Lịch sử" (icon `ri-history-line`) hiện ở cột Hành động. Phiếu đã duyệt chỉ
  còn 3 hành động (In / Xuất Excel / Lịch sử) nên `V2BaseRowActions` hiện thẳng cả 3, không gom vào ⋮.
- **Popup**: tiêu đề "Lịch sử thay đổi" + dòng phụ "Phiếu: TPE.PT0826.00006"; timeline **mới → cũ**
  (Tạo mới nằm cuối); giá trị cũ ĐỎ / mới XANH; nhóm "Bảng chi tiết thêm mới" và "Bảng chi tiết sửa
  thông tin" có nhãn xám; ghi chú "Đã ghi bút toán vào sổ cái." nền vàng.
- **Bộ lọc**: "Loại hành động" đúng **3 nhóm cố định**; "Người thực hiện" liệt kê **đủ nhân sự**
  (không suy từ log); lọc `Thay đổi trạng thái` → còn đúng 2 dòng; lọc theo người không có log →
  hiện "Không có lịch sử phù hợp bộ lọc."; "Làm mới" reset cả `filters` lẫn `appliedFilters`.
- **Màn chi tiết**: khối "Lịch sử" kèm badge đếm `5` nằm TRONG thân trang (dưới khối Ghi chú), có nút
  "Làm mới"/"Thu gọn"; `V2Footer` vẫn chỉ In / Xuất Excel / Quay lại — đúng §5.1. Nội dung timeline
  **giống hệt popup**.
- Console: **0 lỗi** ở cả 2 màn.

📌 Thanh lọc **không có nút "Tìm kiếm"** — đúng như màn Khách hàng (`CustomerHistoryModal.vue`) và
`SystemInfoSection.vue` đã chốt: chọn giá trị là lọc LUÔN qua deep watcher. `ui-base.md` §2/§7 còn mô
tả nút "Tìm kiếm" là **tài liệu cũ chưa cập nhật**, không phải thiếu sót của màn này.

### Checkpoint — 2026-09-03
Vừa hoàn thành: lịch sử thay đổi màn Phiếu thu tiền — BE (whitelist + service ghi log + 5 điểm nối)
và FE (popup ở màn danh sách + khối Lịch sử ở màn chi tiết).
Đang làm dở: không.
Bước tiếp theo: không còn — đã kiểm chứng trên trình duyệt bằng Playwright (2 nơi hiện giống hệt
nhau, bộ lọc chạy, 0 lỗi console). User nghiệm thu.
Blocked: không.

---

## Phase M — Bộ tài liệu bàn giao: Testcase + HDSD + SRS (2026-09-03, @khoipv)

**User yêu cầu:** "gen cả tài liệu phiếu thu" — sau khi xong bộ tài liệu màn Phiếu yêu cầu chuyển hàng.

### M.1 Chuẩn bị
- [x] Đọc lại code nguồn: `BillIncome` (4 trạng thái, generateCode, context) · `BillIncomeAccess`
      (canView/canEdit/canDelete/canApprove thuần) · 4 FormRequest (Store/Update/Approve/Cancel,
      nguyên văn message) · Controller (13 route) · `BillIncomeService` (applyScope 3 nhánh +
      13 ô lọc + whitelist sort) · `BillIncomeWriteService` (guardOneBillPerRequest khoá dòng,
      syncDetails, notifyTreasurers) · `BillIncomeApprovalService` (khoá dòng chặn duyệt lại,
      8 bước duyệt, hủy) · `BillIncomeAccountingService` · 2 Resource · seeder quyền 1500-1502 ·
      FE `index.vue` / `BillIncomeForm.vue` / `_id/index.vue` / `_id/print.vue` /
      `IncomeRequestSearchModal.vue` · menu `finance.js:85`
- [x] Chụp **26 ảnh thật** 1440x900 -> `pt_shots/` (chỉ để local)
      2 vướng mắc + cách xử lý (user chốt):
      1. Không có phiếu **Đang tạo** nào trên cổng dev -> đã tạo phiếu nháp `TPE.PT0926.00001`
         (từ đề nghị TEST.DNTT.00051), chụp Sửa / Xác nhận xóa / hành động dòng, rồi **xóa ngay**
         -> danh sách trở lại đúng **2.379** phiếu. Nháp KHÔNG ghi sổ cái, KHÔNG đổi trạng thái
         phiếu đề nghị, KHÔNG bắn thông báo. Chỉ tiêu 1 số mã phiếu.
      2. Cổng dev **chưa deploy Phase L** (Lịch sử thay đổi, làm cùng ngày) -> 3 ảnh mục Lịch sử
         chụp trên **cổng local** (`localhost:3000`, DB dump riêng) theo chỉ định của user;
         phiếu nháp dựng để lấy dòng lịch sử thật cũng đã xóa sau khi chụp.
- [x] TUYỆT ĐỐI không bấm **Duyệt phiếu thu** và **Hủy phiếu thu** trên dữ liệu thật của cổng dev
      (duyệt = ghi bút toán sổ cái dùng chung, không hoàn tác được) — chỉ chụp nút + ô nhập +
      hộp xác nhận rồi thoát

### M.2 Testcase
- [x] `gen_testcase.py` dùng `tc_engine.py` -> `testcase.xlsx`: **169 TC** (P0 61%), 9 mục mô tả
      đầy đủ, 13 TC-ROLE + 14 section La Mã (I->XIV), bộ kiểm tra thuật ngữ in **OK - sạch**.
      Mọi TC đụng tới Duyệt/Hủy đều mở đầu bằng cảnh báo CHỈ LÀM TRÊN PHIẾU DO CHÍNH MÌNH TẠO

### M.3 HDSD
- [x] `gen_hdsd.py` dùng `hdsd_engine.py` -> `HDSD_Phiếu thu tiền.docx`: **44 trang**,
      15 Heading 1 (Tổng quan + 12 phần), 18 bảng, **26 ảnh thật** + logo bìa;
      mục lục + danh mục hình cập nhật bằng Word
- [x] Verify style HDSD: direct formatting = **2 / 10 / 0** — khớp đúng `HDSD_MAU.docx`

### M.4 SRS
- [x] `gen_srs.py` dùng `srs_docx_lib.py` -> `SRS - Phiếu thu tiền.docx`: **52 trang**, 4 chương,
      **13 chức năng** FR-01->FR-13, 44 bảng, 29 ảnh (1 sơ đồ tổng quan phân cấp + 10 biểu đồ use
      case + 18 ảnh chụp thật), Phần 4 có **16 quy tắc** BR-01->BR-16
- [x] Verify SRS đủ 4 điểm form 2026-08-28: 13 mục Layout ghi `Menu:` (0 dòng URL) · 13 đoạn
      `Quy tắc chung:` · Phần 4 là bảng 5 cột · sơ đồ tổng quan dùng `overview_figure2` phân cấp.
      Đánh số mục con 2.x.y liên tục ở cả 13 chức năng (0 chỗ lệch)
- [x] `git status`: chỉ thấy `.docx`/`.xlsx`/`gen_*.py`, **không có `.png`**

### Checkpoint — 2026-09-03 (Phase M)
Vừa hoàn thành: bộ 3 tài liệu bàn giao màn Phiếu thu tiền (testcase 169 TC · HDSD 44 trang ·
SRS 52 trang), ảnh chụp thật 100%.
Đang làm dở: không có.
Bước tiếp theo: user đọc soát nội dung nghiệp vụ; sửa gì thì chỉnh trong `gen_*.py` rồi chạy lại.
Blocked: không.

⚠️ **Ghi nhận thao tác trên dữ liệu**:
- Cổng dev: tạo phiếu nháp `TPE.PT0926.00001` từ đề nghị TEST.DNTT.00051 để chụp Sửa/Xóa,
  **đã xóa ngay** — danh sách trở lại 2.379 phiếu. Tiêu 1 số mã phiếu (phiếu kế tiếp từ 00002).
- Cổng local: tạo + sửa + xóa 1 phiếu nháp để lấy dòng lịch sử thật cho 2 ảnh mục Lịch sử.
- **KHÔNG bấm Duyệt và KHÔNG bấm Hủy** trên bất kỳ phiếu thật nào ở cả 2 cổng — 2 thao tác đó
  ghi/khoá sổ cái, không hoàn tác được. Ảnh minh hoạ chỉ chụp nút, ô nhập và hộp xác nhận.

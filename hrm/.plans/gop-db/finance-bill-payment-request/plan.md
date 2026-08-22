# Plan — Phiếu đề nghị thanh toán (ERP → HRM, phân hệ Tài chính)

> **For agentic workers:** dùng `superpowers:subagent-driven-development` hoặc `superpowers:executing-plans`, thực hiện task theo checkbox.
> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Spec: `docs/superpowers/specs/gop-db/2026-08-14-finance-bill-payment-request-design.md`
> Tóm tắt design: `.plans/gop-db/finance-bill-payment-request/design.md`

**Goal:** Port màn ERP "Phiếu đề nghị thanh toán" (`bill_payment_requests`, 4.040 phiếu) sang HRM phân hệ Tài chính — dùng chung bảng ERP, đủ **luồng duyệt 5 cấp**, đổi nguồn hợp đồng bán `firm_contracts` → `hrm_contracts`, dừng trước màn Phiếu chi.

**Architecture:** BE `Modules/Finance` (Entity + Service + FormRequest + Resource + ApiController) bám **nguyên khuôn màn Đề nghị thu tiền đã hoàn thành** — đọc `Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php` và `Modules/Finance/Services/BillIncomeRequestService.php` trước khi viết dòng đầu tiên. FE Nuxt 2 V2Base `pages/finance/bill-payment-requests` (list 4 chế độ + form + detail + print). Không migration; thay đổi DB duy nhất là 9 dòng `Permission::create`.

**Tech Stack:** PHP 7.4 / Laravel 8 / `nwidart/laravel-modules` / `spatie/laravel-permission` · Nuxt 2 (Vue 2) + Bootstrap-Vue + V2Base · MySQL DB gộp `gop_db`.

---

## Ràng buộc toàn cục (mọi task ngầm bao gồm)

- Nhánh `gop_db` ở **cả 2 repo**. **KHÔNG commit/push khi user chưa yêu cầu** — vì vậy plan này **không có bước commit**; mỗi task kết thúc bằng bước **Verify**.
- **KHÔNG** dùng `mysql2` / `DB_CONNECTION_SECOND` / `DB_DATABASE_SECOND`; **KHÔNG** khai `$connection` trong model.
- **KHÔNG** sửa bất kỳ file nào trong repo ERP (`D:\laragon\www\erp`) — chỉ đọc.
- **KHÔNG** migration. Thay đổi DB duy nhất: 9 dòng `Permission::create` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (id **1153–1161**).
- **KHÔNG** ghi bảng `bill_payment_request_detail_product_export_requests` (0 dòng, nhánh đã bỏ) — kể cả xoá.
- **KHÔNG** sửa dữ liệu nghiệp vụ đang có của ERP.
- File đính kèm dùng **cột `attachments`** của bảng ERP (chuỗi URL nối bằng `', '`), **KHÔNG** dùng bảng `files` — ngoại lệ có chủ đích, lý do ở spec mục 6.
- **KHÔNG** gắn middleware `checkPermission` cho route nào của màn này. Gate bằng method trên Entity (trait `ChecksEmployeePermission`).
- `auth()->user()->id` là id nhân viên duy nhất (DB đã gộp `employees`).
- BE: rethrow `ValidationException`, không catch chung `Exception`. Sau mỗi file PHP chạy `php -l <file>`.
- FE: đọc trước khi code — `.claude/skills/button-convention/SKILL.md`, `modal-popup/SKILL.md`, `form-validate/SKILL.md`, `unsaved-changes/SKILL.md`, `list-page/SKILL.md`, `print-page/SKILL.md`. Select trong modal **bắt buộc** `V2BaseSelectInModal`.
- FE: cờ quyền **fail-closed** — mọi `can*` khởi tạo `false`, chỉ set từ field BE trả về. Cấm gán literal `true`. Khi review tự grep `can[A-Za-z]*\s*=\s*true`.
- FE: base đã có `v-validate` gắn thẳng vào `V2Base*` (2 mixin `utils/mixins/v2ValidateMixin.js` + `formValidateMixin.js`) — **đọc code hiện tại của `CustomerForm.vue`**, không bám snapshot cũ.
- FE: **không** chép khuôn từ `ProductTransferRequestForm.vue` (class `form-card`/`form-header`/`readonly-cell` nằm trong `<style>` riêng của màn đó, không có ở `v2-styles.scss`). Khuôn chuẩn là `CustomerForm.vue`.
- **Không tự test bằng Playwright** — verify bằng `php -l` / `php artisan tinker` / `curl` HTTP thật / parse template FE. User tự mở trình duyệt. Báo rõ phần chưa kiểm chứng.
- Tài khoản dev đang đăng nhập có **0 quyền** → verify HTTP phải dùng token JWT của tài khoản có quyền thật.
- Base URL API dev: `http://localhost:8000/api/v1/finance/...`
- Nguồn port ERP (chỉ đọc): `app/Http/Controllers/IncomeExpenditure/BillPaymentRequestController.php` · `app/Model/IncomeExpenditure/BillPaymentRequest.php` (+ `...Detail.php`) · `app/Http/Requests/IncomeExpenditure/BillPaymentRequest/*` · `resources/views/income_expenditure/bill_payment_requests/*` · `resources/views/partials/classes/IncomeExpenditure/BillPaymentRequest*.blade.php` · `app/Services/Contracts/SearchContractService.php@searchAllContract|@searchContractForPaymentSupplier` · `app/Model/Accounting/AccountDetail.php:1798`.

### Hằng số nghiệp vụ dùng xuyên suốt

```
STATUS: 1 Đang tạo · 2 Chờ TP duyệt · 3 Chờ KT công nợ · 4 Chờ KT trưởng · 5 Chờ BGĐ
        6 Chờ tạo phiếu chi · 7 Chờ duyệt phiếu chi* · 8 Duyệt phiếu chi* · 9 Đã hủy* · 10 Không duyệt
        (* = ngoài phạm vi, HRM chỉ hiển thị)

TYPE:   1 Chi trả nhà cung cấp · 2 Chi trả lại khách hàng
        6 Chi thưởng thực hiện hợp đồng · 12 Thanh toán chi phí vận chuyển NCC

TYPE_PAYMENT: 1 TM · 2 CK
COST: 1 Phí do người chuyển tiền chịu · 2 Phí do người hưởng chịu · 3 Phí chia sẻ cho 2 bên

Cột tiền theo cấp:
  người lập → payment_money_request        (+ _exchange)
  TP        → payment_money_manage         (+ _exchange)
  KT công nợ→ payment_money_accountant_debt(+ _exchange)
  KT trưởng/BGĐ → payment_money_chief_accountant (+ _exchange)
```

---

## Cấu trúc file

### BE — `hrm-api` (nhánh `gop_db`)

| File | Trách nhiệm |
| --- | --- |
| `Modules/Finance/Entities/Contract/WarehouseImport.php` | read-only, chỉ để morph phiếu cũ |
| `Modules/Finance/Entities/Contract/WarehouseExport.php` | read-only, chỉ để morph phiếu cũ |
| `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php` | hằng số, quan hệ, `searchByFilter`, `generateCode`, toàn bộ `can*` |
| `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequestDetail.php` | quan hệ + morphTo `contractable` |
| `Modules/Finance/Entities/Delivery/DeliveryTrip.php` · `OtherDeliveryTrip.php` · `DeliveryTripAccounting.php` · `OtherDeliveryTripAccounting.php` | read-only, loại chi 12 |
| `Modules/Finance/Entities/Delivery/PriceListValidDelivery.php` (+ `...Vehicle.php`, `...VehiclePayload.php`, `...VehiclePayloadRoad.php`) | bảng giá cước, popup chuyến xe |
| `Modules/Finance/Services/BillPaymentDebtService.php` | công nợ theo TK 3311 / 1311 / 3351 |
| `Modules/Finance/Services/BillPaymentRequestService.php` | list 4 chế độ · show · store · update · destroy · syncDetails |
| `Modules/Finance/Services/BillPaymentApprovalService.php` | chuyển cấp duyệt + Không duyệt + clamp tiền |
| `Modules/Finance/Services/BillPaymentRequestNotifyService.php` | 6 sự kiện thông báo |
| `Modules/Finance/Services/DeliveryTripPaymentService.php` | loại chi 12: lấy dữ liệu + chi tiết chuyến xe |
| `Modules/Finance/Services/BillPaymentAttachmentService.php` | upload/gỡ file trên cột `attachments` |
| `Modules/Finance/Http/Requests/BillPaymentRequest/*.php` (4 file) | validate Store / Update / Approve / ChangeStatus |
| `Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php` | mỏng, chỉ gate quyền + gọi service |
| `Modules/Finance/Transformers/BillPaymentRequestResource/*.php` (3 file) | List · Detail · Print |
| `Modules/Finance/Database/Seeders/BillPaymentRequestTestDataSeeder.php` | dữ liệu test 5 trạng thái, DRY-RUN mặc định |
| *(sửa)* `Modules/Finance/Routes/api.php` · `Modules/Finance/Providers/FinanceServiceProvider.php` · `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | |

### FE — `hrm-client` (nhánh `gop_db`)

| File | Trách nhiệm |
| --- | --- |
| `pages/finance/bill-payment-requests/index.vue` | danh sách, 4 chế độ qua prop `mode` |
| `pages/finance/bill-payment-requests/create.vue` · `_id/edit.vue` · `_id/index.vue` | trang vỏ mỏng bọc form |
| `pages/finance/bill-payment-requests/_id/print.vue` | màn in 3 mẫu |
| `.../components/BillPaymentRequestForm.vue` | form dùng chung create/edit/xem |
| `.../components/BillPaymentRequestDetailTable.vue` | bảng chi tiết, cột đổi theo loại chi |
| `.../components/BankInfoSection.vue` | 2 nhánh ngân hàng |
| `.../components/AttachmentSection.vue` | file đính kèm |
| `.../components/ApproveActions.vue` | nút duyệt theo cấp + `RejectModal` |
| `.../components/DeliveryTripDetailModal.vue` | popup 13 cột |
| *(sửa)* `components/subsystem-menu/finance.js` | 2 mục menu |

---

# Phase 0 — Brainstorming & chốt design

- [x] Đọc hiểu toàn bộ luồng ERP (controller 733 dòng · model 1.190 dòng · 8 blade · 3 class JS · 2 service tìm hợp đồng)
- [x] Khảo sát dữ liệu thật trên `gop_db` (phân bố loại chi / trạng thái / morph type / attachments)
- [x] Chốt 10 quyết định với user (spec mục 2)
- [x] Viết spec `docs/superpowers/specs/gop-db/2026-08-14-finance-bill-payment-request-design.md`
- [x] User review spec — duyệt 2026-08-14
- [x] Lên plan chi tiết (file này)

---

# Phase 1 — BE nền: entity + quyền + danh sách + chi tiết

### Task 1.1 — 2 entity morph còn thiếu + đăng ký morphMap

**Files:**
- Create: `Modules/Finance/Entities/Contract/WarehouseImport.php`
- Create: `Modules/Finance/Entities/Contract/WarehouseExport.php`
- Modify: `Modules/Finance/Providers/FinanceServiceProvider.php` (method `registerMorphMap()`)

**Interfaces:**
- Produces: 2 class read-only có `$table = 'warehouse_imports' | 'warehouse_exports'`; 2 entry morphMap `'App\Model\Warehouse\WarehouseImport'` và `'App\Model\Warehouse\WarehouseExport'`.
- Consumes: khuôn `Modules/Finance/Entities/Contract/FirmContract.php` đã có.

- [x] **Bước 1: Đọc khuôn có sẵn**

Đọc `Modules/Finance/Entities/Contract/FirmContract.php` để copy đúng kiểu docblock + khai báo read-only đang dùng trong module.

- [x] **Bước 2: Tạo 2 entity**

```php
<?php

namespace Modules\Finance\Entities\Contract;

use Illuminate\Database\Eloquent\Model;

/**
 * Phiếu nhập kho của ERP — chỉ ĐỌC.
 *
 * `bill_payment_request_details` có 25 dòng `objectable/contractable_type` trỏ
 * `App\Model\Warehouse\WarehouseImport`. Thiếu class + morphMap thì mở phiếu cũ chứa dòng này
 * sẽ nổ "Class not found". Không cho chọn mới ở form — chỉ để đọc lại phiếu ERP.
 */
class WarehouseImport extends Model
{
    protected $table = 'warehouse_imports';

    public $timestamps = false;

    protected $guarded = ['*'];
}
```

`WarehouseExport.php` giống hệt, đổi `$table = 'warehouse_exports'` và docblock ghi **15 dòng**.

- [x] **Bước 3: Thêm 2 dòng vào morphMap**

Trong `registerMorphMap()`, thêm vào mảng `Relation::morphMap([...])`:

```php
'App\Model\Warehouse\WarehouseImport'         => FinanceContract\WarehouseImport::class,
'App\Model\Warehouse\WarehouseExport'         => FinanceContract\WarehouseExport::class,
```

- [x] **Bước 4: Verify**

```bash
php -l Modules/Finance/Entities/Contract/WarehouseImport.php
php -l Modules/Finance/Entities/Contract/WarehouseExport.php
php artisan tinker --execute="echo Modules\Finance\Entities\Contract\WarehouseImport::count().' | '.Modules\Finance\Entities\Contract\WarehouseExport::count();"
```
Kỳ vọng: in ra 2 số > 0, không exception.

---

### Task 1.2 — Entity `BillPaymentRequest` + `BillPaymentRequestDetail`

**Files:**
- Create: `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php`
- Create: `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequestDetail.php`

**Interfaces:**
- Consumes: trait `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (`currentEmployeeHasPermission`, `currentEmployeeIsSuperAdmin`, `currentCompanyId`, `employeeInfoIdsHavingPermission`).
- Produces:
  - Hằng: `STATUS_*` (10), `TYPE` / `TYPES_ALLOWED = [1,2,6,12]`, `TYPE_PAYMENT`, `COST`, `STATUSES`, `PERMISSION_*` (6).
  - `static searchByFilter(Request $r, string $scope = 'all'): Builder` — `$scope ∈ mine|all|pending|approved`
  - `static generateCode(): string`
  - `static contractMorphTypes(): array` · `static allowedContractTypes(int $type): array`
  - `static typeForSelect(): array` (chỉ 4 loại `TYPES_ALLOWED`) · `static typePaymentForSelect(): array` · `static costForSelect(): array`
  - `canView(): bool` · `canEdit(): bool` · `canDelete(): bool`
  - `canApproveAtCurrentStatus(): bool` · `canCancel(): bool` · `nextStatuses(): array`
  - Cờ FE: `static canViewAllCompany|canViewCompany|canViewDepartment|canViewPart(): bool`, `static isAccountant(): bool`
  - Cờ quyền duyệt cho FE (không phụ thuộc phiếu): `static hasPermissionManage|hasPermissionAccountingDept|hasPermissionChiefAccountant|hasPermissionBoardOfManager(): bool` — mỗi cái là `self::currentEmployeeIsSuperAdmin() || self::currentEmployeeHasPermission(self::PERMISSION_X)`
  - Quan hệ: `details()`, `currency()`, `employee_create()`, `manage_approver()`, `accounting_approver()`, `chief_accounting_approver()`, `board_of_manager_approver()`

- [x] **Bước 1: Đọc khuôn**

Đọc **toàn bộ** `Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequest.php` (542 dòng). Entity mới bám đúng khuôn đó: `extends Model` (không `BaseModel`), `use ChecksEmployeePermission`, hook `creating`/`saving`, docblock giải thích chỗ khác ERP.

- [x] **Bước 2: Viết phần khai báo + hằng số**

```php
<?php

namespace Modules\Finance\Entities\BillPaymentRequest;

use Illuminate\Database\Eloquent\Model;
use Modules\Finance\Entities\Concerns\ChecksEmployeePermission;
use Modules\Finance\Entities\Currency\Currency;
use Modules\Finance\Entities\ProductTransferRequest\EmployeeManagePart;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Entities\EmployeeManageDepartment;

/**
 * Phiếu đề nghị thanh toán — bảng ERP `bill_payment_requests` trên DB gộp
 * (port từ `App\Model\IncomeExpenditure\BillPaymentRequest`).
 *
 * DÙNG CHUNG bảng với cổng ERP: KHÔNG đổi schema, KHÔNG migration.
 * Khác màn Đề nghị thu tiền: chứng từ này đi qua LUỒNG DUYỆT 5 CẤP, mỗi cấp ghi tiền vào
 * một cột riêng ở bảng chi tiết (xem `BillPaymentApprovalService`).
 */
class BillPaymentRequest extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'bill_payment_requests';

    protected $fillable = [
        'code', 'type', 'type_payment', 'reason', 'type_money_id', 'exchange_rate', 'status',
        'created_by', 'updated_by', 'company_id', 'department_id', 'part_id',
        'customer_id', 'customer_code', 'customer_name',
        'supplier_id', 'supplier_code', 'supplier_name',
        'employee_id', 'employee_code', 'employee_name',
        'account_name', 'account_number', 'bank_name', 'bank_branch',
        'bank_province_name', 'bank_province_id', 'bank_id', 'bank_address',
        'swift_code', 'iban_number',
        'mid_bank_id', 'mid_account_number', 'mid_account_name', 'mid_bank_name',
        'mid_swift_code', 'mid_iban_number', 'mid_bank_address',
        'cost', 'has_contract', 'to_date', 'attachments',
        'manage_approved_id', 'manage_approved_time', 'accounting_approved_id',
        'chief_accounting_approved_id', 'board_of_manager_approved_id',
        'note', 'note_accountant_dept', 'note_chief_accountant', 'note_board_of_manager',
        'reject_comment',
    ];

    const STATUS_CREATING = 1;
    const STATUS_AWAITING_MANAGE = 2;
    const STATUS_AWAITING_ACCOUNTING_DEPT = 3;
    const STATUS_AWAITING_CHIEF_ACCOUNTANT = 4;
    const STATUS_AWAITING_BOARD_OF_MANAGER = 5;
    const STATUS_AWAITING_CREATE_BILL_PAYMENT = 6;
    const STATUS_AWAITING_APPROVE_BILL_PAYMENT = 7;  // ngoài phạm vi, chỉ hiển thị
    const STATUS_APPROVED_BILL_PAYMENT = 8;          // ngoài phạm vi, chỉ hiển thị
    const STATUS_CANCEL = 9;                         // ngoài phạm vi, chỉ hiển thị
    const STATUS_REJECT = 10;

    const TYPE_SUPPLIER = 1;
    const TYPE_CUSTOMER_REFUND = 2;
    const TYPE_CONTRACT_BONUS = 6;
    const TYPE_DELIVERY = 12;

    /** Giữ nguyên key của ERP để phiếu cũ hiển thị đúng tên, dù dropdown chỉ cho chọn 4 loại. */
    const TYPE = [
        1 => 'Chi trả nhà cung cấp',
        2 => 'Chi trả lại khách hàng',
        3 => 'Chi thưởng NVKD',
        4 => 'Chi thu nhập cho nhân viên',
        6 => 'Chi thưởng thực hiện hợp đồng',
        10 => 'Chi khác',
        12 => 'Thanh toán chi phí vận chuyển NCC',
    ];

    /** 4 loại được phép tạo/sửa ở HRM (user chốt) — 3/4/10 có 0 phiếu trên DB. */
    const TYPES_ALLOWED = [1, 2, 6, 12];

    const TYPE_PAYMENT = [1 => 'TM', 2 => 'CK'];

    const COST = [
        1 => 'Phí do người chuyển tiền chịu',
        2 => 'Phí do người hưởng chịu',
        3 => 'Phí chia sẻ cho 2 bên',
    ];

    public const STATUSES = [
        ['id' => self::STATUS_CREATING, 'name' => 'Đang tạo', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_MANAGE, 'name' => 'Chờ TP duyệt', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_ACCOUNTING_DEPT, 'name' => 'Chờ kế toán công nợ duyệt', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_CHIEF_ACCOUNTANT, 'name' => 'Chờ kế toán trưởng duyệt', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_BOARD_OF_MANAGER, 'name' => 'Chờ ban giám đốc duyệt', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_CREATE_BILL_PAYMENT, 'name' => 'Chờ tạo phiếu chi', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_APPROVE_BILL_PAYMENT, 'name' => 'Chờ duyệt phiếu chi', 'type' => 'danger'],
        ['id' => self::STATUS_APPROVED_BILL_PAYMENT, 'name' => 'Duyệt phiếu chi', 'type' => 'success'],
        ['id' => self::STATUS_CANCEL, 'name' => 'Đã hủy', 'type' => 'danger'],
        ['id' => self::STATUS_REJECT, 'name' => 'Không duyệt', 'type' => 'danger'],
    ];

    /** Tên quyền giữ NGUYÊN VĂN ERP — kể cả 2 chỗ ERP viết sai "đề nghi" (user chốt, spec 7.1). */
    const PERMISSION_SALE = 'Kinh doanh đề nghị thanh toán';
    const PERMISSION_MANAGE = 'Trưởng phòng duyệt đề nghị thanh toán';
    const PERMISSION_ACCOUNTING_DEPT = 'Kế toán công nợ duyệt đề nghị thanh toán';
    const PERMISSION_CHIEF_ACCOUNTANT = 'Kế toán trưởng duyệt đề nghi thanh toán';
    const PERMISSION_BOARD_OF_MANAGER = 'Ban giám đốc duyệt đề nghi thanh toán';
    const PERMISSION_ACCOUNTANT = 'Kế toán thanh toán';
    const PERMISSION_VIEW_ALL_COMPANY = 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty';
    const PERMISSION_VIEW_COMPANY = 'Xem tất cả phiếu đề nghị thanh toán của công ty';
    const PERMISSION_VIEW_DEPARTMENT = 'Xem tất cả phiếu đề nghị thanh toán của phòng ban';
    const PERMISSION_VIEW_PART = 'Xem tất cả phiếu đề nghị thanh toán của bộ phận';
```

- [x] **Bước 3: Hook `boot()` + quan hệ**

Copy nguyên cách làm của `BillIncomeRequest::boot()` (gán `created_by` / `company_id` / `department_id` / `part_id` ở hook **`creating`**, `updated_by` ở **`saving`**) — có docblock giải thích tại sao không làm ở `created` như ERP.

```php
    public function details()
    {
        return $this->hasMany(BillPaymentRequestDetail::class, 'bill_payment_request_id', 'id');
    }

    public function currency()
    {
        return $this->belongsTo(Currency::class, 'type_money_id');
    }

    public function employee_create()
    {
        return $this->belongsTo(Employee::class, 'created_by', 'id');
    }

    public function manage_approver()
    {
        return $this->belongsTo(Employee::class, 'manage_approved_id', 'id');
    }

    public function accounting_approver()
    {
        return $this->belongsTo(Employee::class, 'accounting_approved_id', 'id');
    }

    public function chief_accounting_approver()
    {
        return $this->belongsTo(Employee::class, 'chief_accounting_approved_id', 'id');
    }

    public function board_of_manager_approver()
    {
        return $this->belongsTo(Employee::class, 'board_of_manager_approved_id', 'id');
    }
```

- [x] **Bước 4: `searchByFilter()` — 4 chế độ**

Bám `BillIncomeRequest::searchByFilter()`.

⚠️ **SỬA SAU KHI THỰC THI (2026-08-14) — bản đầu của plan này SAI, gây lỗi Critical.**
Khối 5 nhánh phạm vi quyền xem **và** khối ẩn phiếu nháp của người khác **CHỈ được áp khi
`$scope === 'all'`**. Đối chiếu ERP `searchByFilter()`: cả 2 khối đó nằm **bên trong**
`if ($request->_type == 'all')`; 3 chế độ `index` / `for-approved` / `approved` hoàn toàn không bị
lọc theo cấp. Nếu áp cho cả 4 chế độ thì người duyệt **không có** quyền `Xem tất cả phiếu … của …`
rơi vào nhánh cuối `created_by = me` ⇒ tab **Chờ duyệt** và **Đã duyệt** rỗng ⇒ **luồng duyệt 5 cấp
chết hẳn**.

```php
        if ($scope === 'all') {
            // ... 5 nhánh phạm vi quyền xem ...
            // ... khối ẩn phiếu nháp của người khác ...
        }
```

Rồi thêm 4 chế độ:

```php
        // ---- Chế độ danh sách (mirror ERP `_type`) ----
        if ($scope === 'mine') {
            $query->where('created_by', $employeeId);
        }

        if ($scope === 'pending') {
            // Mirror ERP `_type = for-approved`: chỉ phiếu trong công ty mình, và chỉ trạng thái
            // mà người đăng nhập có quyền duyệt. Không quyền nào -> không thấy phiếu nào.
            $query->where('company_id', $companyId)->where(function ($q) use ($employeeId, $companyId) {
                if (self::currentEmployeeHasPermission(self::PERMISSION_MANAGE)) {
                    $departmentIds = EmployeeManageDepartment::query()
                        ->where('employee_id', $employeeId)
                        ->where('company_id', $companyId)
                        ->pluck('department_id')
                        ->toArray();
                    $q->orWhere(function ($q1) use ($departmentIds) {
                        $q1->where('status', self::STATUS_AWAITING_MANAGE)
                            ->whereIn('department_id', $departmentIds);
                    });
                }
                if (self::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTING_DEPT)) {
                    $q->orWhere('status', self::STATUS_AWAITING_ACCOUNTING_DEPT);
                }
                if (self::currentEmployeeHasPermission(self::PERMISSION_CHIEF_ACCOUNTANT)) {
                    $q->orWhere('status', self::STATUS_AWAITING_CHIEF_ACCOUNTANT);
                }
                if (self::currentEmployeeHasPermission(self::PERMISSION_BOARD_OF_MANAGER)) {
                    $q->orWhere('status', self::STATUS_AWAITING_BOARD_OF_MANAGER);
                }
                if (self::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTANT)) {
                    $q->orWhere('status', self::STATUS_AWAITING_CREATE_BILL_PAYMENT);
                }
                // Không quyền nào -> thêm điều kiện luôn sai để tránh trả về cả bảng.
                $q->orWhereRaw('1 = 0');
            });
        }

        if ($scope === 'approved') {
            // Mirror ERP `_type = approved`: phiếu mà chính mình đã duyệt ở bất kỳ cấp nào.
            $query->where(function ($q) use ($employeeId) {
                $q->where('manage_approved_id', $employeeId)
                    ->orWhere('accounting_approved_id', $employeeId)
                    ->orWhere('chief_accounting_approved_id', $employeeId)
                    ->orWhere('board_of_manager_approved_id', $employeeId);
            });
        }
```

Bộ lọc FE: `code` (like) · `reason` (like) · `type` · `type_payment` · `status` · `created_by` · `company_id` · `department_id` · `part_id` · `customer_id` · `supplier_id` · `start_date` / `end_date` (`whereDate` `>=` / `<=`) · `payment_money_request_from` / `_to`.

⚠️ 2 điểm **phải sửa so với ERP**:
- `customer_id` / `supplier_id`: ERP `pluck()` toàn bộ id dòng chi tiết rồi `whereIn` — với 47.329 dòng là nạp cả bảng vào PHP. Dùng `whereHas('details', ...)` kết hợp `orWhere` cột trên master:
```php
        if ($request->filled('customer_id')) {
            $customerId = $request->get('customer_id');
            $query->where(function ($q) use ($customerId) {
                $q->where('customer_id', $customerId)
                    ->orWhereHas('details', function ($q1) use ($customerId) {
                        $q1->where('customer_id', $customerId);
                    });
            });
        }
```
- `payment_money_request_from/_to`: ERP nội suy thẳng chuỗi vào `havingRaw("... >= $price_from")` → **lỗ SQL injection**. Dùng binding y như `BillIncomeRequest::parentIdsByTotalIncome()`.

Sort: copy `applySort()` với whitelist `code · created_at · status · type · type_payment`.

- [x] **Bước 5: `generateCode()`**

Copy **nguyên** `BillIncomeRequest::generateCode()`, đổi bảng và prefix — trùng format `{cty}.DNTT{mmyy}.{5 số}` (ERP dùng cùng prefix DNTT cho cả 2 màn nhưng **khác bảng** nên không đụng nhau).

- [x] **Bước 6: Nhóm `can*`**

```php
    /** Sửa/Xoá: chỉ người tạo, chỉ khi phiếu đang nháp hoặc bị trả lại. */
    public function canEdit(): bool
    {
        return in_array($this->status, [self::STATUS_CREATING, self::STATUS_REJECT])
            && $this->created_by == auth()->id();
    }

    public function canDelete(): bool
    {
        return $this->canEdit();
    }

    /**
     * Người đăng nhập có quyền duyệt phiếu ở ĐÚNG trạng thái hiện tại của nó.
     * Port ERP `canCancel()` (:726) — ERP dùng chung điều kiện này cho cả nút duyệt lẫn Không duyệt.
     */
    public function canApproveAtCurrentStatus(): bool
    {
        $companyId = self::currentCompanyId();
        if ($companyId === null || $this->company_id === null || (int) $this->company_id !== $companyId) {
            return false;
        }

        switch ((int) $this->status) {
            case self::STATUS_AWAITING_MANAGE:
                if (!self::currentEmployeeHasPermission(self::PERMISSION_MANAGE)) {
                    return false;
                }
                $departmentIds = EmployeeManageDepartment::query()
                    ->where('employee_id', auth()->id())
                    ->where('company_id', $companyId)
                    ->pluck('department_id')
                    ->toArray();

                return $this->department_id !== null && in_array($this->department_id, $departmentIds);
            case self::STATUS_AWAITING_ACCOUNTING_DEPT:
                return self::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTING_DEPT);
            case self::STATUS_AWAITING_CHIEF_ACCOUNTANT:
                return self::currentEmployeeHasPermission(self::PERMISSION_CHIEF_ACCOUNTANT);
            case self::STATUS_AWAITING_BOARD_OF_MANAGER:
                return self::currentEmployeeHasPermission(self::PERMISSION_BOARD_OF_MANAGER);
            case self::STATUS_AWAITING_CREATE_BILL_PAYMENT:
                return self::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTANT);
            default:
                return false;
        }
    }

    public function canCancel(): bool
    {
        return $this->canApproveAtCurrentStatus();
    }

    /**
     * Các trạng thái hợp lệ mà người đăng nhập được đẩy phiếu sang, tính từ trạng thái hiện tại.
     * Dùng để validate `status` gửi lên — chặn nhảy cóc (vd 2 -> 6) và chặn tự đặt 7/8/9.
     */
    public function nextStatuses(): array
    {
        if (!$this->canApproveAtCurrentStatus()) {
            return [];
        }

        switch ((int) $this->status) {
            case self::STATUS_AWAITING_MANAGE:
                return [self::STATUS_AWAITING_ACCOUNTING_DEPT];
            case self::STATUS_AWAITING_ACCOUNTING_DEPT:
                return [self::STATUS_AWAITING_CHIEF_ACCOUNTANT];
            case self::STATUS_AWAITING_CHIEF_ACCOUNTANT:
                // KT trưởng: duyệt thẳng (6) hoặc chuyển BGĐ (5).
                return [self::STATUS_AWAITING_CREATE_BILL_PAYMENT, self::STATUS_AWAITING_BOARD_OF_MANAGER];
            case self::STATUS_AWAITING_BOARD_OF_MANAGER:
                return [self::STATUS_AWAITING_CREATE_BILL_PAYMENT];
            default:
                return [];
        }
    }
```

`canView()` copy khuôn `BillIncomeRequest::canView()` (fail-closed khi chưa auth), thay 2 nhánh "người duyệt" thành 4 cột `*_approved_id`, và thêm nhánh cuối `canApproveAtCurrentStatus()`.

4 cờ `canViewAllCompany/Company/Department/Part` + `isAccountant()` copy nguyên.

- [x] **Bước 7: Entity `BillPaymentRequestDetail`**

```php
<?php

namespace Modules\Finance\Entities\BillPaymentRequest;

use Illuminate\Database\Eloquent\Model;
use Modules\Finance\Entities\Supplier;
use Modules\Human\Entities\Employee;

/**
 * Dòng chi tiết phiếu đề nghị thanh toán — bảng ERP `bill_payment_request_details`.
 *
 * `contractable_type` lưu TÊN CLASS PHP CỦA ERP (ERP không đăng ký morphMap) — HRM map ngược
 * bằng `Relation::morphMap()` trong `FinanceServiceProvider` (10 class sau Task 1.1).
 * 754/47.329 dòng có `contractable_type` NULL (chủ yếu loại chi 12) → mọi chỗ đọc phải null-safe.
 */
class BillPaymentRequestDetail extends Model
{
    protected $table = 'bill_payment_request_details';

    protected $fillable = [
        'bill_payment_request_id',
        'customer_id', 'customer_code', 'customer_name',
        'supplier_id', 'supplier_code', 'supplier_name',
        'employee_id', 'employee_code', 'employee_name',
        'contractable_id', 'contractable_type', 'contract_code', 'type_contract_import',
        'payment_money_request', 'payment_money_request_exchange',
        'payment_money_manage', 'payment_money_manage_exchange',
        'payment_money_accountant_debt', 'payment_money_accountant_debt_exchange',
        'payment_money_chief_accountant', 'payment_money_chief_accountant_exchange',
        'note', 'is_payment_begin', 'need_payment', 'work_id',
        'delivery_trip_id', 'delivery_trip_code',
        'other_delivery_trip_id', 'other_delivery_trip_code',
        'delivery_trip_accounting_id', 'delivery_trip_accounting_code',
        'other_delivery_trip_accounting_id', 'other_delivery_trip_accounting_code',
        'total_cost_transition',
    ];

    public function bill_payment_request()
    {
        return $this->belongsTo(BillPaymentRequest::class, 'bill_payment_request_id', 'id');
    }

    public function customer()
    {
        return $this->belongsTo(\Modules\Finance\Entities\Customer::class, 'customer_id', 'id');
    }

    public function supplier()
    {
        return $this->belongsTo(Supplier::class, 'supplier_id', 'id');
    }

    public function employee()
    {
        return $this->belongsTo(Employee::class, 'employee_id', 'id');
    }

    public function contractable()
    {
        return $this->morphTo();
    }
}
```

⚠️ Trước khi viết, kiểm tra tên class khách hàng đang dùng trong module (feature trước dùng `App\Models\TpCustomer`, KHÔNG phải `Modules\Assign\Entities\Customer`):
```bash
grep -rn "public function customer()" -A 3 Modules/Finance/Entities/BillIncomeRequest/BillIncomeRequestDetail.php
```
Dùng đúng class mà file đó đang dùng.

- [x] **Bước 8: Verify**

```bash
php -l Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php
php -l Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequestDetail.php
php artisan tinker --execute="\$m = Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest::with('details')->find(1); echo \$m->code.' | details='.\$m->details->count().' | status='.\$m->status;"
```
Kỳ vọng: in mã phiếu + số dòng chi tiết > 0.

Kiểm morph resolve được **toàn bộ 10 loại**:
```bash
php artisan tinker --execute="\$q = Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequestDetail::select('contractable_type')->distinct()->whereNotNull('contractable_type')->pluck('contractable_type'); foreach (\$q as \$t) { \$d = Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequestDetail::where('contractable_type', \$t)->first(); echo \$t.' => '.(optional(\$d->contractable)->code ?: 'NULL').PHP_EOL; }"
```
Kỳ vọng: **10 dòng, không dòng nào ném exception**.

- [x] **Bước 9 (vòng sửa 2 — 2026-08-15): vá 1 Important + 2 Minor của review**

1. **[Important] `searchByFilter()` fail-open khi chưa đăng nhập** → thêm đầu hàm:
   `if (!$employeeId) { return $query->whereRaw('1 = 0'); }`.
2. **[Minor] `canEdit()` so lỏng `==`** (`created_by` null gặp `auth()->id()` null → true) → viết lại:
   chặn `$employeeId` rỗng + `created_by !== null` + so `(int) === (int)` + `in_array(..., true)`.
3. **[Minor] scope `pending` khi user không gắn `employee_info`** (`$companyId` null →
   `where('company_id', null)` rơi thành `whereNull`) → `if ($companyId === null) { return $query->whereRaw('1 = 0'); }`.

**Verify chạy thật trên DB dev** (`php artisan tinker` + `php -l` sạch):

| Ca | Trước | Sau |
| --- | --- | --- |
| Guest, scope `all` / `mine` / `pending` / `approved` | `approved` khớp **4.036/4.040** | cả 4 scope ra SQL `where 1 = 0`, **count = 0** (bảng có 4.040 phiếu) |
| `canEdit()` guest + phiếu `created_by` NULL, status nháp | `true` | `false` |
| `canEdit()` đúng người + nháp / + chờ TP / + `created_by` NULL | — | `true` / `false` / `false` |
| scope `pending`, user không có `employee_info` | `where company_id is null` | `where 1 = 0`, count 0 |

📌 Ghi nhận: DB hiện **0 phiếu có `company_id` NULL** và **0 dòng `created_by` NULL** → 2 Minor là
lỗ hổng tiềm ẩn chứ chưa khai thác được bằng dữ liệu thật; vẫn sửa theo luật fail-closed của CLAUDE.md.

---

### Task 1.3 — 9 quyền mới + gán role

**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm sau dòng id 1152)
- Create: `Modules/Finance/Database/Seeders/BillPaymentRequestPermissionSeeder.php`

**Interfaces:**
- Produces: 9 bản ghi `permissions` id 1153–1161, `guard_name = 'api'`, `group = 'Đề nghị thanh toán'`, `type = 8`.
- Consumes: quyền `Kế toán thanh toán` id 1152 đã có (dùng lại, **không tạo trùng**).

- [x] **Bước 1: Thêm 9 dòng vào `PermissionsTableSeeder`**

```php
        Permission::create(['id' => 1153, 'guard_name' => 'api', 'name' => 'Kinh doanh đề nghị thanh toán', 'display_name' => 'Kinh doanh đề nghị thanh toán', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 1]);
        Permission::create(['id' => 1154, 'guard_name' => 'api', 'name' => 'Trưởng phòng duyệt đề nghị thanh toán', 'display_name' => 'Trưởng phòng duyệt đề nghị thanh toán', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 2]);
        Permission::create(['id' => 1155, 'guard_name' => 'api', 'name' => 'Kế toán công nợ duyệt đề nghị thanh toán', 'display_name' => 'Kế toán công nợ duyệt đề nghị thanh toán', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 3]);
        // ⚠️ 1156 + 1157 GIỮ NGUYÊN lỗi chính tả "đề nghi" của ERP (user chốt 2026-08-14) để đối
        // chiếu chéo quyền giữa 2 cổng không lệch tên. KHÔNG sửa thành "đề nghị".
        Permission::create(['id' => 1156, 'guard_name' => 'api', 'name' => 'Kế toán trưởng duyệt đề nghi thanh toán', 'display_name' => 'Kế toán trưởng duyệt đề nghi thanh toán', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 4]);
        Permission::create(['id' => 1157, 'guard_name' => 'api', 'name' => 'Ban giám đốc duyệt đề nghi thanh toán', 'display_name' => 'Ban giám đốc duyệt đề nghi thanh toán', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 5]);
        Permission::create(['id' => 1158, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty', 'display_name' => 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 6]);
        Permission::create(['id' => 1159, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thanh toán của công ty', 'display_name' => 'Xem tất cả phiếu đề nghị thanh toán của công ty', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 7]);
        Permission::create(['id' => 1160, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thanh toán của phòng ban', 'display_name' => 'Xem tất cả phiếu đề nghị thanh toán của phòng ban', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 8]);
        Permission::create(['id' => 1161, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu đề nghị thanh toán của bộ phận', 'display_name' => 'Xem tất cả phiếu đề nghị thanh toán của bộ phận', 'group' => 'Đề nghị thanh toán', 'type' => 8, 'sort_order' => 9]);
```

⚠️ Seeder này hiện **chạy lại sẽ nổ** vì trùng khoá ở cặp 1117/1118 (lỗi có sẵn, ghi trong STATUS.md) → **không chạy cả seeder**, chỉ INSERT 9 dòng vào DB dev bằng seeder riêng ở Bước 2.

- [x] **Bước 2: Seeder INSERT + gán role**

```php
<?php

namespace Modules\Finance\Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

/**
 * Nạp 9 quyền màn Đề nghị thanh toán vào DB dev + gán cho đúng role đang giữ quyền ERP cùng tên.
 *
 * KHÔNG chạy `PermissionsTableSeeder` toàn bộ: file đó khai TRÙNG id 1117/1118 (lỗi có sẵn)
 * nên chạy lại là nổ khoá. Seeder này chỉ đụng 9 id mới, idempotent.
 *
 * Ánh xạ role: quyền HRM (guard api) gán cho MỌI role đang có quyền ERP (guard web) cùng tên —
 * cùng cách đã dùng ở `BillIncomeRequestTestDataSeeder`.
 */
class BillPaymentRequestPermissionSeeder extends Seeder
{
    /** id HRM => tên quyền (khớp hằng số PERMISSION_* của Entity). */
    const PERMISSIONS = [
        1153 => 'Kinh doanh đề nghị thanh toán',
        1154 => 'Trưởng phòng duyệt đề nghị thanh toán',
        1155 => 'Kế toán công nợ duyệt đề nghị thanh toán',
        1156 => 'Kế toán trưởng duyệt đề nghi thanh toán',
        1157 => 'Ban giám đốc duyệt đề nghi thanh toán',
        1158 => 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty',
        1159 => 'Xem tất cả phiếu đề nghị thanh toán của công ty',
        1160 => 'Xem tất cả phiếu đề nghị thanh toán của phòng ban',
        1161 => 'Xem tất cả phiếu đề nghị thanh toán của bộ phận',
    ];

    public function run()
    {
        $sortOrder = 1;
        foreach (self::PERMISSIONS as $id => $name) {
            DB::table('permissions')->updateOrInsert(
                ['id' => $id],
                [
                    'name' => $name,
                    'display_name' => $name,
                    'guard_name' => 'api',
                    'group' => 'Đề nghị thanh toán',
                    'type' => 8,
                    'sort_order' => $sortOrder++,
                ]
            );

            // Role nào đang có quyền ERP (guard web) cùng tên thì nhận luôn quyền HRM tương ứng.
            $webId = DB::table('permissions')->where('name', $name)->where('guard_name', 'web')->value('id');
            if (!$webId) {
                continue;
            }

            $roleIds = DB::table('role_has_permissions')->where('permission_id', $webId)->pluck('role_id');
            foreach ($roleIds as $roleId) {
                DB::table('role_has_permissions')->updateOrInsert(
                    ['permission_id' => $id, 'role_id' => $roleId],
                    []
                );
            }
        }
    }
}
```

- [x] **Bước 3: Chạy + Verify**

```bash
php -l Modules/Finance/Database/Seeders/BillPaymentRequestPermissionSeeder.php
php artisan db:seed --class="Modules\Finance\Database\Seeders\BillPaymentRequestPermissionSeeder"
php artisan tinker --execute="echo DB::table('permissions')->whereBetween('id',[1153,1161])->count().' quyen | role_has: '.DB::table('role_has_permissions')->whereBetween('permission_id',[1153,1161])->count();"
```
Kỳ vọng: `9 quyen | role_has: >0`.

⚠️ Ghi lại số `role_has` vào checkpoint — nếu bằng 0 nghĩa là DB dev chưa có role nào giữ quyền ERP tương ứng, phải báo user để gán tay trước khi test.

**Kết quả thật (2026-08-15):** `9 quyen | role_has: 59`. Cả 9 id 1153–1161 trước đó **trống**
(max id bảng `permissions` = 101037, dải 1153–1161 chưa ai chiếm). 9 quyền ERP guard `web`
tương ứng đều tồn tại (`web#100202..100219`) và đang được 2–22 role giữ → map sang HRM đủ.
Chạy seeder **lần 2 không sinh thêm dòng nào** (59 → 59, permissions vẫn 9) — idempotent đạt.

📌 **Thêm so với plan (theo tiền lệ màn Đề nghị thu tiền):** seeder gán luôn 9 quyền cho
**role 18 `Super admin`** (guard `api`, 2.480 quyền). Lý do: FE `middleware/checkPermission.js`
so THẲNG tên quyền trong store, **không có nhánh bỏ qua cho super admin**, trong khi BE
`currentEmployeeIsSuperAdmin()` cho qua ⇒ không gán thì super admin bị đá 404 ngay cửa FE
(đúng bug đã gặp ở feature trước). Verify: role 18 giữ **9/9** quyền mới, và đã có sẵn 1152.

---

### Task 1.4 — `BillPaymentDebtService`

**Files:**
- Create: `Modules/Finance/Services/BillPaymentDebtService.php`

**Interfaces:**
- Produces: `getPaymentMoney(int $contractableId, string $contractableType, int $type, array $context): array` trả `['payment_money' => float, 'payment_money_foreign' => float]`.
  `$context` nhận `supplier_id` (loại 1), `customer_id` (loại 2), `employee_id` + `work_id` (loại 6).
- Consumes: `Modules\Finance\Entities\Account\Account`, `Modules\Finance\Entities\Accounting\AccountDetail` (đã có, dùng ở `BillIncomeDebtService`).

- [x] **Bước 1: Đọc khuôn**

Đọc `Modules/Finance/Services/BillIncomeDebtService.php` (89 dòng). Service mới **không sửa file đó** — chiều cộng/trừ ngược nhau nên phải là service riêng.

- [x] **Bước 2: Viết service**

```php
<?php

namespace Modules\Finance\Services;

use Modules\Finance\Entities\Account\Account;
use Modules\Finance\Entities\Accounting\AccountDetail;
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;

/**
 * "Số tiền còn nợ / còn lại" của 1 hợp đồng cho màn Phiếu đề nghị thanh toán.
 *
 * Port 3 nhánh của ERP (chiều NGƯỢC với màn Đề nghị thu tiền — ở đây mình NỢ đối tác):
 *   loại 1  Chi trả NCC              -> TK 3311, lọc (supplier_id OR customer_id) = supplier
 *   loại 2  Chi trả lại khách hàng   -> TK 1311, lọc customer_id
 *   loại 6  Chi thưởng thực hiện HĐ  -> TK 3351, lọc employee_id + work_id
 *   loại 12 Vận chuyển               -> KHÔNG qua đây (xem DeliveryTripPaymentService)
 *
 * Công thức: SUM(Có) − SUM(Nợ) trên `money_value_exchange` (ERP `AccountDetail::
 * getDataForBillPaymentRequest()` :1798 và `BuyContract2::getDataForBillPaymentRequest()` :149).
 * `payment_money_foreign` là cùng phép tính trên `money_value` (chưa quy đổi) — ERP chỉ trả
 * riêng cho `BuyContract2` / `BuyDebtContractBeginning`, các nguồn khác lấy bằng `payment_money`.
 *
 * ⚠️ Hợp đồng lấy từ `hrm_contracts` hiện CHƯA có bút toán nào trong `account_details` → trả 0.
 * Đúng thiết kế (user chốt giữ nguyên công thức ERP); khi có luồng hạch toán thì số tự lên.
 */
class BillPaymentDebtService
{
    const ACCOUNT_PAYABLE = 3311;        // Phải trả người bán
    const ACCOUNT_RECEIVABLE = 1311;     // Phải thu khách hàng
    const ACCOUNT_OTHER_PAYABLE = 3351;  // Phải trả khác (thưởng thực hiện HĐ)

    /** 2 nguồn ERP trả `payment_money_foreign` riêng; còn lại foreign = payment_money. */
    const FOREIGN_AWARE_TYPES = [
        'App\Model\Order\BuyContract2',
        'App\Model\Contract\BuyDebtContractBeginning',
    ];

    protected static $accountIdCache = [];

    public function getPaymentMoney($contractableId, $contractableType, int $type, array $context): array
    {
        if (!$contractableId || !$contractableType) {
            return ['payment_money' => 0.0, 'payment_money_foreign' => 0.0];
        }

        $accountId = $this->accountIdByIdentifyNumber($this->identifyNumberForType($type));
        if (!$accountId) {
            return ['payment_money' => 0.0, 'payment_money_foreign' => 0.0];
        }

        $query = AccountDetail::query()
            ->selectRaw('SUM(CASE WHEN type = ? THEN money_value_exchange ELSE 0 END) as debt_exchange', [AccountDetail::TYPE_DEBT])
            ->selectRaw('SUM(CASE WHEN type = ? THEN money_value_exchange ELSE 0 END) as have_exchange', [AccountDetail::TYPE_HAS])
            ->selectRaw('SUM(CASE WHEN type = ? THEN money_value ELSE 0 END) as debt_value', [AccountDetail::TYPE_DEBT])
            ->selectRaw('SUM(CASE WHEN type = ? THEN money_value ELSE 0 END) as have_value', [AccountDetail::TYPE_HAS])
            ->where('contractable_id', $contractableId)
            ->where('contractable_type', $contractableType)
            ->where('account_id', $accountId);

        if ($type === BillPaymentRequest::TYPE_SUPPLIER) {
            $supplierId = $context['supplier_id'] ?? null;
            $query->where(function ($q) use ($supplierId) {
                $q->where('supplier_id', $supplierId)->orWhere('customer_id', $supplierId);
            });
        } elseif ($type === BillPaymentRequest::TYPE_CUSTOMER_REFUND) {
            $query->where('customer_id', $context['customer_id'] ?? null);
        } elseif ($type === BillPaymentRequest::TYPE_CONTRACT_BONUS) {
            if (!empty($context['employee_id'])) {
                $query->where('employee_id', $context['employee_id']);
            }
            if (!empty($context['work_id'])) {
                $query->where('work_id', $context['work_id']);
            }
        }

        $row = $query->first();

        $money = (float) ($row->have_exchange ?? 0) - (float) ($row->debt_exchange ?? 0);
        $foreign = in_array($contractableType, self::FOREIGN_AWARE_TYPES, true)
            ? (float) ($row->have_value ?? 0) - (float) ($row->debt_value ?? 0)
            : $money;

        return ['payment_money' => $money, 'payment_money_foreign' => $foreign];
    }

    /** id `works` của mã vụ việc TTHHD — loại chi 6 lọc theo cột này (ERP `Work::getByCode()`). */
    public function workIdTTHHD(): ?int
    {
        $id = \Illuminate\Support\Facades\DB::table('works')->where('code', 'TTHHD')->value('id');

        return $id !== null ? (int) $id : null;
    }

    protected function identifyNumberForType(int $type): int
    {
        if ($type === BillPaymentRequest::TYPE_CUSTOMER_REFUND) {
            return self::ACCOUNT_RECEIVABLE;
        }
        if ($type === BillPaymentRequest::TYPE_CONTRACT_BONUS) {
            return self::ACCOUNT_OTHER_PAYABLE;
        }

        return self::ACCOUNT_PAYABLE;
    }

    protected function accountIdByIdentifyNumber(int $identifyNumber): ?int
    {
        if (array_key_exists($identifyNumber, self::$accountIdCache)) {
            return self::$accountIdCache[$identifyNumber];
        }

        $id = Account::query()->where('identify_number', $identifyNumber)->value('id');

        return self::$accountIdCache[$identifyNumber] = $id !== null ? (int) $id : null;
    }
}
```

⚠️ Kiểm tra tên hằng trong `AccountDetail` của HRM trước khi dùng (`TYPE_DEBT` / `TYPE_HAS` — feature trước dùng đúng 2 tên này, ERP là `TYPE_DEPT`/`TYPE_HAS`):
```bash
grep -n "const TYPE_" Modules/Finance/Entities/Accounting/AccountDetail.php
```

- [x] **Bước 3: Verify — đối chiếu ERP bằng dữ liệu thật**

```bash
php -l Modules/Finance/Services/BillPaymentDebtService.php
php artisan tinker --execute="\$s = app(Modules\Finance\Services\BillPaymentDebtService::class); \$d = Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequestDetail::where('contractable_type','App\\\\Model\\\\Order\\\\BuyContract2')->whereNotNull('supplier_id')->first(); print_r(\$s->getPaymentMoney(\$d->contractable_id, \$d->getRawOriginal('contractable_type'), 1, ['supplier_id' => \$d->supplier_id]));"
```

Đối chiếu bằng SQL thuần (thay `<ID>`, `<ACC>` bằng giá trị thật):
```sql
SELECT SUM(CASE WHEN type=2 THEN money_value_exchange ELSE 0 END)
     - SUM(CASE WHEN type=1 THEN money_value_exchange ELSE 0 END) AS con_no
FROM account_details
WHERE contractable_id = <ID> AND contractable_type = 'App\\Model\\Order\\BuyContract2'
  AND account_id = (SELECT id FROM accounts WHERE identify_number = 3311)
  AND (supplier_id = <SUP> OR customer_id = <SUP>);
```
Kỳ vọng: 2 số **khớp tuyệt đối**.

Làm tương tự 1 mẫu cho loại 2 (`FirmContract`, TK 1311) và 1 mẫu cho loại 6 (`FirmContract`, TK 3351 + `work_id` TTHHD).

**Kết quả thật (2026-08-15)** — không chỉ 3 mẫu mà đối chiếu **1.035 dòng chi tiết** với SQL thuần,
**lệch 0**:

| Loại chi | TK | Dòng đối chiếu | Lệch | Số dòng ra khác 0 |
| --- | --- | --- | --- | --- |
| 1 — Chi trả NCC | 3311 (`accounts.id`=99) | 400 | **0** | 145 |
| 2 — Chi trả lại KH | 1311 (id=22) | 235 | **0** | 11 |
| 6 — Thưởng thực hiện HĐ | 3351 (id=117) | 400 | **0** | 32 |

- Nhánh `payment_money_foreign` chạy đúng: `BuyContract2#76` ra `-20,00` (quy đổi) ≠ `-19,84` (nguyên tệ);
  nguồn ngoài `FOREIGN_AWARE_TYPES` thì 2 số bằng nhau.
- `workIdTTHHD()` = **12** (`works.code = 'TTHHD'` — "Thưởng thực hiện hợp đồng"), có memoize.
- Ca biên: `contractable_id` null / hợp đồng không tồn tại / loại 12 → đều trả `0.0` cho cả 2 số,
  không ném lỗi.
- 3 tài khoản đều CÓ thật trên DB: `1311` id 22 · `3311` id 99 · `3351` id 117.

📌 **Sửa một nhận định cũ của spec/design**: hợp đồng HRM **KHÔNG còn 0 bút toán** —
`account_details` đã có **59 dòng / 33 hợp đồng** `Modules\Assign\Entities\Contract\Contract`.
Nhưng **toàn bộ nằm ở TK 1311 và SUM(Có) − SUM(Nợ) đều ≤ 0** (số dư bên Nợ: khách nợ mình),
nên theo chiều CHI của màn này công nợ vẫn ra 0/âm ⇒ **quyết định "trần số tiền đề nghị chỉ áp
khi công nợ > 0" vẫn cần giữ**, lý do không đổi.

---

### Task 1.5 — Service đọc + 2 Resource

**Files:**
- Create: `Modules/Finance/Services/BillPaymentRequestService.php` (phần đọc)
- Create: `Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestListResource.php`
- Create: `Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestDetailResource.php`

**Interfaces:**
- Produces:
  - `searchByFilter(Request $r, string $scope = 'all')` → paginator (`per_page`, mặc định 10)
  - `findForShow(int $id): BillPaymentRequest` (eager-load đủ cho màn chi tiết)
  - `findOrFail(int $id): BillPaymentRequest`
  - `meta(): array` — `statuses`, `types`, `type_payments`, `costs`, 5 cờ quyền duyệt + 4 cờ quyền xem
  - `detailPaymentMoney(BillPaymentRequest $m): array` — map `detail_id => ['payment_money', 'payment_money_foreign', 'money_payed']`
- Consumes: `BillPaymentDebtService` (Task 1.4), `BillPaymentRequest` (Task 1.2).

- [x] **Bước 1: Đọc khuôn** — `Modules/Finance/Services/BillIncomeRequestService.php` (phần đọc, dòng 34–78) và 2 Resource tương ứng.

- [x] **Bước 2: Viết `searchByFilter` + `findForShow` + `findOrFail`**

```php
    public function searchByFilter(Request $request, string $scope = 'all')
    {
        $limit = (int) $request->get('per_page', 10);

        return BillPaymentRequest::searchByFilter($request, $scope)
            ->with(['details.customer', 'details.supplier', 'employee_create.info.department', 'currency'])
            ->paginate($limit);
    }

    public function findForShow(int $id): BillPaymentRequest
    {
        return BillPaymentRequest::query()
            ->with([
                'details.customer',
                'details.supplier',
                'details.employee.info',
                'details.contractable',
                'employee_create.info.department',
                'manage_approver.info',
                'accounting_approver.info',
                'chief_accounting_approver.info',
                'board_of_manager_approver.info',
                'currency',
            ])
            ->findOrFail($id);
    }
```

⚠️ **KHÔNG** eager-load `details.contractable` ở danh sách — 10 loại morph × mỗi trang là hàng chục query thừa; lưới không hiển thị mã hợp đồng.

- [x] **Bước 3: `detailPaymentMoney()` — công nợ từng dòng cho màn chi tiết**

```php
    /**
     * Công nợ + số đã trả của từng dòng chi tiết (port ERP `getDataForEdit()` :454).
     * Loại 12 không đi qua `BillPaymentDebtService`: `payment_money` = tổng cước − đã trả.
     */
    public function detailPaymentMoney(BillPaymentRequest $model): array
    {
        $type = (int) $model->type;
        $result = [];

        foreach ($model->details as $detail) {
            if ($type === BillPaymentRequest::TYPE_DELIVERY) {
                $moneyPayed = app(DeliveryTripPaymentService::class)->paidMoneyForDetail($detail);
                $result[$detail->id] = [
                    'payment_money' => (float) $detail->total_cost_transition - $moneyPayed,
                    'payment_money_foreign' => (float) $detail->total_cost_transition - $moneyPayed,
                    'money_payed' => $moneyPayed,
                ];
                continue;
            }

            $context = [
                'supplier_id' => (int) $model->type_payment === 1 ? $detail->supplier_id : $model->supplier_id,
                'customer_id' => $model->customer_id ?: $detail->customer_id,
                'employee_id' => $model->created_by,
                'work_id' => app(BillPaymentDebtService::class)->workIdTTHHD(),
            ];

            $money = app(BillPaymentDebtService::class)->getPaymentMoney(
                $detail->contractable_id,
                $detail->getRawOriginal('contractable_type'),
                $type,
                $context
            );

            $result[$detail->id] = $money + ['money_payed' => 0.0];
        }

        return $result;
    }
```

⚠️ `DeliveryTripPaymentService::paidMoneyForDetail()` làm ở **Task 3.2**. Tới Task 1.5 tạm để nhánh loại 12 trả `money_payed = 0` kèm `// TODO Task 3.2` — **và phải gỡ TODO khi làm Task 3.2** (ghi vào checkpoint Phase 3).

- [x] **Bước 4: `meta()`**

```php
    public function meta(): array
    {
        return [
            'meta' => [
                'statuses' => BillPaymentRequest::STATUSES,
                'types' => BillPaymentRequest::typeForSelect(),
                'type_payments' => BillPaymentRequest::typePaymentForSelect(),
                'costs' => BillPaymentRequest::costForSelect(),
                'can_view_all_company' => BillPaymentRequest::canViewAllCompany(),
                'can_view_company' => BillPaymentRequest::canViewCompany(),
                'can_view_department' => BillPaymentRequest::canViewDepartment(),
                'can_view_part' => BillPaymentRequest::canViewPart(),
                'can_approve_manage' => BillPaymentRequest::hasPermissionManage(),
                'can_approve_accounting_dept' => BillPaymentRequest::hasPermissionAccountingDept(),
                'can_approve_chief_accountant' => BillPaymentRequest::hasPermissionChiefAccountant(),
                'can_approve_board_of_manager' => BillPaymentRequest::hasPermissionBoardOfManager(),
                'is_accountant' => BillPaymentRequest::isAccountant(),
            ],
        ];
    }
```
→ Bổ sung 4 method `hasPermission*()` vào Entity (Task 1.2) nếu chưa có — mỗi cái là
`self::currentEmployeeIsSuperAdmin() || self::currentEmployeeHasPermission(self::PERMISSION_X)`.

- [x] **Bước 5: 2 Resource**

`BillPaymentRequestListResource` — các field lưới cần: `id`, `code`, `type`, `type_name`, `type_payment`, `type_payment_name`, `object_name` (KH/NCC theo đúng luật ERP `searchData` :78-97), `total_money` (đổi theo trạng thái, luật ở spec 4.3) + `currency_name`, `created_at` (`d/m/Y`), `manage_approved_time` (`d/m/Y` hoặc `null`), `created_by_name`, `department_name`, `status`, `status_name`, `can_edit`, `can_delete`.

`BillPaymentRequestDetailResource` — toàn bộ field Thông tin chung + mảng `details` (mỗi dòng kèm `payment_money`, `payment_money_foreign`, `money_payed`, `contract_code`, `contractable_type`) + `attachments` (mảng URL đã tách) + khối cờ quyền:
```php
            'can_edit' => $this->canEdit(),
            'can_delete' => $this->canDelete(),
            'can_approve' => $this->canApproveAtCurrentStatus(),
            'can_cancel' => $this->canCancel(),
            'next_statuses' => $this->nextStatuses(),
```

⚠️ `object_name` (cột "Khách hàng" của lưới) port đúng nhánh ERP:
- `type ∈ [2, 6]`: `type_payment == 2` → lấy `customer` của phiếu; ngược lại lấy `details[0].customer`
- `type == 1`: `type_payment == 2` → `supplier_code - supplier_name` của phiếu; ngược lại `details[0].supplier`
- `type == 12`: luôn `supplier_code - supplier_name` của phiếu

- [x] **Bước 6: Verify**

```bash
php -l Modules/Finance/Services/BillPaymentRequestService.php
php -l Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestListResource.php
php -l Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestDetailResource.php
```

**Kết quả thật (2026-08-15)** — `php -l` sạch 3 file, và chạy service + 2 Resource trên dữ liệu
thật (đăng nhập bằng nhân viên #590, người lập nhiều phiếu nhất):

- **4 chế độ** đều dựng được: `all`/`mine` = **1.148 phiếu**, `pending`/`approved` = 0
  (đúng: người này không giữ quyền duyệt nào, và DB gần như không có phiếu chờ duyệt).
- **Cột `total_money` đổi theo trạng thái**: đối chiếu **116 phiếu trải đủ 9 trạng thái có dữ liệu**
  với `SUM()` SQL của đúng cột theo bảng ánh xạ → **lệch 0**. (status 5 = 0 phiếu, đã biết trước.)
- **`object_name`** chạy đủ 4 loại × 2 hình thức, lấy đúng nguồn: loại 1 TM ra NCC của dòng đầu,
  loại 1 CK ra NCC của phiếu, loại 2 TM/CK ra KH tương ứng, loại 12 luôn ra NCC của phiếu.
- **`DetailResource`** mở được 1 phiếu mỗi loại: loại 1 (1 dòng, 2 file, morph
  `BuyDebtContractBeginning`, công nợ 442.323), loại 2, loại 6, loại 12 (**37 dòng**, `contract_code`
  NULL đúng bản chất chuyến xe).
- **Ca biên không nổ**: dòng `contractable_type = NULL` (phiếu #209) → `contract_code` null;
  phiếu có `attachments` → tách đúng **2 URL S3**; `meta()` trả 4 dropdown + **9 cờ quyền đều `false`**
  cho tài khoản không quyền (fail-closed đúng).

📌 **Đã chốt (user, 2026-08-15): GIỮ NGUYÊN NHƯ ERP.** Luật `object_name` của ERP xếp loại **6**
vào nhánh "lấy khách hàng", nhưng loại 6 là chi thưởng cho **NHÂN VIÊN** → cột "Khách hàng"
**luôn rỗng** với loại 6 (đo thật: **0/429** phiếu có tên KH, **67/429** có `employee_name`).
User chốt làm y như ERP ⇒ **không đổi `object_name`**, FE không thay cột. Field `employee_name`
vẫn trả trong list row (chi phí 0) nhưng **FE không dùng** — để sẵn nếu sau này đổi ý.

---

### Task 1.6 — Controller + routes

**Files:**
- Create: `Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php`
- Modify: `Modules/Finance/Routes/api.php`

**Interfaces:**
- Consumes: `BillPaymentRequestService` (Task 1.5), Entity (Task 1.2).
- Produces: 4 endpoint đọc `GET /` · `GET /pending` · `GET /approved` · `GET /{id}`.

- [x] **Bước 1: Controller (phase 1 — chỉ đọc)**

Bám `BillIncomeRequestController` (extends `ApiController`, dùng `listResponse()` / `responseJson()`). Bổ sung docblock đầu class giải thích **vì sao không gắn `checkPermission`** (copy ý từ file cũ).

```php
    /** Danh sách phiếu. `mode` = mine | all | pending | approved (mặc định all). */
    public function index(Request $request)
    {
        $scope = $this->resolveScope($request->get('mode'));

        return $this->listResponse($this->service->searchByFilter($request, $scope));
    }

    /** Màn "Chờ duyệt" — chỉ phiếu ở đúng trạng thái mà người đăng nhập có quyền duyệt. */
    public function pending(Request $request)
    {
        return $this->listResponse($this->service->searchByFilter($request, 'pending'));
    }

    /** Màn "Đã duyệt" — phiếu chính mình đã duyệt ở bất kỳ cấp nào. */
    public function approved(Request $request)
    {
        return $this->listResponse($this->service->searchByFilter($request, 'approved'));
    }

    public function show($id)
    {
        $model = $this->service->findForShow((int) $id);

        if (!$model->canView()) {
            return $this->responseJson('Bạn không có quyền xem phiếu này', 403);
        }

        return new BillPaymentRequestDetailResource($model);
    }

    /** Chỉ nhận 4 giá trị hợp lệ — `mode` lạ rơi về 'all' (đã bị chặn phạm vi bên trong). */
    private function resolveScope($mode): string
    {
        return in_array($mode, ['mine', 'all', 'pending', 'approved'], true) ? $mode : 'all';
    }
```

⚠️ **Không** gate `pending` bằng 403 như màn Đề nghị thu tiền: ở đây người duyệt có 5 vai khác nhau, `searchByFilter($r,'pending')` đã tự lọc theo quyền (không quyền nào → `1 = 0` → rỗng).

- [x] **Bước 2: Routes**

Thêm vào `Modules/Finance/Routes/api.php`, **trong cùng group** với `bill-income-requests`:

```php
    // Phieu de nghi thanh toan (bang ERP `bill_payment_requests` tren DB gop).
    // KHONG gan checkPermission cho route nao — ly do o docblock Controller.
    Route::group(['prefix' => '/bill-payment-requests'], function () {
        Route::get('/', [BillPaymentRequestController::class, 'index']);
        // Route tinh PHAI dat TRUOC /{id} de khong bi route dong nuot.
        Route::get('/pending', [BillPaymentRequestController::class, 'pending']);
        Route::get('/approved', [BillPaymentRequestController::class, 'approved']);
        Route::get('/{id}', [BillPaymentRequestController::class, 'show']);
    });
```

- [x] **Bước 3: Verify**

```bash
php -l Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php
php -l Modules/Finance/Routes/api.php
php artisan route:list --path=bill-payment-requests
```
Kỳ vọng: 4 route, `/pending` và `/approved` đứng **trước** `/{id}`.

**Kết quả thật (2026-08-15):** `php -l` sạch 2 file. Đúng **4 route**, thứ tự
`/` → `/pending` → `/approved` → `/{id}`, middleware `api, auth:api`, không route nào gắn
`checkPermission` (đúng thiết kế).

⚠️ **`php artisan route:list` KHÔNG chạy được trên repo này** — lỗi CÓ SẴN, không liên quan màn này:
`RequestUpdateTimeSheetController.php:51` gọi `isCurrentEmployeeHasPermission()` ở **thân file
route** (lúc nạp route chưa có user) → `PermissionHelper.php:23` nổ
"Trying to get property 'employee_info_id' of non-object". Thay bằng liệt kê qua
`app('router')->getRoutes()` trong tinker. Ai cần `route:list` sau này nhớ bẫy này.

---

### Task 1.7 — Verify Phase 1 bằng HTTP thật

**Files:** không tạo file.

- [x] **Bước 1: Lấy token của tài khoản có quyền**

```bash
php artisan tinker --execute="\$e = DB::table('employee_has_roles')->join('role_has_permissions','role_has_permissions.role_id','=','employee_has_roles.role_id')->whereIn('permission_id',[1154,1155,1156,1157])->pluck('employee_has_roles.model_id')->unique()->take(5); print_r(\$e->toArray());"
```
Chọn 1 id, đăng nhập lấy JWT (theo cách đã dùng ở feature trước).

- [x] **Bước 2: Gọi 4 endpoint**

```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests?per_page=5" | head -c 900
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests?mode=mine&per_page=5" | head -c 400
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/pending?per_page=5" | head -c 400
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/approved?per_page=5" | head -c 400
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/<ID_PHIEU_ERP>" | head -c 1200
```

- [x] **Bước 3: Đối chiếu số liệu với SQL thuần**

Với tài khoản có quyền "tổng công ty", `total` của `mode=all` phải bằng:
```sql
SELECT COUNT(*) FROM bill_payment_requests
WHERE status <> 1 OR created_by = <EMPLOYEE_ID>;
```
Kỳ vọng: khớp tuyệt đối (tổng 4.040 trừ đi số nháp của người khác).

**Kết quả thật (2026-08-15)** — server `php artisan serve 127.0.0.1:8123`, JWT sinh bằng
`auth('api')->login()`, gọi **thật** qua HTTP với **3 mức quyền**:

| Tài khoản | Quyền DNTT | `all` | SQL kỳ vọng | `pending` | `approved` |
| --- | --- | --- | --- | --- | --- |
| NV **36** (công ty 1) | đủ 1152–1161 | **4.021** | **4.021** ✅ | 116 | 0 |
| NV **147** (công ty 1) | 1152 · 1155 · 1156 · 1159 | **3.786** | **3.786** ✅ | **116** = SQL(cty1, status 3/4/6) ✅ | **2** = SQL 4 cột duyệt = 147 ✅ |
| NV **25** (công ty 1) | không có quyền nào | **0** | 0 ✅ | 0 ✅ | — |

- **Không token → 401**; NV25 mở phiếu #1 → **403** `"Bạn không có quyền xem phiếu này"`;
  id không tồn tại → **404**; đường dẫn lạ `/pendingx` → 404 (không bị `/{id}` nuốt).
- **`meta` trả đủ 21 khoá**, các cờ quyền đúng người: NV36 `can_view_all_company=true`,
  NV147 `can_view_company=true` + `can_view_all_company=false`, NV25 **tất cả false** (fail-closed).
- `show` trả đủ Thông tin chung + khối ngân hàng + `details` (phiếu #1: loại 1/CK, RUPEE,
  tỷ giá 315.83, status 8).

📌 **Giải thích 1 số thoạt nhìn tưởng sai**: NV36 giữ đủ 5 vai duyệt nhưng `pending` ra **116**
chứ không phải 119 (= số phiếu công ty 1 ở status 2–6). Đúng thiết kế: 3 phiếu chênh đang ở
status 2 (Chờ TP duyệt) thuộc phòng ban **46, 46, 95**, mà NV36 **không quản lý phòng ban nào**
(`employee_manage_departments` rỗng) → nhánh TP lọc đúng theo phòng ban được giao.

⚠️ 2 bẫy khi lấy tài khoản test: nhân viên có `status = 0` (vd NV82) luôn bị **401** dù đủ quyền;
và `employee_has_roles` khoá theo cột **`employee_id`**, KHÔNG phải `model_id` như lệnh mẫu ở
Bước 1 của plan (lệnh đó chạy sẽ lỗi "Unknown column").

- [x] **Bước 4: Ghi checkpoint** vào cuối file plan này.

---

### Task 1.8 — Kiểm 3 endpoint popup dùng lại (hợp đồng bán / hợp đồng mua / NCC)

**Files:**
- Modify *(chỉ khi thiếu)*: `Modules/Finance/Services/BillIncomeRequestService.php`

**Interfaces:**
- Consumes: `GET /finance/bill-income-requests/search-contracts` · `/search-buy-contracts` · `/search-suppliers` (đã có từ feature Đề nghị thu tiền).
- Produces: kết luận **dùng lại nguyên** hay **cần bổ sung**, ghi vào checkpoint.

> ⚠️ Task này tồn tại vì spec mục 5.1/5.2 nói "dùng lại endpoint đã có" nhưng bộ lọc của màn Đề nghị **thanh toán** không hoàn toàn trùng màn Đề nghị **thu**. Phải đối chiếu trước khi FE gọi, đừng giả định.

- [x] **Bước 1: Đối chiếu nguồn hợp đồng mua**

ERP `searchContractForPaymentSupplier()` UNION **6 nguồn**: `buy_contract2` · `inland_buy_contracts` · `inland_buy_contract_news` · `buy_debt_contract_beginnings` · `buy_service_contracts` · **`insurance_principle_forms`**.
`BillIncomeRequestService::searchBuyContracts()` hiện chỉ có **5 nguồn** (thiếu `insurance_principle_forms`).

Kiểm dữ liệu thật xem có đáng bổ sung không:
```bash
php artisan tinker --execute="echo DB::table('bill_payment_request_details')->where('contractable_type','App\\\\Model\\\\Insurance\\\\InsurancePrincipleForm')->count();"
```
- Ra **0** → ghi nhận "không bổ sung", dùng lại nguyên endpoint 5 nguồn.
- Ra **> 0** → thêm nguồn thứ 6 vào `searchBuyContracts()` **theo kiểu thuần thêm** (không đổi 5 nguồn cũ để không ảnh hưởng màn Đề nghị thu tiền đang chạy), kèm entity `InsurancePrincipleForm` + 1 dòng morphMap.

- [x] **Bước 2: Đối chiếu bộ lọc hợp đồng bán**

ERP `extrated()` với `type = create_bill` (loại chi 2) thêm điều kiện **`created_by = auth()->id()`** — người lập chỉ chọn được hợp đồng của chính mình. `searchSellContracts()` hiện **không** có điều kiện này.

→ **Không sửa** `searchSellContracts()` (đang phục vụ màn Đề nghị thu tiền đã nghiệm thu). Thay vào đó truyền tham số tuỳ chọn:
```php
        // Thuần THÊM: không truyền `only_mine` thì hành vi y hệt trước, màn Đề nghị thu tiền không đổi.
        if ($request->boolean('only_mine')) {
            $hrm->where('created_by', auth()->id());
            $wr->where('created_by', auth()->id());
        }
```
FE màn Đề nghị thanh toán gọi kèm `only_mine=1` khi `type = 2`; loại 6 (ERP `payment_TTHHD`) **không** lọc theo người lập.

- [x] **Bước 3: Verify**

**Kết luận Bước 1 — KHÔNG bổ sung nguồn thứ 6.** `bill_payment_request_details` có **0 dòng**
`App\Model\Insurance\InsurancePrincipleForm` (đếm thật). Dùng lại nguyên endpoint 5 nguồn,
**không** tạo entity `InsurancePrincipleForm`, **không** thêm morphMap.
⇒ Đây cũng là câu trả lời cho **Ruling #5**: `allowedContractTypes()` giữ nguyên, không liệt kê
class không tồn tại. Phân bố morph thật của bảng chi tiết (7.188 dòng): `BuyContract2` 2.733 ·
`InlandBuyContractNew` 1.875 · `BuyDebtContractBeginning` 951 · `InlandBuyContract` 929 ·
**NULL 754** · `FirmContract` 733 · `BuyServiceContract` 110 · `OpeningContract` 52 ·
`WarehouseImport` 25 · `WarehouseExport` 15 · `WrServiceContract` 11.

**Bước 2 — đã thêm `only_mine` (thuần thêm) vào `searchSellContracts()`**, kèm fail-closed:
chưa đăng nhập thì ra `1 = 0` chứ không rơi về `where created_by is null`.
Cờ chỉ áp cho `hrm_contracts` + `wr_service_contracts`; **không** áp cho `opening_contracts`
(hợp đồng đầu kỳ là dữ liệu chuyển sổ, `created_by` là người nhập liệu — lọc theo sẽ làm rỗng
popup, ERP cũng không lọc). Cả 3 bảng đều CÓ cột `created_by` (đã kiểm), nên đây là quyết định
nghiệp vụ chứ không phải giới hạn schema.

**Kết quả gọi thật (2026-08-15, KH 916 / NCC 30725):**

| Lần gọi | Kết quả |
| --- | --- |
| `search-contracts?customer_id=916` — NV13 | **45** |
| `search-contracts?customer_id=916` — NV36 | **45** (bằng hệt ⇒ **không phá màn Đề nghị thu tiền**) |
| `+ only_mine=1` — NV13 (người lập 3 HĐ của KH này) | **5** |
| `+ only_mine=1` — NV36 | **3** (khác người khác số ⇒ cờ ăn đúng theo người đăng nhập) |
| `search-buy-contracts?supplier_id=30725` | **104** |
| `search-suppliers` | **9.547** (khớp con số đã nghiệm thu ở feature trước) |
| `search-contracts` thiếu `customer_id` | **422** |

⇒ **Dùng lại được cả 3 endpoint**, FE màn Đề nghị thanh toán chỉ cần thêm `only_mine=1` khi loại chi = 2.

---

# Phase 2 — BE ghi: tạo/sửa/xóa + luồng duyệt 5 cấp

### Task 2.1 — FormRequest Store / Update

**Files:**
- Create: `Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestStoreRequest.php`
- Create: `Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestUpdateRequest.php`

**Interfaces:**
- Produces: rule set đầy đủ theo ma trận nhánh loại chi (spec 8.3). `UpdateRequest extends StoreRequest` (khuôn `BillIncomeRequestUpdateRequest` 16 dòng).

- [x] **Bước 1: Ma trận nhánh (dựng đầu `rules()`)**

```php
        $type = (int) $this->get('type');
        $typePayment = (int) $this->get('type_payment');
        $supplierType = (int) $this->get('supplier_type');   // 3 = NCC nước ngoài

        $isSupplier = $type === BillPaymentRequest::TYPE_SUPPLIER;
        $isCustomer = $type === BillPaymentRequest::TYPE_CUSTOMER_REFUND;
        $isBonus    = $type === BillPaymentRequest::TYPE_CONTRACT_BONUS;
        $isDelivery = $type === BillPaymentRequest::TYPE_DELIVERY;

        $isCash     = $typePayment === 1;
        $isTransfer = $typePayment === 2;

        $supplierForeign = $isSupplier && $isTransfer && $supplierType === 3;
        $supplierInland  = $isSupplier && $isTransfer && $supplierType && $supplierType !== 3;
        $needBankInland  = $supplierInland || ($isCustomer && $isTransfer) || ($isBonus && $isTransfer) || ($isDelivery && $isTransfer);
        $hasContract     = $isSupplier || $isCustomer || $isBonus;
```

- [x] **Bước 2: Rule chính**

```php
        $rules = [
            'type' => ['required', Rule::in(BillPaymentRequest::TYPES_ALLOWED)],
            'type_payment' => ['required', Rule::in([1, 2])],
            'reason' => 'required|string',
            'type_money_id' => 'required|integer|exists:currencies,id',
            'exchange_rate' => 'required|numeric|gt:0',
            'status' => ['required', Rule::in([BillPaymentRequest::STATUS_CREATING, BillPaymentRequest::STATUS_AWAITING_MANAGE])],

            'to_date' => [Rule::requiredIf($isDelivery), 'nullable', 'date'],
            'customer_id' => [Rule::requiredIf($isCustomer && $isTransfer)],
            'supplier_id' => [Rule::requiredIf(($isSupplier && $isTransfer) || $isDelivery)],

            'account_number' => [Rule::requiredIf($needBankInland || $supplierForeign)],
            'account_name' => [Rule::requiredIf($needBankInland || $supplierForeign)],
            'bank_name' => [Rule::requiredIf($needBankInland || $supplierForeign)],
            'bank_branch' => [Rule::requiredIf($needBankInland)],
            'bank_province_id' => [Rule::requiredIf($needBankInland)],
            'bank_province_name' => [Rule::requiredIf($needBankInland)],

            'bank_id' => [Rule::requiredIf($supplierForeign)],
            'swift_code' => [Rule::requiredIf($supplierForeign)],
            'cost' => [Rule::requiredIf($supplierForeign), 'nullable', Rule::in([1, 2, 3])],

            'details' => 'required|array|min:1',
            'details.*.customer_id' => [Rule::requiredIf($isCustomer && $isCash)],
            'details.*.supplier_id' => [Rule::requiredIf($isSupplier && $isCash)],
            'details.*.contractable_id' => [Rule::requiredIf($hasContract)],
            'details.*.contractable_type' => [
                Rule::requiredIf($hasContract),
                'nullable',
                Rule::in(BillPaymentRequest::allowedContractTypes($type)),
            ],
        ];

        // Loại 12: dòng không tick "cần thanh toán" thì không bắt nhập tiền.
        foreach ((array) $this->get('details', []) as $i => $detail) {
            if ($isDelivery && empty($detail['need_payment'])) {
                continue;
            }
            $rules['details.' . $i . '.payment_money_request'] = 'required|numeric|min:1';
        }

        // Loại chi 1 bắt buộc có file — trừ khi phiếu đang sửa đã có sẵn file.
        $hasExistingFiles = $this->route('id')
            && BillPaymentRequest::query()->whereKey($this->route('id'))->value('attachments');
        if ($isSupplier && !$hasExistingFiles) {
            $rules['attachments'] = 'required|array|min:1';
        } else {
            $rules['attachments'] = 'nullable|array';
        }
        $rules['attachments.*'] = 'string';

        return $rules;
```

⚠️ `allowedContractTypes(int $type)` (Entity, Task 1.2) trả danh sách chuỗi morph hợp lệ:
- `type = 1` → 6 nguồn mua (`BuyContract2`, `InlandBuyContract`, `InlandBuyContractNew`, `BuyDebtContractBeginning`, `BuyServiceContract`, `InsurancePrincipleForm`)
- `type ∈ [2, 6]` → 3 nguồn bán (`Modules\Assign\Entities\Contract\Contract`, `OpeningContract`, `WrServiceContract`)
- `type = 12` → `[]`

Lấy chuỗi bằng `(new $class())->getMorphClass()`, **không viết tay** (sai 1 ký tự là phiếu ghi xong không mở lại được).

- [x] **Bước 3: `messages()`** — dùng đúng câu chữ chuẩn đã thống nhất: `Bắt buộc nhập` · `Phải là số` · `Không được nhỏ hơn :min` · `Tối đa :max`.

- [x] **Bước 4: Verify**

```bash
php -l Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestStoreRequest.php
php -l Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestUpdateRequest.php
```

Chạy Validator thật với 3 payload (hợp lệ loại 1 CK NCC nước ngoài / thiếu `swift_code` / `exchange_rate = 0`):
```bash
php artisan tinker --execute="\$r = new Modules\Finance\Http\Requests\BillPaymentRequest\BillPaymentRequestStoreRequest(); \$r->merge(['type'=>1,'type_payment'=>2,'supplier_type'=>3,'exchange_rate'=>0,'details'=>[[]]]); \$v = Validator::make(\$r->all(), \$r->rules(), \$r->messages()); print_r(\$v->errors()->toArray());"
```
Kỳ vọng: có lỗi ở `exchange_rate`, `swift_code`, `bank_id`, `cost`, `reason`, `details.0.payment_money_request`.

**Kết quả thật (2026-08-15):** `php -l` sạch 2 file; chạy Validator thật **15 ca — 15/15 đạt**
(mỗi ca so KHỚP TUYỆT ĐỐI tập khoá lỗi, thiếu hay thừa đều tính trượt).

*10 ca xấu bị chặn đúng:* payload rỗng · loại 1/CK/NCC nước ngoài thiếu ngân hàng + `exchange_rate = 0`
(12 lỗi cùng lúc) · `type = 3` (loại đã bỏ) · **`status = 6` nhảy cóc qua 4 cấp duyệt** ·
`details: []` · `contractable_type` bịa · **loại 2 gửi morph của hợp đồng MUA** · loại 12 thiếu
`to_date` + NCC · loại 2/TM không chọn KH ở dòng · `payment_money_request = 0`.

*5 ca tốt lọt sạch:* loại 1/CK NCC nước ngoài đủ trường · loại 1/TM (chọn NCC theo dòng, vẫn bắt
file) · loại 6/TM (không bắt file, không bắt KH) · **loại 12 với dòng không tick `need_payment`
thì không bắt nhập tiền** · loại 12/CK đủ khối ngân hàng trong nước.

📌 2 điểm làm rõ khi verify:
- `attachments` chỉ bắt buộc khi `type = 1`; payload không có `type` thì **không** báo thiếu file
  (đúng thiết kế, không phải bỏ sót).
- `allowedContractTypes(1)` trả **5** class (không có `InsurancePrincipleForm`) — khớp kết luận
  Task 1.8: DB 0 dòng dùng loại đó, không tạo entity.

---

### Task 2.2 — Service ghi: store / update / destroy / syncDetails

**Files:**
- Modify: `Modules/Finance/Services/BillPaymentRequestService.php`

**Interfaces:**
- Produces: `store(Request $r): BillPaymentRequest` · `update(Request $r, BillPaymentRequest $m): BillPaymentRequest` · `destroy(BillPaymentRequest $m): void` · `private syncDetails(BillPaymentRequest $m, array $details): void` · `private masterPayload(Request $r): array`
- Consumes: `generateCode()`, `BillPaymentRequestNotifyService` (Task 2.5), `BillPaymentAttachmentService` (Task 4.1).

> ⚠️ **Thứ tự thực hiện**: `store()` gọi `$this->notifyService` và `$this->attachmentService` — cả 2 nhận qua **constructor injection**:
> ```php
>     public function __construct(
>         BillPaymentRequestNotifyService $notifyService,
>         BillPaymentAttachmentService $attachmentService
>     ) {
>         $this->notifyService = $notifyService;
>         $this->attachmentService = $attachmentService;
>     }
> ```
> Nếu chạy tuần tự thì làm **Task 2.5 và Task 4.1 trước Task 2.2**; nếu làm song song thì tạo 2 class rỗng (chỉ khai method, thân trống) ở Task 2.2 rồi điền thân ở task của nó.

- [x] **Bước 1: `store()`**

Bám `BillIncomeRequestService::store()`: bọc `DB::transaction`, `generateCode()` bên trong transaction, không catch `Exception`.

```php
    public function store(Request $request): BillPaymentRequest
    {
        return DB::transaction(function () use ($request) {
            $model = BillPaymentRequest::create($this->masterPayload($request) + [
                'code' => BillPaymentRequest::generateCode(),
                'has_contract' => 1,   // ERP luôn ghi 1 (cột = 1 ở cả 4.040 phiếu, ô chọn đã bị comment)
            ]);

            $this->syncDetails($model, (array) $request->get('details', []));
            $this->attachmentService->sync($model, (array) $request->get('attachments', []));

            if ((int) $model->status === BillPaymentRequest::STATUS_AWAITING_MANAGE) {
                $this->notifyService->onSubmitted($model);
            }

            return $model;
        });
    }
```

`masterPayload()` gom đúng các cột Thông tin chung theo loại chi — **xóa trắng** các cột không thuộc nhánh hiện tại (port `clearInfoBank()` của ERP) để phiếu đổi loại chi không còn dữ liệu thừa của loại cũ.

- [x] **Bước 2: `syncDetails()`**

Xóa hết dòng cũ rồi insert mới (đúng cách ERP). 2 điểm phải giữ:
```php
        foreach ($details as $detail) {
            // ERP bỏ qua dòng không tick "cần thanh toán" (chỉ có ở loại 12).
            if (array_key_exists('need_payment', $detail) && !$detail['need_payment']) {
                continue;
            }
            BillPaymentRequestDetail::create([
                'bill_payment_request_id' => $model->id,
                // ... map đủ cột, xem $fillable của Entity
                'payment_money_request' => $detail['payment_money_request'] ?? 0,
                'payment_money_request_exchange' => ($detail['payment_money_request'] ?? 0) * (float) $model->exchange_rate,
                'is_payment_begin' => 0,   // nhánh "Chi đầu kỳ" đã bỏ
                'need_payment' => $detail['need_payment'] ?? 1,
            ]);
        }
```
⚠️ `*_exchange` **tính lại ở BE** theo `exchange_rate` của phiếu, **không tin số FE gửi** (ERP tin FE → lệch tỷ giá là sai tiền).

⚠️ **KHÔNG** đụng bảng `bill_payment_request_detail_product_export_requests`, kể cả xóa.

- [x] **Bước 3: `update()` + `destroy()`**

`update()` giống `store()` nhưng không đổi `code` / `created_by` / 3 cột tổ chức; chỉ bắn thông báo khi phiếu **chuyển từ nháp/không duyệt sang chờ TP duyệt**.
`destroy()` xóa details rồi xóa master, trong transaction.

- [x] **Bước 4: Verify** `php -l`, test thật ở Task 2.6.

---

### Task 2.3 — `BillPaymentApprovalService` — duyệt theo cấp

**Files:**
- Create: `Modules/Finance/Services/BillPaymentApprovalService.php`
- Create: `Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestApproveRequest.php`

**Interfaces:**
- Produces: `approve(Request $r, BillPaymentRequest $m): BillPaymentRequest`
- Consumes: `BillPaymentRequest::nextStatuses()`, `BillPaymentRequestNotifyService` (inject qua constructor).

> ⚠️ **Lệch spec 8.2 có chủ đích**: spec ghi "dùng chung `PUT /{id}` cho cả sửa lẫn duyệt (giữ nguyên ERP)". Plan tách riêng **`POST /{id}/approve`** vì gộp 1 endpoint bắt buộc phải nới `canEdit()` cho người duyệt (họ không phải người tạo) — mở đúng cái lỗ mà mục 8.3 yêu cầu bịt. Tách ra thì `PUT /{id}` giữ nguyên gate `canEdit()` (chỉ người tạo, chỉ status 1/10) và `approve` gate bằng `canApproveAtCurrentStatus()`, mỗi endpoint một bộ validate riêng. FE là bên duy nhất gọi 2 endpoint này nên không ảnh hưởng tương thích với ERP (ERP có route riêng của nó). Ghi lại vào spec khi wrap up.

- [x] **Bước 1: FormRequest duyệt**

```php
    public function rules()
    {
        return [
            'status' => 'required|integer',
            'details' => 'required|array|min:1',
            'details.*.id' => 'required|integer',
            'details.*.money' => 'required|numeric|min:0',
        ];
    }
```
(Validate `status` có nằm trong `nextStatuses()` không thì làm ở Service — cần model, FormRequest không có.)

- [x] **Bước 2: Bảng cột tiền theo trạng thái NGUỒN**

```php
    /** Trạng thái hiện tại của phiếu => cột tiền mà cấp đang duyệt ghi vào, và cột trần của nó. */
    const MONEY_COLUMN_BY_STATUS = [
        BillPaymentRequest::STATUS_AWAITING_MANAGE => ['payment_money_manage', 'payment_money_request'],
        BillPaymentRequest::STATUS_AWAITING_ACCOUNTING_DEPT => ['payment_money_accountant_debt', 'payment_money_manage'],
        BillPaymentRequest::STATUS_AWAITING_CHIEF_ACCOUNTANT => ['payment_money_chief_accountant', 'payment_money_accountant_debt'],
        BillPaymentRequest::STATUS_AWAITING_BOARD_OF_MANAGER => ['payment_money_chief_accountant', 'payment_money_accountant_debt'],
    ];
```

⚠️ Trạng thái 5 (BGĐ) ghi **cùng cột** với KT trưởng — đúng như ERP (`update()` :266-268 dùng `payment_money_chief_accountant` cho cả 2).

- [x] **Bước 3: `approve()`**

```php
    public function approve(Request $request, BillPaymentRequest $model): BillPaymentRequest
    {
        $currentStatus = (int) $model->status;
        $nextStatus = (int) $request->get('status');

        if (!in_array($nextStatus, $model->nextStatuses(), true)) {
            throw ValidationException::withMessages([
                'status' => 'Không thể chuyển phiếu sang trạng thái này',
            ]);
        }

        [$column, $capColumn] = self::MONEY_COLUMN_BY_STATUS[$currentStatus];
        $exchangeRate = (float) $model->exchange_rate;

        return DB::transaction(function () use ($request, $model, $currentStatus, $nextStatus, $column, $capColumn, $exchangeRate) {
            foreach ((array) $request->get('details', []) as $row) {
                $detail = $model->details->firstWhere('id', $row['id']);
                if (!$detail) {
                    continue;
                }

                // Trần = số tiền cấp trước đã duyệt. Cắt ở BE, KHÔNG tin FE (ERP chỉ cắt ở FE).
                $cap = (float) $detail->{$capColumn};
                $money = min((float) $row['money'], $cap);

                $detail->update([
                    $column => $money,
                    $column . '_exchange' => $money * $exchangeRate,
                ]);
            }

            $model->status = $nextStatus;
            $this->stampApprover($model, $currentStatus);
            $model->save();

            $this->notifyService->onApproved($model, $currentStatus, $nextStatus);

            return $model->refresh();
        });
    }

    /** Ghi lại người duyệt + thời điểm của cấp vừa xử lý (port ERP `update()` :305-365). */
    private function stampApprover(BillPaymentRequest $model, int $currentStatus): void
    {
        $employeeId = auth()->id();

        if ($currentStatus === BillPaymentRequest::STATUS_AWAITING_MANAGE) {
            $model->manage_approved_id = $employeeId;
            $model->manage_approved_time = now()->format('Y-m-d H:i:s');
        } elseif ($currentStatus === BillPaymentRequest::STATUS_AWAITING_ACCOUNTING_DEPT) {
            $model->accounting_approved_id = $employeeId;
        } elseif ($currentStatus === BillPaymentRequest::STATUS_AWAITING_CHIEF_ACCOUNTANT) {
            $model->chief_accounting_approved_id = $employeeId;
        } elseif ($currentStatus === BillPaymentRequest::STATUS_AWAITING_BOARD_OF_MANAGER) {
            $model->board_of_manager_approved_id = $employeeId;
        }
    }
```

- [x] **Bước 4: Verify** `php -l` cả 2 file; test thật ở Task 2.6.

---

### Task 2.4 — Không duyệt (`changeStatus`)

**Files:**
- Create: `Modules/Finance/Http/Requests/BillPaymentRequest/BillPaymentRequestChangeStatusRequest.php`
- Modify: `Modules/Finance/Services/BillPaymentApprovalService.php`

**Interfaces:**
- Produces: `reject(Request $r, BillPaymentRequest $m): BillPaymentRequest`

- [x] **Bước 1: FormRequest** — bắt buộc ghi chú của **đúng cấp** đang giữ phiếu:

```php
    public function rules()
    {
        $model = BillPaymentRequest::query()->find($this->route('id'));
        $status = $model ? (int) $model->status : 0;

        return [
            'reject_comment' => 'nullable|string',
            'note' => [Rule::requiredIf($status === BillPaymentRequest::STATUS_AWAITING_MANAGE)],
            'note_accountant_dept' => [Rule::requiredIf($status === BillPaymentRequest::STATUS_AWAITING_ACCOUNTING_DEPT)],
            'note_chief_accountant' => [Rule::requiredIf($status === BillPaymentRequest::STATUS_AWAITING_CHIEF_ACCOUNTANT)],
            'note_board_of_manager' => [Rule::requiredIf($status === BillPaymentRequest::STATUS_AWAITING_BOARD_OF_MANAGER)],
        ];
    }
```

- [x] **Bước 2: `reject()`**

```php
    public function reject(Request $request, BillPaymentRequest $model): BillPaymentRequest
    {
        $statusBefore = (int) $model->status;

        $model->fill([
            'note' => $request->get('note', $model->note),
            'note_accountant_dept' => $request->get('note_accountant_dept', $model->note_accountant_dept),
            'note_chief_accountant' => $request->get('note_chief_accountant', $model->note_chief_accountant),
            'note_board_of_manager' => $request->get('note_board_of_manager', $model->note_board_of_manager),
            'reject_comment' => $request->get('reject_comment'),
        ]);

        // ⚠️ Bẫy ERP phải giữ (`changeStatus()` :531-533): không duyệt Ở CẤP TP thì phiếu quay về
        // "Đang tạo" (1) để người lập sửa tiếp, KHÔNG phải "Không duyệt" (10). Các cấp sau mới về 10.
        $model->status = $statusBefore === BillPaymentRequest::STATUS_AWAITING_MANAGE
            ? BillPaymentRequest::STATUS_CREATING
            : BillPaymentRequest::STATUS_REJECT;

        $model->save();

        $this->notifyService->onRejected($model, $statusBefore);

        return $model->refresh();
    }
```

- [x] **Bước 3: Verify** `php -l`; test thật ở Task 2.6.

---

### Task 2.5 — Thông báo

**Files:**
- Create: `Modules/Finance/Services/BillPaymentRequestNotifyService.php`

**Interfaces:**
- Produces: `onSubmitted(BillPaymentRequest $m)` · `onApproved(BillPaymentRequest $m, int $from, int $to)` · `onRejected(BillPaymentRequest $m, int $statusBefore)`
- Consumes: `BillPaymentRequest::employeeInfoIdsHavingPermission()`, `EmployeeInfoService::sendNotification()`.

- [x] **Bước 1: Đọc khuôn** — `BillIncomeRequestService::notifyAccountants()` + `buildNotificationContent()` (dòng 357–430) và `.claude/skills/notification-convention/SKILL.md`.

- [x] **Bước 2: Bảng người nhận theo sự kiện**

```php
    /** Trạng thái MỚI => quyền của nhóm cần nhận thông báo "có việc cần duyệt". */
    const RECEIVER_PERMISSION_BY_STATUS = [
        BillPaymentRequest::STATUS_AWAITING_MANAGE => BillPaymentRequest::PERMISSION_MANAGE,
        BillPaymentRequest::STATUS_AWAITING_ACCOUNTING_DEPT => BillPaymentRequest::PERMISSION_ACCOUNTING_DEPT,
        BillPaymentRequest::STATUS_AWAITING_CHIEF_ACCOUNTANT => BillPaymentRequest::PERMISSION_CHIEF_ACCOUNTANT,
        BillPaymentRequest::STATUS_AWAITING_BOARD_OF_MANAGER => BillPaymentRequest::PERMISSION_BOARD_OF_MANAGER,
        BillPaymentRequest::STATUS_AWAITING_CREATE_BILL_PAYMENT => BillPaymentRequest::PERMISSION_ACCOUNTANT,
    ];

    /** Không duyệt: báo cho TẤT CẢ các cấp đã đi qua (port ERP `getPermissionWhenCancel()` :750). */
    const CANCEL_RECEIVERS = [
        BillPaymentRequest::STATUS_AWAITING_MANAGE => [BillPaymentRequest::PERMISSION_SALE],
        BillPaymentRequest::STATUS_AWAITING_ACCOUNTING_DEPT => [BillPaymentRequest::PERMISSION_SALE, BillPaymentRequest::PERMISSION_MANAGE],
        BillPaymentRequest::STATUS_AWAITING_CHIEF_ACCOUNTANT => [BillPaymentRequest::PERMISSION_SALE, BillPaymentRequest::PERMISSION_MANAGE, BillPaymentRequest::PERMISSION_ACCOUNTING_DEPT],
        BillPaymentRequest::STATUS_AWAITING_BOARD_OF_MANAGER => [BillPaymentRequest::PERMISSION_SALE, BillPaymentRequest::PERMISSION_MANAGE, BillPaymentRequest::PERMISSION_ACCOUNTING_DEPT, BillPaymentRequest::PERMISSION_CHIEF_ACCOUNTANT],
        BillPaymentRequest::STATUS_AWAITING_CREATE_BILL_PAYMENT => [BillPaymentRequest::PERMISSION_SALE, BillPaymentRequest::PERMISSION_MANAGE, BillPaymentRequest::PERMISSION_ACCOUNTING_DEPT, BillPaymentRequest::PERMISSION_CHIEF_ACCOUNTANT, BillPaymentRequest::PERMISSION_BOARD_OF_MANAGER],
    ];
```

`onApproved()` ngoài nhóm cấp kế tiếp còn báo ngược cho **người lập** và **người duyệt cấp liền trước** (đọc từ 4 cột `*_approved_id`).

- [x] **Bước 3: Nội dung thông báo**

Prefix `[DNTT-Chi]`, in đậm mã phiếu, deep-link `/finance/bill-payment-requests/{id}`, ≤ 120 ký tự (cắt ghi chú trước, rồi cắt tên):
```
[DNTT-Chi] Chờ duyệt: <b>{mã phiếu}</b>. Người đề nghị: {tên}. Số tiền: {tổng}
[DNTT-Chi] Đã duyệt: <b>{mã phiếu}</b>. Cấp duyệt: {tên cấp}.
[DNTT-Chi] Không duyệt: <b>{mã phiếu}</b>. Lý do: {reject_comment}
```

- [x] **Bước 4: Chống vỡ luồng chính**

Bọc `try/catch \Throwable` **2 lớp** (toàn hàm + từng người nhận) như file mẫu — lỗi gửi thông báo không được rollback phiếu.

- [x] **Bước 5: Verify**

```bash
php -l Modules/Finance/Services/BillPaymentRequestNotifyService.php
php artisan tinker --execute="echo count(Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest::employeeInfoIdsHavingPermission('Trưởng phòng duyệt đề nghị thanh toán', null));"
```
Kỳ vọng: số người nhận ≥ 0 (nếu 0 → ghi vào checkpoint, cần gán quyền trước khi test).

**Kết quả thật (2026-08-15):** `php -l` sạch. Đo trên DB (công ty 1) — **mọi nhóm đều có người
nhận**, không phải gán quyền tay:

| Nhóm | Kinh doanh | Trưởng phòng | KT công nợ | KT trưởng | BGĐ | KT thanh toán |
| --- | --- | --- | --- | --- | --- | --- |
| Số người | 12 | 37 | 31 | 31 | 17 | 32 |

Nội dung dựng thật (đo độ dài trên bản đã bỏ thẻ HTML):
```
[ 90] [DNTT-Chi] Chờ duyệt: <b>TPE.DNTT0825.00001</b>. Người đề nghị: … Số tiền: 27.391.936
[ 65] [DNTT-Chi] Đã duyệt: <b>TPE.DNTT0825.00001</b>. Cấp duyệt: Trưởng phòng.
[ 90] [DNTT-Chi] Từ chối: <b>TPE.DNTT0825.00001</b>. Lý do: Sai số tài khoản ngân hàng…
[119] (lý do dài 280 ký tự) → cắt còn 119, kết thúc bằng `...`
```
`levelName()` đúng 5 cấp, trạng thái lạ trả rỗng · `infoIdsOfEmployees([36,147,null,0])` → `[25,138]`
(lọc sạch null/0/id không tồn tại) · `approverIdAtStatus()` đọc đúng cột theo cấp ·
`onSubmitted()`/`onRejected()` với phiếu `company_id = null` + status lạ **không ném exception**.

⚠️ **2 lệch có chủ đích so với plan** (ghi rõ trong docblock service):
1. Nhóm hành động khi không duyệt dùng **`Từ chối`** chứ không phải `Không duyệt` —
   `.claude/skills/notification-convention/SKILL.md` chốt cứng **14 giá trị** và không có
   "Không duyệt" ("Không duyệt" là nhãn NÚT trên màn, không phải nhóm hành động thông báo).
2. Khi ghi chú quá dài thì **cắt ngắn + `...`** trước, chỉ bỏ hẳn khi cắt vẫn không đủ chỗ.
   Khuôn cũ (`BillIncomeRequestService`) bỏ nguyên câu ⇒ thông báo từ chối mất luôn lý do —
   đúng thứ duy nhất người lập cần đọc. Vẫn đúng SKILL ("cắt ghi chú trước").

---

### Task 2.6 — Controller ghi + routes + verify vòng đời

**Files:**
- Modify: `Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php`
- Modify: `Modules/Finance/Routes/api.php`

- [x] **Bước 1: 5 action mới**

```php
    public function store(BillPaymentRequestStoreRequest $request)
    {
        $model = $this->service->store($request);

        return $this->responseJson(
            (int) $model->status === BillPaymentRequest::STATUS_AWAITING_MANAGE
                ? 'Gửi duyệt phiếu đề nghị thanh toán thành công!'
                : 'Lưu phiếu đề nghị thanh toán thành công!',
            200,
            ['id' => $model->id, 'code' => $model->code]
        );
    }

    public function update(BillPaymentRequestUpdateRequest $request, $id)
    {
        $model = $this->service->findOrFail((int) $id);
        if (!$model->canEdit()) {
            return $this->responseJson('Bạn không có quyền sửa phiếu này', 403);
        }
        ...
    }

    public function destroy($id) { /* canDelete() -> 403 */ }

    public function approve(BillPaymentRequestApproveRequest $request, $id)
    {
        $model = $this->service->findForShow((int) $id);
        if (!$model->canApproveAtCurrentStatus()) {
            return $this->responseJson('Bạn không có quyền duyệt phiếu này ở trạng thái hiện tại', 403);
        }
        $this->approvalService->approve($request, $model);

        return $this->responseJson('Duyệt phiếu đề nghị thanh toán thành công!');
    }

    public function changeStatus(BillPaymentRequestChangeStatusRequest $request, $id)
    {
        $model = $this->service->findOrFail((int) $id);
        if (!$model->canCancel()) {
            return $this->responseJson('Bạn không có quyền không duyệt phiếu này', 403);
        }
        $this->approvalService->reject($request, $model);

        return $this->responseJson('Không duyệt phiếu đề nghị thanh toán thành công!');
    }
```

- [x] **Bước 2: Routes**

```php
        Route::post('/', [BillPaymentRequestController::class, 'store']);
        Route::put('/{id}', [BillPaymentRequestController::class, 'update']);
        Route::delete('/{id}', [BillPaymentRequestController::class, 'destroy']);
        Route::post('/{id}/approve', [BillPaymentRequestController::class, 'approve']);
        Route::post('/{id}/change-status', [BillPaymentRequestController::class, 'changeStatus']);
```

- [x] **Bước 3: Verify — chạy trọn vòng đời bằng HTTP thật**

Kịch bản (dùng token của từng cấp; nếu DB chưa có người đủ 5 vai thì làm **Task 8.1 trước**):

1. `POST /` status 1 → 200, có `code` đúng format `*.DNTT{mmyy}.*`
2. `PUT /{id}` status 2 (gửi duyệt) → 200
3. `POST /{id}/approve` bằng token TP, `status = 3` → 200; kiểm `payment_money_manage` đã ghi và `manage_approved_id` = id TP
4. `POST /{id}/approve` bằng token KT công nợ, `status = 4` → 200
5. `POST /{id}/approve` bằng token KT trưởng, `status = 5` → 200 (chuyển BGĐ)
6. `POST /{id}/approve` bằng token BGĐ, `status = 6` → 200
7. `POST /{id}/change-status` ở bước 3 (phiếu đang status 2) → phiếu về **status 1**, không phải 10

- [x] **Bước 4: Verify — 8 ca xấu bắt buộc bị chặn**

| # | Ca | Kỳ vọng |
| --- | --- | --- |
| 1 | `POST /` với `type = 3` | 422 |
| 2 | `POST /` với `exchange_rate = 0` | 422 |
| 3 | `POST /` loại 1 không gửi `attachments` | 422 |
| 4 | `POST /` với `contractable_type` là class hợp đồng bán trong khi `type = 1` | 422 |
| 5 | `PUT /{id}` bằng token người khác | 403 |
| 6 | `DELETE /{id}` phiếu đang ở status 3 | 403 |
| 7 | `POST /{id}/approve` nhảy cóc `status = 6` khi phiếu đang status 2 | 422 |
| 8 | `POST /{id}/approve` với `money` **lớn hơn** số cấp trước duyệt | 200 nhưng DB ghi đúng **bằng trần** |

**Kết quả thật (2026-08-15)** — 9 route (4 đọc + 5 ghi), chạy HTTP thật với **6 tài khoản khác nhau**
(người lập 25 *không có quyền nào* · TP 24 · KT công nợ 147 · KT trưởng 196 · BGĐ 100 · người ngoài 36):

**Vòng đời đủ 5 cấp — 6/6 bước 200:**
`POST /` → `TPE.DNTT0826.00001` (đúng format `{cty}.DNTT{mmyy}.{5 số}`) → `PUT` gửi duyệt →
TP duyệt (3) → KT công nợ (4) → KT trưởng chuyển BGĐ (5) → BGĐ duyệt (6).
Đối chiếu DB sau vòng đời:
- `status = 6`, **4 cột người duyệt** ghi đúng `24 / 147 / 196 / 100`, `manage_approved_time` có giờ.
- **Trần cắt ở BE ăn thật**: TP gửi `money = 99.999.999` cho dòng 2 (đề nghị 500.000) → DB ghi
  đúng **500.000**. Dòng 1: 1.000.000 → TP 800.000 → KTCN 700.000 → KTT/BGĐ 650.000, mỗi cấp một cột riêng.
- `*_exchange` do BE tự nhân tỷ giá, không lấy số FE.
- `masterPayload()` **xoá trắng cột ngoài nhánh**: `bank_branch` / `bank_province_id` /
  `customer_id` / `to_date` đều NULL ở phiếu loại 1 CK nước ngoài.
- `created_by = 25`, `company_id = 1`, `department_id = 42` do hook `creating` gán — người lập
  **không cần quyền nào** vẫn tạo được phiếu (đúng ERP).

**Ca xấu — 10/10 bị chặn đúng:**

| Ca | Kết quả |
| --- | --- |
| `type = 3` | 422 (`type` + kéo theo `contractable_type` vì loại 3 không có danh sách morph) |
| `exchange_rate = 0` | 422 `exchange_rate` |
| loại 1 không gửi `attachments` | 422 `attachments` |
| loại 1 gửi morph **hợp đồng bán** | 422 `details.0.contractable_type` |
| `PUT` bằng token người khác | **403** |
| `DELETE` phiếu đang status 6 | **403** |
| approve nhảy cóc `status = 6` khi phiếu đang 2 | 422 *"Không thể chuyển phiếu sang trạng thái này"* |
| KT trưởng bấm duyệt khi phiếu đang chờ **TP** | **403** |
| Không duyệt mà thiếu ghi chú của đúng cấp | 422 `note` |
| approve `money` vượt trần | 200 nhưng DB = **đúng trần** |

**Không duyệt — giữ đúng bẫy ERP:**
- TP không duyệt → phiếu về **status 1 (Đang tạo)**, `note` + `reject_comment` ghi đủ.
- KT công nợ không duyệt → phiếu về **status 10 (Không duyệt)**, ghi `note_accountant_dept`.
- Xoá phiếu nháp của chính mình → 200, master + **dòng chi tiết đều sạch**.

🧹 **Đã dọn sạch dữ liệu test**: 5 phiếu `TPE.DNTT0826.*` do phiên verify tạo đã xoá cùng 10 dòng
chi tiết — bảng trở lại **đúng 4.040 phiếu** như trước khi test.

⚠️ Bẫy khi test bằng curl: thiếu header `Accept: application/json` thì lỗi validate trả **302
redirect** chứ không phải 422 (Laravel tưởng là request trình duyệt), và payload có dấu `\` phải
đưa qua **file** `-d @file.json` — nhét thẳng chuỗi trong bash bị nuốt.

- [x] **Bước 5: Ghi checkpoint.**

---

# Phase 3 — BE loại chi 12 (vận chuyển)

### Task 3.1 — 8 entity read-only cho chuyến xe & bảng giá cước

**Files:**
- Create: `Modules/Finance/Entities/Delivery/DeliveryTrip.php` · `OtherDeliveryTrip.php` · `DeliveryTripAccounting.php` · `OtherDeliveryTripAccounting.php`
- Create: `Modules/Finance/Entities/Delivery/PriceListValidDelivery.php` · `PriceListValidDeliveryVehicle.php` · `PriceListValidDeliveryVehiclePayload.php` · `PriceListValidDeliveryVehiclePayloadRoad.php`

**Interfaces:**
- Produces: 8 class read-only, mỗi class khai `$table` tường minh + quan hệ cần cho popup.

- [x] **Bước 1: Xác nhận tên bảng thật (KHÔNG đoán)**

```bash
php artisan tinker --execute="foreach (['delivery_trips','other_delivery_trips','delivery_trip_accounting','other_delivery_trip_accounting','price_list_valid_deliveries','price_list_valid_delivery_vehicles','price_list_valid_delivery_vehicle_payloads','price_list_valid_delivery_vehicle_payload_roads','roads','license_plates','works'] as \$t) { echo \$t.' => '.(Schema::hasTable(\$t) ? DB::table(\$t)->count() : 'KHONG CO').PHP_EOL; }"
```
⚠️ Model ERP `PriceListValidDelivery` khai `$table` riêng (bảng thật là **số nhiều** `price_list_valid_deliveries`) — copy đúng tên bảng in ra ở bước này, không copy tên class.

- [x] **Bước 2: Viết 8 entity**

Khuôn giống Task 1.1 (`$guarded = ['*']`), thêm quan hệ:
```php
// PriceListValidDelivery
public function vehicles()
{
    return $this->hasMany(PriceListValidDeliveryVehicle::class, 'price_list_valid_delivery_id');
}
// PriceListValidDeliveryVehicle
public function payloads()
{
    return $this->hasMany(PriceListValidDeliveryVehiclePayload::class, 'price_list_valid_delivery_vehicle_id');
}
// PriceListValidDeliveryVehiclePayload
public function roads()
{
    return $this->hasMany(PriceListValidDeliveryVehiclePayloadRoad::class, 'price_list_valid_delivery_vehicle_payload_id');
}
```
⚠️ Tên khoá ngoại phải **đối chiếu `information_schema`** trước khi viết:
```bash
php artisan tinker --execute="print_r(Schema::getColumnListing('price_list_valid_delivery_vehicle_payload_roads'));"
```

- [x] **Bước 3: Verify** `php -l` 8 file + `::count()` từng entity.

**Kết quả thật (2026-08-15):** `php -l` sạch 8 file; đếm thật + chạy thật quan hệ:

| Entity | Bảng | Dòng |
| --- | --- | --- |
| `DeliveryTrip` | `delivery_trips` | 2.728 |
| `OtherDeliveryTrip` | `other_delivery_trips` | 345 |
| `DeliveryTripAccounting` | `delivery_trip_accounting` *(số ít)* | 2.555 |
| `OtherDeliveryTripAccounting` | `other_delivery_trip_accounting` *(số ít)* | 329 |
| `PriceListValidDelivery` | `price_list_valid_deliveries` *(số nhiều)* | 6 |
| `PriceListValidDeliveryVehicle` | `price_list_valid_delivery_vehicles` | 14 |
| `PriceListValidDeliveryVehiclePayload` | `price_list_valid_delivery_vehicle_payloads` | 65 |
| `PriceListValidDeliveryVehiclePayloadRoad` | `price_list_valid_delivery_vehicle_payload_roads` | 86.462 |

Quan hệ chạy thật: `DeliveryTrip#1 → accountings` ra `TPE_HTCXCH_00081` ·
`DeliveryTripAccounting#1 → delivery_trip` ra `TPHP_CXCH_00012` ·
`PriceList#2 → 6 loại xe → payload → 1.824 tuyến đường`.

---

### Task 3.2 — `DeliveryTripPaymentService::accountingDetails()`

**Files:**
- Create: `Modules/Finance/Services/DeliveryTripPaymentService.php`

**Interfaces:**
- Produces:
  - `accountingDetails(int $supplierId, string $toDate): array` — danh sách dòng chi tiết loại 12
  - `paidMoneyForDetail(BillPaymentRequestDetail $d): float` — số đã trả, dùng lại ở `detailPaymentMoney()` (Task 1.5)

- [x] **Bước 1: Port query lấy dữ liệu** (spec 5.4) — giữ nguyên 6 điều kiện `WHERE` và 2 `COALESCE` cột code.

- [x] **Bước 2: Tính `money_payed`**

```php
    /**
     * Số tiền ĐÃ THANH TOÁN cho 1 phiếu hạch toán chuyến xe.
     *
     * ⚠️ ERP có 2 công thức KHÁC NHAU cho cùng khái niệm này, phải giữ đúng từng chỗ:
     *   - Lúc "Lấy dữ liệu" (`getDeliveryTripAccountingDetails()` :599): type IN (1,2),
     *     billable_type IN (DeliveryTripAccounting, OtherDeliveryTripAccounting)
     *   - Lúc mở lại phiếu (`DeliveryTripAccounting::getPaymentMoney()` :209): CHỈ type = 1,
     *     CHỈ billable_type = DeliveryTripAccounting
     * Bê nhầm là số "Đã thanh toán" của phiếu cũ lệch so với ERP.
     */
    public function paidMoneyForDetail(BillPaymentRequestDetail $detail): float
    { ... }
```

- [x] **Bước 3: Gỡ TODO ở `BillPaymentRequestService::detailPaymentMoney()`** (Task 1.5 Bước 3) — nhánh loại 12 gọi thật `paidMoneyForDetail()`.

- [x] **Bước 4: Verify — đối chiếu SQL thuần**

```bash
php artisan tinker --execute="\$s = app(Modules\Finance\Services\DeliveryTripPaymentService::class); \$rows = \$s->accountingDetails(<SUPPLIER_ID>, '2026-08-14'); echo count(\$rows).' dong | tong cuoc='.array_sum(array_column(\$rows,'total_cost_transition'));"
```
So với SQL thuần dựng đúng query ở spec 5.4. Kỳ vọng: **số dòng và tổng cước khớp tuyệt đối**.

Chọn `<SUPPLIER_ID>` từ phiếu loại 12 có thật:
```sql
SELECT supplier_id, COUNT(*) FROM bill_payment_requests WHERE type = 12 GROUP BY supplier_id ORDER BY 2 DESC LIMIT 3;
```

**Kết quả thật (2026-08-15)** — đối chiếu với SQL thuần dựng đúng query spec 5.4, **4/4 NCC khớp
tuyệt đối cả số dòng lẫn tổng cước**:

| NCC | Service | SQL thuần | Dòng thô (trước khi lọc `payment_money > 0`) |
| --- | --- | --- | --- |
| 14059 | 14 dòng / 27.942.112 | 14 / 27.942.112 ✅ | 88 |
| 7040 | 25 dòng / 45.218.199 | 25 / 45.218.199 ✅ | 470 |
| 11735 | 0 dòng | 0 ✅ | 29 |
| 620 | 2.764 dòng / 1.590.418.069 | 2.764 / 1.590.418.069 ✅ | 2.764 |

Ca biên: NCC không tồn tại / `supplier_id = 0` / `to_date = 2000-01-01` → **0 dòng**, không lỗi.
`paidMoneyForDetail()` trên dòng thật (`detail#2114`, hạch toán 21) = **366.000** = SQL ✅.

🐛 **Plan/spec ghi SAI namespace morph, đã sửa khi làm**: chuỗi trong `account_details` là
`App\Model\**Warehouse**\DeliveryTripAccounting` (13.792 dòng) và
`App\Model\**Warehouse**\OtherDeliveryTripAccounting` (1.523 dòng) — spec ghi tắt "Delivery",
viết theo spec thì query ra **0 dòng**. `account_id = 99` của ERP đúng là TK **3311** trên DB này,
nhưng code tra theo `identify_number` thay vì chốt cứng id.

---

### Task 3.3 — `DeliveryTripPaymentService::tripDetail()` — popup 13 cột

**Files:**
- Modify: `Modules/Finance/Services/DeliveryTripPaymentService.php`

**Interfaces:**
- Produces: `tripDetail(?int $deliveryTripId, ?int $otherDeliveryTripId): array` với đúng 13 khoá:
  `delivery_trip_code · accounting_code · vehicle_name · total_km_actual · km_additional · delivery_recipe · price_additional · total_cost_transition · delivery_tax · total_cost_transition_after_vat · road_name · license_plate · employees`

- [x] **Bước 1: Tính `delivery_recipe` theo bảng giá cước**

```php
    /**
     * Cước chính = giá tuyến đường trong bảng giá HIỆU LỰC của công ty người đăng nhập,
     * nhân 2 nếu chuyến 2 chiều (port ERP `getDeliveryTripDetail()` :704-726).
     *
     * Bảng giá chọn theo: company_id + hôm nay nằm trong [date_valid_from, date_valid_to];
     * không có bản hiệu lực thì lấy bản MỚI NHẤT của công ty (fallback của ERP).
     * Chuỗi quan hệ: price list -> vehicle(vehicle_category_id) -> payload(vehicle_payload_id)
     *             -> road(road_id) -> cost
     */
```
⚠️ ERP **không null-check** 3 mắt xích này (`->first()->payloads()` …) → chuyến xe có loại xe/tuyến chưa khai giá là **nổ 500**. HRM phải null-safe, thiếu mắt nào thì `delivery_recipe = 0` và ghi log cảnh báo.

- [x] **Bước 2: Ghép cột "Nhân viên kinh doanh"**

Port `getDeliveryTripDetail()` :646-702: duyệt phiếu xuất kho / nhập kho gắn chuyến xe, ghép
`{mã NV} - {tên NV} - {mã phiếu} - {mã KH} - {tên KH}`, nối bằng `', '`. Nhánh `other_delivery_trip` duyệt `activities` thay vì `warehouse_exports/imports`.
Mọi mắt xích đều null-safe (ERP dùng `??` rời rạc, dễ nổ khi thiếu `customer`).

- [x] **Bước 3: Verify**

```bash
php artisan tinker --execute="\$s = app(Modules\Finance\Services\DeliveryTripPaymentService::class); print_r(\$s->tripDetail(<DELIVERY_TRIP_ID>, null));"
```
Kỳ vọng: đủ **13 khoá**, không khoá nào thiếu; `total_cost_transition_after_vat` = `total_cost_transition + delivery_tax`.

Chạy thêm với 1 `other_delivery_trip_id` và với 1 chuyến xe **chưa khai giá cước** → kỳ vọng: không exception, `delivery_recipe = 0`.

**Kết quả thật (2026-08-15)** — chuyến xe #1 trả **đủ 13 khoá**:
```
delivery_trip_code   TPE_CXCH_00001      accounting_code  TPE_HTCXCH_00081
vehicle_name         Xe tải có mui - 2.5 tấn                total_km_actual  24
delivery_recipe      1.539.648            total_cost_transition 712.800  delivery_tax 0
total_cost_transition_after_vat 712.800   (= cước + thuế ✅)
road_name            Liên Ninh, Hà Nội - Long Biên, Hà Nội
license_plate        15C-13876 - Trần Văn Chung
employees            12010262 - Vương Văn Duy - PXK-00023 - 29TPHPVI-140 - CÔNG TY … LOTUS VIỆT NAM
```
Chuyến xe KHÁC (#10) cũng đủ 13 khoá (`TPE_CXK_00010` / `TPE_HTCXK_00001`, cước 475.200).
Chuyến không tồn tại và chuyến **không có tuyến đường** → 13 khoá, `delivery_recipe = 0`,
**không exception** (ERP nổ 500 ở đúng 2 ca này). Mẫu 30 chuyến có đủ loại xe/tải trọng/tuyến:
**22/30 tính ra cước > 0**, 8 chuyến còn lại bảng giá chưa khai → 0 + ghi log cảnh báo.

🐛 **Plan ghi SAI cách nối phiếu kho với chuyến xe, đã sửa khi làm**: `warehouse_exports` /
`warehouse_imports` **KHÔNG có cột `delivery_trip_id`** (và **không có bảng `activities`**).
Thực tế nối qua pivot **`activity_has_delivery_trips`** (4.561 dòng) và
**`activity_has_other_delivery_trips`** (569 dòng).
⚠️ Nhân viên lấy từ `employee_created_request_id` → tra qua **`employees`** rồi mới sang
`employee_infos`: trên DB gộp cùng một con số vừa là id `employees` vừa là id `employee_infos`
của NGƯỜI KHÁC (đo thật: id 116 → "Vương Văn Duy" qua `employees` nhưng "Nguyễn Hà Chi" nếu tra
thẳng `employee_infos`).

---

### Task 3.4 — 2 endpoint loại 12

**Files:**
- Modify: `Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php`
- Modify: `Modules/Finance/Routes/api.php`

- [x] **Bước 1: 2 action**

```php
    /** Loại chi 12 — nút "Lấy dữ liệu": sinh dòng chi tiết theo NCC + mốc Đến ngày. */
    public function deliveryTripAccountingDetails(Request $request)
    {
        if (!$request->filled('supplier_id')) {
            return $this->responseJson('Vui lòng chọn nhà cung cấp trước', 422);
        }
        if (!$request->filled('to_date')) {
            return $this->responseJson('Vui lòng chọn Đến ngày trước', 422);
        }

        return response()->json([
            'data' => $this->deliveryService->accountingDetails(
                (int) $request->get('supplier_id'),
                $request->get('to_date')
            ),
        ]);
    }

    /** Loại chi 12 — popup chi tiết chuyến xe (13 cột). */
    public function deliveryTripDetail(Request $request)
    {
        return response()->json([
            'data' => $this->deliveryService->tripDetail(
                $request->get('delivery_trip_id'),
                $request->get('other_delivery_trip_id')
            ),
        ]);
    }
```

- [x] **Bước 2: Routes — đặt TRƯỚC `/{id}`**

```php
        Route::get('/delivery-trip-accounting-details', [BillPaymentRequestController::class, 'deliveryTripAccountingDetails']);
        Route::get('/delivery-trip-detail', [BillPaymentRequestController::class, 'deliveryTripDetail']);
```

- [x] **Bước 3: Verify**

```bash
php artisan route:list --path=bill-payment-requests
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/delivery-trip-accounting-details?supplier_id=<ID>&to_date=2026-08-14" | head -c 800
```
Kỳ vọng: JSON có dòng, **không** bị route `/{id}` nuốt (nếu trả 404/lỗi ép kiểu id → route đặt sai thứ tự).

**Kết quả thật (2026-08-15):** tổng **11 route**, 2 route mới nằm **trước** `/{id}` nên không bị nuốt.
- `GET /delivery-trip-accounting-details?supplier_id=14059&to_date=2026-08-15` → **14 dòng**, mỗi
  dòng đủ 13 khoá FE cần (`delivery_trip_id/code`, `..._accounting_id/code`, `total_cost_transition`,
  `money_payed`, `payment_money`, `payment_money_request` điền sẵn, `need_payment = 1`).
- `GET /delivery-trip-detail?delivery_trip_id=1` → **13 khoá** đúng như Task 3.3.
- Thiếu `supplier_id` / thiếu `to_date` / popup thiếu cả 2 id → **422** kèm câu tiếng Việt
  (BE chặn, không chỉ dựa FE như ERP).

---

# Phase 4 — BE file đính kèm + in + xuất Excel

### Task 4.1 — File đính kèm

**Files:**
- Create: `Modules/Finance/Services/BillPaymentAttachmentService.php`
- Modify: Controller + routes

**Interfaces:**
- Produces: `upload(UploadedFile[] $files): array` (mảng URL) · `sync(BillPaymentRequest $m, array $urls): void` · `remove(BillPaymentRequest $m, string $url): bool` · `static parse(?string $attachments): array`

- [x] **Bước 1: Service**

```php
    /** Ngăn cách giữa các URL trong cột `attachments` — PHẢI đúng ', ' để cổng ERP tách được. */
    const SEPARATOR = ', ';

    public function upload(array $files): array
    {
        return (new \App\Helper\CmcS3Helper())->putFiles($files, 'bill_payment_requests');
    }

    /** Ghi đè chuỗi `attachments` bằng danh sách URL hiện tại của phiếu. */
    public function sync(BillPaymentRequest $model, array $urls): void
    {
        $model->attachments = implode(self::SEPARATOR, array_values(array_filter($urls)));
        $model->save();
    }

    /**
     * Gỡ 1 file khỏi phiếu.
     *
     * ⚠️ KHÔNG xóa vật lý trên S3 (ERP `deleteFile()` gọi `unlink(public_path().$file)` — code chết
     * vì file nằm trên S3). Chỉ gỡ khỏi chuỗi: phiếu bên ERP có thể còn tham chiếu cùng URL.
     */
    public function remove(BillPaymentRequest $model, string $url): bool { ... }

    public static function parse(?string $attachments): array
    {
        return array_values(array_filter(array_map('trim', explode(',', (string) $attachments))));
    }
```
⚠️ `parse()` tách bằng `,` rồi `trim` (không tách bằng `', '`) để chịu được dữ liệu ERP cũ ghi thiếu khoảng trắng.

- [x] **Bước 2: FormRequest upload**

```php
            'files' => 'required|array|min:1',
            'files.*' => 'required|file|mimes:pdf,png,jpg,jpeg,docx,doc,xls,xlsx,zip|max:20000',
```

- [x] **Bước 3: 2 route**

```php
        Route::post('/{id}/attachments', [BillPaymentRequestController::class, 'uploadAttachments']);
        Route::delete('/{id}/attachments', [BillPaymentRequestController::class, 'removeAttachment']);
```
Cả 2 gate bằng `canEdit()` → 403.

- [x] **Bước 4: Verify**

```bash
php -l Modules/Finance/Services/BillPaymentAttachmentService.php
php artisan tinker --execute="print_r(Modules\Finance\Services\BillPaymentAttachmentService::parse(Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest::whereNotNull('attachments')->where('attachments','<>','')->value('attachments')));"
```
Kỳ vọng: mảng URL sạch, không phần tử rỗng.

Upload thật 1 file nhỏ qua `curl -F` → kiểm cột `attachments` có thêm URL và **giữ nguyên** URL cũ.

🔁 **Làm lại theo khuôn HRM (user chốt 2026-08-15: "phần file xem bên HRM đang xử lý như nào thì
làm như vậy")** — bỏ thiết kế upload-trước-lấy-URL, bám đúng `ProductTransferRequest` đang chạy:

| | Bản đầu (đã bỏ) | Bản theo HRM (đang dùng) |
| --- | --- | --- |
| Upload | endpoint riêng `POST /{id}/attachments`, FE gửi URL khi lưu | **gửi kèm ngay trong `store`/`update`** bằng `multipart/form-data`, `attachments[]` là FILE |
| Sửa có file | — | FE gửi `POST` + `_method=PUT` (PHP không parse multipart cho PUT thật) |
| Gỡ file | `DELETE /{id}/attachments`, body `url`, **không** xoá S3 | **`DELETE /{id}/files`**, body `file_url`, **xoá object S3 thật** qua `CmcS3Helper::deleteFile()` |
| Lưu không kèm file | ghi đè theo mảng FE gửi | **giữ nguyên** danh sách cũ, file mới chỉ APPEND |

Đã xoá `BillPaymentRequestUploadRequest` (HRM không có FormRequest riêng cho upload); rule file
chuyển vào `BillPaymentRequestStoreRequest`:
`attachments` = `required|array|min:1` khi loại chi 1 & phiếu chưa có file, còn lại `nullable|array`;
`attachments.*` = `file|mimes:pdf,png,jpg,jpeg,docx,doc,xls,xlsx,zip|max:20000`.

📌 Lý do "không xoá S3" của bản đầu **không còn đúng**: mỗi file có tên ngẫu nhiên riêng do
`putFiles()` sinh nên URL chỉ thuộc đúng 1 phiếu, mà 2 cổng lại đọc **cùng một dòng** dữ liệu →
xoá thật không ảnh hưởng phiếu nào khác. Bỏ được luôn khoản lệch so với HRM.

**Kết quả thật (2026-08-15):** `parse()` chạy trên **toàn bộ 3.432 phiếu có file** (**11.587 file**,
phiếu nhiều nhất 45 file) → **0 phiếu parse ra rỗng**; chịu được mọi dạng bẩn (`'a,b'` · `'a, b'` ·
`'a, '` · `' , a , , b , '`).

**Chạy vòng đời file THẬT qua HTTP (có upload lên S3):**

| Ca | Kết quả |
| --- | --- |
| Tạo phiếu loại 1 **không** kèm file | **422** `attachments` |
| Kèm file `.exe` | **422** *"Chỉ nhận file pdf, png, jpg, …"* |
| Tạo phiếu kèm 1 PDF | 200, `attachments` có **1 URL S3**, file tải được (**HTTP 200**) |
| Sửa (`_method=PUT`) kèm PDF thứ 2 | 200, danh sách thành **2 URL** — file cũ **không mất** |
| Sửa **không** kèm file | 200, danh sách **giữ nguyên 2 URL** |
| `DELETE /{id}/files` thiếu `file_url` | **422** |
| `file_url` không thuộc phiếu | **404** |
| Người khác gỡ file | **403** |
| Gỡ đúng file | 200, còn 1 URL; **object trên S3 đã biến mất** (200 → 403), file còn lại vẫn tải được |

🧹 Đã dọn sạch: gỡ nốt file thứ 2 khỏi S3 + xoá phiếu test → bảng về đúng **4.040 phiếu**,
**không để lại file rác nào trên bucket**.

---

### Task 4.2 — Dữ liệu màn in

**Files:**
- Create: `Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestPrintResource.php`
- Modify: Controller + routes (`GET /{id}/print-data`)

**Interfaces:**
- Produces: JSON gồm `template` (`ncc_tm` | `ncc_ck` | `chung`), khối header (đơn vị, mã phiếu, ngày, người lập, phòng ban, loại chi, hình thức TT, lý do, tỷ giá), khối ngân hàng, mảng `details` **đã tính sẵn** 6 cột tiền + cờ hiện/ẩn từng cột duyệt, khối chữ ký 5 ô.

- [x] **Bước 1: Chọn mẫu**

```php
        // Port ERP `print()` :483-489 (template 405 / 406 / 210).
        if ($model->type == 1 && $model->has_contract == 1) {
            $template = $model->type_payment == 1 ? 'ncc_tm' : 'ncc_ck';
        } else {
            $template = 'chung';
        }
```

- [x] **Bước 2: Cờ hiện cột duyệt** (port ERP `billPaymentRequestTable()` :1031-1033)

```php
        $status = (int) $model->status;
        $notDead = !in_array($status, [1, 9, 10], true);
        'show_manage' => $notDead && in_array($status, [3, 4, 5, 6, 7, 8], true),
        'show_accountant_debt' => $notDead && in_array($status, [4, 5, 6, 7, 8], true),
        'show_chief_accountant' => $notDead && in_array($status, [6, 7, 8], true),
```
Cột nào `false` thì FE in `_` (đúng ERP).

- [x] **Bước 3: Khối chữ ký** — chỉ trả tên khi phiếu đã qua cấp đó (cùng bộ cờ trên), kèm chữ "Đã duyệt"; người lập luôn có "Đã ký".

- [x] **Bước 4: Verify**

```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/<ID>/print-data" | head -c 1200
```
Kiểm 3 phiếu: 1 phiếu loại 1 TM (`ncc_tm`), 1 phiếu loại 1 CK (`ncc_ck`), 1 phiếu loại 6 (`chung`); 1 phiếu status 8 phải hiện đủ 3 cột duyệt, 1 phiếu status 2 phải ẩn cả 3.

**Kết quả thật (2026-08-15)** — gọi HTTP `GET /{id}/print-data` trên **5 phiếu**:

| Phiếu | Loại | Template | Cờ cột duyệt |
| --- | --- | --- | --- |
| #38 | 1 / TM | **`ncc_tm`** ✅ | đủ 3 |
| #1 | 1 / CK (RUPEE) | **`ncc_ck`** ✅ | đủ 3 |
| #28 | 6 | **`chung`** ✅ | đủ 3 |
| #121 | 12 (37 dòng) | **`chung`** ✅ | đủ 3 |
| #4161 | status 2 | `ncc_ck` | **ẩn cả 3** ✅ |

Chữ ký: phiếu status 8 điền đủ tên 4 cấp đã duyệt + "Đã duyệt"; phiếu status 2 chỉ có người lập
("Đã ký"), 4 ô còn lại **rỗng**. Khối `bank` trả đủ 15 khoá (gồm bộ `mid_*`), `company_name` lấy
được từ bảng `companies`.

📌 Bổ sung so với plan: thêm `header.debt_label` (nhãn cột công nợ đổi theo loại chi — port
`$billTypes` :990 của ERP) và `details[].payment_money` / `money_payed` để **bản in và file Excel
dùng chung một nguồn số**.

---

### Task 4.3 — Xuất Excel

**Files:**
- Create: `Modules/Finance/Exports/BillPaymentRequestExport.php`
- Modify: Controller + routes (`GET /{id}/export`)

- [x] **Bước 1:** Đọc `app/ExcelExports/BillPaymentRequestExcel.php` bên ERP để lấy đúng bố cục cột.
- [x] **Bước 2:** Viết export bằng `maatwebsite/excel` (đã có trong stack), dùng lại dữ liệu của `BillPaymentRequestPrintResource` để 2 đầu ra không lệch nhau.
- [x] **Bước 3: Verify** — tải file thật, mở kiểm số dòng chi tiết + tổng tiền khớp màn chi tiết:
```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/bill-payment-requests/<ID>/export" -o /tmp/dntt.xlsx && ls -l /tmp/dntt.xlsx
```

**Kết quả thật (2026-08-15)** — đã đọc được bố cục ERP từ repo `D:/laragon/www/erp`
(`app/ExcelExports/BillPaymentRequestExcel.php` + blade `billpayment_request_export` +
`BillPaymentRequest::billPaymentRequestTable()` :986) nên bám đúng **cột động** của ERP.

Tải thật 3 file (HTTP 200, 80–83 KB) rồi **mở lại bằng PhpSpreadsheet** để đối chiếu:

| Phiếu | Cột động sinh ra | Dòng | Tổng đề nghị (Excel = DB) |
| --- | --- | --- | --- |
| #1 loại 1 CK, **ngoại tệ RUPEE** | Số hợp đồng · Số tiền còn nợ · Đề nghị chi · **Quy đổi VND** · 3 cột duyệt · Số tiền duyệt · Ghi chú | 1 | 86.730 ✅ |
| #38 loại 1 **TM** | **Nhà cung cấp** · Số hợp đồng · … (không có cột quy đổi vì VNĐ) | 4 | 28.376.000 ✅ |
| #121 **loại 12** | **Số chuyến xe · Hạch toán** · Số tiền còn lại · … | 37 | 62.425.296 ✅ |

Khối chữ ký in **ngược thứ tự** như ERP (BGĐ → … → Người đề nghị), có dòng "(Ký, họ tên)", tên và
"Đã duyệt"/"Đã ký". Cột "Số tiền duyệt" luôn `_` — đúng ERP khi chưa có phiếu chi (màn Phiếu chi
ngoài phạm vi đợt này). Nhãn cột công nợ đổi đúng theo loại chi
(`Số tiền còn nợ` / `Công nợ còn lại` / `Số tiền còn lại`).

---

# Phase 5 — FE danh sách + menu

### Task 5.1 — `index.vue` 4 chế độ

**Files:**
- Create: `pages/finance/bill-payment-requests/index.vue`

**Interfaces:**
- Consumes: `GET /finance/bill-payment-requests?mode=…`, `/pending`, `/approved`
- Produces: prop nội bộ `mode` lấy từ `$route.query.mode`; các cờ quyền chỉ đọc từ `meta` BE trả về.

- [x] **Bước 1: Đọc 2 màn mẫu**

`pages/assign/customers/index.vue` (base chuẩn) và `pages/finance/bill-income-requests/index.vue` (743 dòng — cách 1 file phục vụ 2 chế độ qua prop `pendingMode`). Màn này mở rộng thành **4 chế độ**.

- [x] **Bước 2: Khai báo chế độ**

```js
const MODES = {
    mine: { label: 'Của tôi', endpoint: '' },
    all: { label: 'Tất cả', endpoint: '' },
    pending: { label: 'Chờ duyệt', endpoint: '/pending' },
    approved: { label: 'Đã duyệt', endpoint: '/approved' },
}
```
`mine` và `all` dùng chung endpoint gốc, khác nhau ở query `mode`.

- [x] **Bước 3: Cột lưới** (đúng thứ tự ERP)

STT · Mã phiếu (link chi tiết) · Loại chi · Hình thức thanh toán · Khách hàng · Số tiền · Ngày lập · Ngày nhận · Người lập · Phòng ban · Trạng thái · **Hành động** (chốt cuối, dùng `V2BaseRowActions`).

- [x] **Bước 4: Bộ lọc** — Mã phiếu · Lý do chi · Số tiền từ/đến · Loại chi · Hình thức TT · Người lập · Trạng thái · Khách hàng · Nhà cung cấp · khoảng ngày.

- [x] **Bước 5: Cờ quyền fail-closed**

```js
data() {
    return {
        // Fail-closed: mọi cờ quyền khởi tạo false, chỉ set từ meta BE trả về.
        canViewAllCompany: false,
        canApproveManage: false,
        canApproveAccountingDept: false,
        canApproveChiefAccountant: false,
        canApproveBoardOfManager: false,
        isAccountant: false,
    }
},
```

- [x] **Bước 6: Verify**

```bash
npx vue-template-compiler-cli 2>/dev/null || node -e "
const compiler = require('vue-template-compiler');
const fs = require('fs');
const src = fs.readFileSync('pages/finance/bill-payment-requests/index.vue','utf8');
const tpl = src.split('<template>')[1].split('</template>')[0];
const r = compiler.compile(tpl);
console.log('errors:', r.errors.length ? r.errors : 'none');
"
```
Kỳ vọng: `errors: none`. Thêm: grep chặn fail-open
```bash
grep -nE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payment-requests/index.vue
```
Kỳ vọng: **không có kết quả**.

**Kết quả thật (2026-08-15):** `pages/finance/bill-payment-requests/index.vue` — **template errors:
none**, script parse OK, `grep` fail-open **không có kết quả**. Chạy cùng bộ kiểm với màn Đề nghị
thu tiền (đã nghiệm thu) để chắc chắn khuôn kiểm đúng: cả 2 file đều sạch.

⚠️ **Lệnh verify trong plan sai, đã sửa khi chạy**: `src.split('<template>')[1]` cắt nhầm ở
`<template #cell-...>` bên trong bảng → báo *"tag has no matching end tag"* giả. Phải lấy từ
`<template>` đầu file tới `</template>` **cuối cùng trước `<script>`**
(`src.lastIndexOf('</template>', scriptAt)`).

**3 điểm khác/bổ sung so với plan:**
1. ~~Thêm thanh 4 chế độ~~ — **ĐÃ GỠ BỎ (user chốt 2026-08-15: "làm như ERP")**.
   Ban đầu em tự dựng thanh 4 tab vì plan khai `MODES` có `label` mà menu chỉ 2 lối vào.
   Đối chiếu lại ERP: ERP có đủ 3 route (`/?_type=`, `/for-approved`, `/approved`) nhưng
   **menu chỉ 2 mục** và **không có thanh tab nào** — 2 chế độ `mine`/`approved` chỉ vào được
   bằng URL. HRM nay giữ đúng vậy: lối vào là MENU, `?mode=` vẫn chạy đủ 4 chế độ.
   📌 Bài học: thứ plan không yêu cầu mà ERP cũng không có thì **hỏi trước khi thêm**, đừng tự suy.
2. **`localStorageKey` KHÔNG được khai bằng computed** — `filterStateMixin` đã khai chính key này
   trong `data()`, trùng tên thì Vue **giữ data và bỏ qua computed** ⇒ key rỗng, bộ lọc 4 chế độ
   ghi đè nhau. Đã chuyển sang gán trong `restoreSavedFilters()` theo `mode`.
3. **Bỏ code chết chép từ màn cũ**: màn Đề nghị thu tiền đọc `savedState.supplierOption` nhưng
   `filterStateMixin` chỉ lưu `filter` + `filterCollapsed` — nhánh đó không bao giờ chạy.

📐 **Chỉnh độ rộng cột (user yêu cầu 2026-08-15)**: khai `minWidth` cho 3 cột chữ dài —
**Khách hàng 240px · Lý do chi 200px · Phòng ban 190px**. Trước đó cả 3 không khai width nên
auto-layout bóp tên KH xuống 4–5 dòng (hàng cao ~130px). ⚠️ Nới 2 cột đầu thì cột **Lý do chi bị
ép còn 64px** — phải khai cho CẢ 3, không thì cột không khai bị "ăn" hết chỗ. Đo lại sau khi sửa:
hàng cao **46px**, tên KH còn 2 dòng.

**Chốt khác đáng nhớ:**
- Chỉ bật `sortable` cho cột nằm trong whitelist sort của BE (`code` · `createdAt` · `status` ·
  `type` · `typePayment`). Cột **Số tiền KHÔNG cho sort** dù skill khuyến nghị — BE tính tổng từ
  bảng chi tiết, chưa có nhánh sort; bật ra thì bấm không đổi (đúng cảnh báo của skill).
- Dropdown **Khách hàng** dùng `assign/customers/search` (luồng KH duy nhất sau `customer-cut-mysql2`),
  **Nhà cung cấp** dùng lại `finance/bill-income-requests/search-suppliers` — không dựng endpoint
  trùng chức năng.
- Xuất Excel dùng helper chung `utils/download-excel.js` (tự gắn `Authorization`), khuôn màn
  Danh mục tài khoản.

---

### Task 5.2 — Menu

**Files:**
- Modify: `components/subsystem-menu/finance.js`

- [x] **Bước 1:** Đọc 3 vị trí đang khai *Đề nghị thu tiền* (`grep -n "bill-income-requests" components/subsystem-menu/finance.js`).
- [x] **Bước 2:** Thêm ngay sau mỗi vị trí:
```js
{ label: 'Đề nghị thanh toán', link: '/finance/bill-payment-requests' },
```
và mục chờ duyệt: `link: '/finance/bill-payment-requests?mode=pending'`.
- [x] **Bước 3: Verify** — nạp thật file menu bằng mini-loader Node (khuôn đã dùng ở `chuyen-menu-nhom-nganh`), kiểm không khai trùng link và mục mới xuất hiện đúng nhóm.

**Kết quả thật (2026-08-15):** nạp thật `components/subsystem-menu/finance.js` (27 nhóm) →
**đúng 3 mục** trỏ về màn mới, cấu trúc y hệt Đề nghị thu tiền:

| Nhóm | Nhãn | Link |
| --- | --- | --- |
| Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi | Đề nghị thanh toán | `/finance/bill-payment-requests` |
| Đề nghị | Đề nghị thanh toán | `/finance/bill-payment-requests` |
| Phê duyệt - Công nợ - Thu - Chi | Phiếu đề nghị thanh toán chờ duyệt | `/finance/bill-payment-requests?mode=pending` |

Không còn mục "Đề nghị thanh toán" nào thiếu link. Link trùng đúng 2 lần ở mục danh sách —
**chủ ý**, y như Đề nghị thu tiền (ERP cũng có 2 lối vào).

📌 **Khác màn Đề nghị thu tiền 1 điểm**: mục chờ duyệt **KHÔNG gate `isShow`** bằng 1 quyền.
Phiếu này có **5 vai duyệt** khác nhau (TP · KT công nợ · KT trưởng · BGĐ · kế toán thanh toán);
gate bằng `Kế toán thanh toán` như màn kia thì 4 vai còn lại không nhìn thấy mục menu của chính
mình. BE đã tự lọc theo vai (không giữ vai nào → danh sách rỗng).

---

# Phase 6 — FE form tạo/sửa

### Task 6.1 — Khung form + Thông tin chung

**Files:**
- Create: `pages/finance/bill-payment-requests/components/BillPaymentRequestForm.vue`
- Create: `pages/finance/bill-payment-requests/create.vue`
- Create: `pages/finance/bill-payment-requests/_id/edit.vue`

**Interfaces:**
- Props: `mode: 'create' | 'edit'`, `requestId: String`, `readonly: Boolean`
- Emit: `loaded(data)`

- [x] **Bước 1: Đọc khuôn** — `pages/assign/customers/…/CustomerForm.vue` (khuôn `.card` chuẩn) + `BillIncomeRequestForm.vue` (1.021 dòng, cách tổ chức state cho phiếu 2 cấp).
- [x] **Bước 2: 2 trang vỏ** — copy đúng khuôn `create.vue` / `_id/edit.vue` của bill-income-requests (dùng `unsavedChildFormMixin`).
- [x] **Bước 3: Khối Thông tin chung** — bố cục 2 cột `col-md-6`, Loại tiền + Tỷ giá chung 1 cột, tỷ giá có addon `VND` và **khóa khi VND**; ô "Đến ngày" chỉ hiện khi loại 12.
- [x] **Bước 4: `changeForm()`** — đổi Loại chi / Hình thức TT thì **reset bảng chi tiết + xóa trắng 26 trường đối tượng/ngân hàng** (port `clearInfoBank()`).
- [x] **Bước 5: Verify** — compile template + `grep` fail-open như Task 5.1.
- [x] **Bước 7 — Ô "Tỷ giá" khoá phải nhìn giống các ô khoá khác (user báo 2026-08-15).**
  Đo trên trình duyệt: `V2BaseCurrencyInput[disabled]` để **nền trắng** (`#fff`, chữ `#0f172a`, viền
  `#d1d5db`) trong khi `V2BaseInput[disabled]` là **`#f1f5f9` / `#475569` / `#e2e8f0`** ⇒ ô Tỷ giá trông
  như vẫn nhập được. `V2BaseCurrencyInput` là component DÙNG CHUNG nên **không sửa file gốc**, chỉ đè
  trong scoped style của form: `::v-deep .v2-currency-input:disabled { … border-color: … !important }`
  (`!important` bắt buộc vì bản gốc khai `border: … !important`). Đo lại: 3 giá trị trùng khít ô khác.

- [x] **Bước 6 — 2 sai lệch so với ERP, user chỉ ra 2026-08-15 (đối chiếu `form.blade.php` của ERP).**

| Sai lệch | ERP | Đã sửa |
| --- | --- | --- |
| **Người tạo / Phòng ban** | `form.blade.php` :117-125 — hiện ở **cả màn tạo**, ô read-only | Bỏ `v-if="isEdit"`; màn tạo điền sẵn từ **`meta.creator`** của API danh sách (xem bẫy bên dưới) |
| **Ô "Ghi chú" cấp phiếu** | **KHÔNG có** — ERP chỉ có cột Ghi chú trong BẢNG CHI TIẾT (:501, `detail.note`) | Bỏ card "Ghi chú", đổi thành card **"Lịch sử duyệt"** chỉ hiện ở màn xem (giữ vết duyệt 4 cấp + Lý do không duyệt vốn nằm nhờ trong card đó) |

⚠️ **Vẫn nạp và gửi lại cột `note` của phiếu** dù không còn ô nhập: bỏ hẳn khỏi payload thì sửa 1 phiếu
cũ do bên ERP tạo sẽ **xoá trắng ghi chú** của họ (BE `masterPayload()` ghi đè cả 26 trường).

🐛 **Bẫy đã trả giá — ô Phòng ban TRỐNG khi tra bằng store FE.** Bản đầu lấy tên phòng ban bằng cách tra
`$store.state.departments` theo `current_employee_info.department_id`. Danh sách đó do
`AuthNewController::userProfile()` trả và **chỉ lấy `status = 1` (68/87 phòng ban)** ⇒ **70 nhân sự** đang
thuộc phòng ban đã ngừng hoạt động sẽ thấy ô trống, trong khi ERP vẫn hiện (ERP đi thẳng quan hệ
`employee_create->info->department`, không lọc status).

→ Chuyển sang **BE trả sẵn**: `BillPaymentRequestService::meta()` thêm khối
`creator: {name, department_name}` lấy từ `optional(auth()->user())->info->department` — cùng nguồn với
ERP và với hook `creating` của Entity (chỗ thật sự ghi `department_id`), nên hiển thị không lệch giá trị
sẽ lưu. Không tốn request mới: màn form vốn đã gọi `GET /bill-payment-requests?per_page=1` để lấy dropdown.
Verify: nhân sự id 274 (phòng ban `status = 0`) vẫn ra `Thiết bị ô tô 5`.

---

### Task 6.2 — `BankInfoSection.vue`

**Files:**
- Create: `pages/finance/bill-payment-requests/components/BankInfoSection.vue`

- [x] **Bước 1:** 2 nhánh loại trừ nhau (spec 4.5): NCC nước ngoài (2 select ngân hàng + 2 khối 6 dòng read-only) và trong nước (1 khối 5 dòng read-only).
- [x] **Bước 2:** Select **bắt buộc** `V2BaseSelectInModal` nếu nằm trong modal; ở form trang dùng `V2BaseSelect`.
- [x] **Bước 3:** Chọn ngân hàng → tự điền 6 trường (port `changeBank()` / `changeMidBank()`).
- [x] **Bước 4: Verify** compile template.

---

### Task 6.5 — 🐛 Menu không xoá được `?mode=pending` (user báo 2026-08-15)

**Triệu chứng:** đang ở `/finance/bill-payment-requests?mode=pending`, bấm menu "Đề nghị thanh toán" thì
URL vẫn giữ `?mode=pending`. Chiều ngược lại cũng hỏng: đang ở danh sách thường bấm "…chờ duyệt" cũng
không đổi URL.

**Nguyên nhân:** `components/sale/SaleHubSidebar.vue::openScreen()` chặn push bằng
`if (this.$route.path !== screen.link)` — so **`path`** nên 2 mục menu chỉ khác nhau ở QUERY luôn bị coi
là "đang đứng sẵn ở đó" ⇒ không điều hướng. Lỗi này dính MỌI phân hệ, không riêng màn này.

**Sửa:** `$route.path` → **`$route.fullPath`** (1 dòng). Vẫn giữ mục đích cũ là chặn push trùng
(`NavigationDuplicated`), chỉ khác là tính cả query.
⚠️ File DÙNG CHUNG (rail MISA của mọi phân hệ) → **đã hỏi user và được duyệt** trước khi sửa.

**Verify trên trình duyệt (bấm menu thật):**
`?mode=pending` → bấm "Đề nghị thanh toán" → URL sạch query, title "Phiếu đề nghị thanh toán" ·
URL sạch → bấm "Phiếu đề nghị thanh toán chờ duyệt" → `?mode=pending`, title đổi đúng. 0 lỗi console.
Trang tự nạp lại dữ liệu nhờ watcher `mode()` có sẵn ở `index.vue`.

---

### Task 6.3b — 2 chỉnh sau phản hồi user (2026-08-15)

- [x] 🐛 **THỦ PHẠM THẬT của khoảng trống: `.table-responsive { min-height: 50vh }` (style GLOBAL).**
  Đo trên trình duyệt: card "Chi tiết" cao **377px** trong khi cái bảng chỉ **83px** — 341px còn lại là
  `min-height` global áp cho MỌI `.table-responsive`. Fix: thêm class **`table-auto-height`** + scoped
  `.table-responsive.table-auto-height { min-height: 0 !important }` (khuôn có sẵn ở
  `components/assign-components/customer/manager/DocumentTable.vue`).
  **Kết quả đo lại: card-body 377px → 120px** (bảng 83px + padding), cả card 170px.
  ⚠️ Cùng rule này còn áp cho `.table-responsive` trong `DeliveryTripDetailModal` (popup 1 dòng) — chưa sửa,
  chờ user quyết.
- [x] **Bảng chi tiết thấp lại — CHỈ ĐỘNG VÀO CHIỀU CAO, không đổi cấu trúc.** 2 dòng CSS phụ:
  hàng rỗng bỏ `py-3` → `.empty-row` (padding 4px, chữ 12px, line-height 18px) và `th` của `.detail-table`
  ghim `padding: 4px 6px` (header 2 tầng nên mỗi px padding bị nhân đôi). Markup y như cũ:
  vẫn "Không có dữ liệu", vẫn header 2 tầng, vẫn `rowspan="2"`.

  ⚠️ **2 lần làm quá tay đã bị user bác — đừng lặp:**
  1. Thay cả bảng bằng khối `.detail-empty` 1 dòng + nút "Thêm dòng" → *"vẫn hiện table bình thường"*.
  2. Gộp header còn 1 tầng khi loại tiền VND (`:rowspan="headerRowspan"`, `<tr v-if="!isVnd">`) →
     *"sửa lại như lúc đầu, tôi bảo sửa height thôi"*.

  Bài học: yêu cầu chỉnh **kích thước** thì chỉ đụng CSS kích thước, không nhân tiện sắp xếp lại markup —
  kể cả khi thấy chỗ đó "thừa" (mốc so sánh user đưa là bảng `.matrix-table` ở
  `customer-care/services/create`, nhưng ý là ĐỘ CAO, không phải cấu trúc header).
- [x] 🐛 **Lỗi 422 hiện ra `[ "Bắt buộc nhập" ]`.** `errorOf()` của `BillPaymentRequestDetailTable` và
  `BankInfoSection` trả **thẳng `fieldErrors[key]`**, mà Laravel trả **mảng câu** → template in nguyên mảng.
  Đã chuẩn hoá `Array.isArray(error) ? error[0] : error` ở cả 2 file.
  ⚠️ Chỉ 2 component con dính: form cha dùng `fieldError()` của `formValidateMixin` (đã lấy `[0]` sẵn) —
  component con nào TỰ viết hàm đọc `fieldErrors` đều phải tự chuẩn hoá.

---

### Task 6.3 — `BillPaymentRequestDetailTable.vue`

**Files:**
- Create: `pages/finance/bill-payment-requests/components/BillPaymentRequestDetailTable.vue`

- [x] **Bước 1:** Ma trận cột theo loại chi — copy **đúng bảng ở spec 4.6**.
- [x] **Bước 2:** Popup chọn hợp đồng: loại 1 → `search-buy-contracts`; loại 2/6 → `search-contracts`. **Dùng lại** `pages/finance/bill-income-requests/components/ContractSearchModal.vue` (import theo đường dẫn tương đối, không copy file).
- [x] **Bước 3:** Chặn dòng trùng (`contractable_id` + `contractable_type`; loại 1 thêm `supplier_id`) → toast *"Hợp đồng đã tồn tại!"*.
- [x] **Bước 4: Trần số tiền — điểm KHÁC ERP**

```js
/**
 * Trần "Số tiền đề nghị chi": chỉ áp khi công nợ > 0.
 *
 * ⚠️ Khác ERP có chủ đích (spec 9.2): hợp đồng `hrm_contracts` chưa có bút toán nào nên công nợ
 * luôn = 0; bê nguyên luật ERP thì loại chi 2 bị cắt số tiền về 0 và màn không dùng được.
 * BE cũng áp đúng luật này — FE chỉ là lớp tiện dụng.
 */
capPaymentMoney(detail, value) {
    const debt = Number(detail.payment_money_foreign || 0)
    if (debt > 0 && [2].includes(Number(this.form.type)) && value > debt) return debt
    return value
},
```

- [x] **Bước 5:** Loại 12 — nút **Lấy dữ liệu**, checkbox chọn dòng + check-all, cột Hạch toán bấm mở `DeliveryTripDetailModal`.
- [x] **Bước 6:** Dòng Tổng cộng theo đúng 2 dạng ở spec 4.6.
- [x] **Bước 7: Verify** compile template.

---

### Task 6.4 — `AttachmentSection.vue`

**Files:**
- Create: `pages/finance/bill-payment-requests/components/AttachmentSection.vue`

- [x] **Bước 1:** Hiển thị file đã có (từ `attachments` BE trả) + chọn file mới (multiple), giới hạn đúng 9 đuôi + 20 MB.
- [x] **Bước 2:** Nhãn có dấu `(*)` đỏ khi `type == 1`.
- [x] **Bước 3:** Xóa file gọi `DELETE /{id}/attachments`, có xác nhận `BaseConfirmModal`.
- [x] **Bước 4: Verify** compile template.
- [x] **Bước 5 — Đổi giao diện theo khuôn "Import tài liệu kèm biên bản" (user yêu cầu 2026-08-15).**

**Khuôn tham chiếu:** `pages/assign/meeting/components/MeetingReport.vue` (khối 2), **BỎ cột "Tên tài liệu"**
→ lưới 4 cột: `STT (col-1) · Upload / File (col-8) · Dung lượng (col-2) · Xóa (col-1)`.
Nút **"Thêm tài liệu"** nằm bên phải `card-header`, bấm là thêm 1 **dòng trống** có nhãn "Chọn tệp";
dòng đã có file hiện icon theo đuôi + tên + cụm nút **Xem trước / Tải xuống / Thay đổi**, xem trước dùng
`components/modal/FilePreviewModal.vue` (modal này nhận được CẢ URL `file_path` lẫn `File` object).

⚠️ **Chỉ đổi GIAO DIỆN, KHÔNG đổi cách gửi file.** Màn biên bản upload ngay khi chọn (`uploadImage` →
lưu `file_path`); phiếu này vẫn theo khuôn `ProductTransferRequestForm` đã chốt trước đó — file mới nằm
trong `newFiles`, gửi kèm `attachments[]` lúc lưu phiếu, file đã lưu xóa bằng `DELETE /{id}/files`.
(Badge "Chờ lưu" từng gắn ở dòng file mới — user yêu cầu bỏ 2026-08-15.)

**2 điểm khác khuôn có chủ ý:**
1. **"Thay đổi" chỉ có ở dòng CHƯA lưu** — đổi file đã lưu buộc phải xoá object S3 ngay, không hoàn tác được.
   Cần thay thì Xóa rồi Thêm lại.
2. ~~**Dung lượng của file đã lưu hiện `—`**~~ → **đã bổ sung 2026-08-15** (user hỏi "sao xem chi tiết
   không hiện dung lượng"): endpoint **`GET /{id}/attachment-sizes`** trả map `{url: byte}`, lấy bằng
   **HTTP HEAD** vào chính URL S3 (file `ACL public-read` nên đọc được `Content-Length`, không cần ký).
   Chạy song song bằng `Http::pool` — đo thật: **11 file / 840ms**, 1 file / 110ms.
   ⚠️ **KHÔNG nhét vào `show()`**: `findForShow()` còn dùng cho màn in + xuất Excel, không đáng để 2 chỗ
   đó phải chờ S3. FE gọi endpoint này trong `watch: files` của `AttachmentSection`, hỏng thì cột hiện `—`.
   Verify trên trình duyệt (phiếu 4197): cột Dung lượng ra **38 KB**.

**Chi tiết dựng lưới:** `rows` là **computed** ghép `files` (của phiếu) → `pendingFiles` (chờ lưu) →
`placeholders` (dòng trống, state riêng của khối) ⇒ giữ nguyên hợp đồng props/emit với form cha.
Emit: `add-file` / `replace-file` / `remove-pending` / `remove-file`; đổi file dùng `splice(index, 1, item)`
để dòng **không nhảy xuống cuối lưới**.

- [x] **Bước 6 — Upload NGAY lúc chọn file để XEM TRƯỚC được (user chốt 2026-08-15, sau khi báo lỗi).**

🐛 **Triệu chứng user báo:** "sao tôi không xem trước được file như bên assign/meeting/create".
**Nguyên nhân:** `FilePreviewModal` xem trước **PDF bằng Google Docs Viewer** và **Word/Excel bằng Office
Online Viewer** — 2 dịch vụ này phải TỰ TẢI file qua URL công khai. Giữ file ở client (khuôn
`ProductTransferRequest`) thì modal chỉ có `blob:` URL nội bộ ⇒ **chỉ ảnh xem trước được**. Màn Biên bản
họp chạy được vì nó upload ngay lúc chọn nên có URL S3 thật.

**Đã đổi sang upload ngay** (user chọn phương án này, chấp nhận file rác trên S3 nếu bỏ form giữa chừng —
màn Biên bản họp cũng vậy):

| Lớp | Thay đổi |
| --- | --- |
| Route | `POST /finance/bill-payment-requests/upload-files` — route TĨNH, đặt TRƯỚC `/{id}` |
| Controller | `uploadFiles()` — validate 9 đuôi + 20MB, trả mảng URL. Không gate quyền riêng (cả nhóm route này không gắn `checkPermission`), chỉ đẩy file lên thư mục dùng chung |
| Service | `upload(array $files)` mới; `uploadAttachments()` nhận thêm `attachment_urls[]`, **vẫn nhận** `attachments[]` là FILE (luồng cũ) |
| FormRequest | `attachment_urls` thay `attachments` ở nhánh "loại chi 1 bắt buộc file"; mỗi URL phải `starts_with:` **`BillPaymentAttachmentService::URL_PREFIX`** |
| FE | `newFiles: [File]` → `pendingFiles: [{url, name, size}]`; lưu phiếu gửi `attachment_urls[]` thay vì file |

⚠️ **Bắt buộc chặn `starts_with`**: không có nó thì client gửi URL bất kỳ vào cột `attachments` — mà FE
render cột này thành link tải về. Prefix lấy từ dạng `ObjectURL` thật của `CmcS3Helper::putFile()`:
`https://tanphat.s3.cloud.cmctelecom.vn/bill_payment_requests/` (đã đối chiếu dữ liệu ERP trong DB).

- [x] **Bước 7 — Lỗi validate của khối file phải hiện TẠI khối file (user báo 2026-08-15).**

Trước đó BE trả 422 đúng nhưng FE chỉ toast "Vui lòng kiểm tra lại dữ liệu nhập" — người dùng không biết
thiếu ở đâu (vi phạm quy tắc validate của CLAUDE.md: lỗi phải inline tại từng ô required).

- Form cha: hằng `ATTACHMENT_ERROR_KEYS = ['attachment_urls', 'attachment_urls.0', 'attachments', 'attachments.0']`
  + computed `attachmentError` → truyền xuống prop **`errorMessage`** (KHÔNG đặt tên `errors`, xem bẫy vee-validate).
- `AttachmentSection`: `displayError = localError || errorMessage`, hiện bằng `V2BaseError` (class `.v2-error`
  nên `scrollToInputError()` cuộn tới được) + **viền đỏ cả card** (`.card--invalid`).
- Chọn được file → `clearFieldError()` cho cả 4 key: lỗi BE không tự mất vì thao tác không qua ô nhập.
- 422 của endpoint upload (`errors: {'attachments.0': [...]}`) cũng đổ vào `localError` thay vì chỉ toast.

Verify: `BillPaymentRequestStoreRequest::rules()` với loại chi 1 + không file → `attachment_urls` =
`required|array|min:1`, key lỗi trả về đúng **`attachment_urls`**, câu lỗi **"Bắt buộc đính kèm ít nhất 1 file"**.

**Verify (chạy thật, không mock):** upload 1 PNG → URL đúng prefix · `GET` URL đó trả **HTTP 200**
(⇒ Google/Office Viewer đọc được) · append vào chuỗi cũ đúng dấu `', '` · không gửi gì thì giữ nguyên
chuỗi cũ · URL lạ (`https://evil.example.com/...`) bị rule chặn · dọn file test khỏi S3 (còn **HTTP 403**).

---

# Phase 7 — FE chi tiết + duyệt + in

### Task 7.1 — Màn chi tiết

**Files:**
- Create: `pages/finance/bill-payment-requests/_id/index.vue`

- [x] **Bước 1:** Trang vỏ mỏng bọc `BillPaymentRequestForm` với prop `readonly` — đúng khuôn `pages/finance/bill-income-requests/_id/index.vue`.
- [x] **Bước 2:** Ở `readonly`, bảng chi tiết hiện thêm 4 cột tiền duyệt + cột "Số tiền chi"; cột của cấp **đang duyệt** thành ô nhập, các cột khác read-only.
- [x] **Bước 3:** Mặc định ô nhập của cấp hiện tại = số tiền cấp trước (port `after()` của `BillPaymentRequestDetail` JS ERP :12-23).
- [x] **Bước 4: Verify** compile template.

---

### Task 7.2 — Nút duyệt theo cấp + Không duyệt

**Files:**
- Create: `pages/finance/bill-payment-requests/components/ApproveActions.vue`
- Create: `pages/finance/bill-payment-requests/components/RejectModal.vue`

- [x] **Bước 1: Bảng nút theo trạng thái** (chỉ hiện khi `can_approve` BE trả về **true**)

| Trạng thái | Nút |
| --- | --- |
| 2 | **TP Duyệt** (`status = 3`) |
| 3 | **KT công nợ duyệt** (`status = 4`) |
| 4 | **KT Trưởng Duyệt** (`status = 6`) · **Chuyển duyệt BGĐ** (`status = 5`) |
| 5 | **BGĐ Duyệt** (`status = 6`) |
| mọi cấp trên | **Không duyệt** (mở `RejectModal`) |

- [x] **Bước 2:** `RejectModal` — ô lý do chung (`reject_comment`) + ô ghi chú **bắt buộc của đúng cấp**; validate inline `is-invalid` + `invalid-feedback`, flag `touched`.
- [x] **Bước 3:** Nút theo `.claude/skills/button-convention/SKILL.md`. **Không** dựng nút "Tạo phiếu chi" (ngoài phạm vi).
- [x] **Bước 4: Verify** compile template + grep fail-open.

---

### Task 7.3 — `DeliveryTripDetailModal.vue`

**Files:**
- Create: `pages/finance/bill-payment-requests/components/DeliveryTripDetailModal.vue`

- [x] **Bước 1:** Bảng 13 cột, header 2 tầng (cột "Cước tính toán" tách Chính / Phụ trội) — đúng `show.blade.php` :90-128.
- [x] **Bước 2:** Gọi `GET /delivery-trip-detail`; hiển thị `—` cho ô trống (không để trắng, không dùng `-`).
- [x] **Bước 3:** Theo `.claude/skills/modal-popup/SKILL.md`.
- [x] **Bước 4: Verify** compile template.

---

### Task 7.4 — Màn in

**Files:**
- Create: `pages/finance/bill-payment-requests/_id/print.vue`

- [x] **Bước 1:** Đọc `.claude/skills/print-page/SKILL.md` **trước khi viết** + `pages/finance/bill-income-requests/_id/print.vue` (250 dòng) làm khuôn.
- [x] **Bước 2:** 3 bố cục theo `template` BE trả (`ncc_tm` / `ncc_ck` / `chung`); bảng chi tiết 2 dạng VND / ngoại tệ (header 2 tầng).
- [x] **Bước 3:** Khối chữ ký 5 ô.
- [x] **Bước 4: Verify theo skill** — đo tràn mép phải = **0px**, đủ viền 4 cạnh (kể cả khi sang trang), logo tải được, tự bật hộp thoại in.

---

# Phase 8 — Seeder dữ liệu test + rà soát

### Task 8.1 — Seeder dữ liệu test

**Files:**
- Create: `Modules/Finance/Database/Seeders/BillPaymentRequestTestDataSeeder.php`

- [x] **Bước 1:** Đọc khuôn `Modules/Finance/Database/Seeders/BillIncomeRequestTestDataSeeder.php` (DRY-RUN mặc định, bật bằng biến môi trường).
- [x] **Bước 2:** Sinh **8 phiếu mẫu** mã `TEST.DNTT-CHI.*`: mỗi loại chi (1/2/6/12) 1 phiếu ở status 2, và 4 phiếu lần lượt ở status 3 / 4 / 5 / 6 để test từng cấp duyệt.
- [x] **Bước 3:** Gán 9 quyền mới cho tài khoản test của từng vai (TP / KT công nợ / KT trưởng / BGĐ / KT thanh toán) — in ra bảng `id nhân viên | vai` để user đăng nhập test.
- [x] **Bước 4: Verify**
```bash
php -l Modules/Finance/Database/Seeders/BillPaymentRequestTestDataSeeder.php
php artisan db:seed --class="Modules\Finance\Database\Seeders\BillPaymentRequestTestDataSeeder"   # DRY-RUN, chỉ in
FINANCE_TEST_DATA=1 php artisan db:seed --class="Modules\Finance\Database\Seeders\BillPaymentRequestTestDataSeeder"
php artisan tinker --execute="echo Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest::where('code','like','TEST.DNTT-CHI%')->count();"
```
Kỳ vọng: DRY-RUN không ghi gì; chạy thật ra **8**.

---

### Task 8.2 — Rà soát tổng thể

**Files:** không tạo file (chỉ sửa nếu phát hiện lỗi).

- [x] **Bước 1: Contract FE ↔ BE** — liệt kê mọi endpoint FE gọi, đối chiếu với `php artisan route:list --path=bill-payment-requests`; liệt kê mọi field FE đọc từ response, đối chiếu với 3 Resource. Không được có field FE đọc mà BE không trả.
- [x] **Bước 2: Quét fail-open toàn feature**
```bash
grep -rnE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payment-requests/
```
Kỳ vọng: rỗng.
- [x] **Bước 3: Quét sót ràng buộc**
```bash
grep -rn "mysql2\|DB_CONNECTION_SECOND\|DB_DATABASE_SECOND" Modules/Finance/ | grep -i payment
grep -rn "product_export_request" Modules/Finance/ | grep -i payment
grep -rn "checkPermission" Modules/Finance/Routes/api.php | grep -i bill-payment
```
Kỳ vọng: cả 3 lệnh **không có kết quả**.
- [x] **Bước 4: `php -l` toàn bộ file BE mới**
```bash
find Modules/Finance -newer composer.json -name "*.php" | xargs -n1 php -l | grep -v "No syntax errors" || echo "OK: khong loi cu phap"
```
- [x] **Bước 5:** Cập nhật `design.md`, `plan.md` (checkpoint), `STATUS.md`; báo user danh sách **phần chưa kiểm chứng** (những gì cần mở trình duyệt).

---

## Fix bug sau nghiệm thu

### Task BF.1 — Bộ lọc: nhãn "Khách hàng" và "Nhà cung cấp" hiện 2 lần
- [x] Cùng lỗi phát hiện ở màn Phiếu đề nghị thu tiền (Task 8.1 của `finance-bill-income-request`):
      `V2BaseSmartFilterPanel.vue:126` đã render `<V2BaseLabel>{{ field.label }}</V2BaseLabel>` cho field
      không khai `hideLabel`; slot `#field-customer_id` / `#field-supplier_id` render thêm 1 nhãn nữa.
- [x] Sửa `hrm-client/pages/finance/bill-payment-requests/index.vue` (dòng 32-33 và 44-45):
      bỏ 2 `<V2BaseLabel>` trong slot, để panel render nhãn từ schema (`index.vue:442-443`).
- [x] Verify: compile `vue-template-compiler` — 0 lỗi; không còn nhãn tự render trong template.
- [x] User mở trình duyệt xác nhận xong (2026-08-18).

**Quy tắc:** slot `#field-<key>` chỉ tự render nhãn khi field khai `hideLabel: true`
(kèm `wrapperClass: 'd-contents'` nếu slot dựng nhiều cột). Field 1 ô → KHÔNG đặt label trong slot.

### Checkpoint — 2026-08-18 (fix bug bộ lọc)
Vừa hoàn thành: Task BF.1 — bỏ 2 nhãn lặp ở bộ lọc màn danh sách (1 file FE). User test xong,
đã commit `hrm-client` `dde97025c`.
Đang làm dở: không có.
Bước tiếp theo: bổ sung popup Cấu hình cột hiển thị cho màn này (user chốt làm sau).
Blocked: không.

### Task BF.2 — Màn IN: khối ngân hàng lệch ERP (2026-08-20) — @khoipv
User hỏi "IBAN Number / Swift Code là gì, ở đâu, sao phiếu có phiếu không" → soi ra 3 lỗi thật.
Đối chiếu nguồn ERP: `report_templates` id 406 (mẫu `ncc_ck`) + `BillPaymentRequest::getPrintData()`
:818-819 và :835-840 của repo `erp`.

- [x] **Bug 1 — điều kiện hiện Swift/IBAN/Phí sai.** ERP gắn 3 dòng này với **NCC nước ngoài**
      (`customers.customer_type = 3`); nếu không phải thì `clearNull()` xoá cả nhãn. HRM lại gắn với
      **mẫu in** `ncc_ck` (`_id/print.vue:253`) → **1.876/2.594 phiếu (72%)** in ra 4 dòng rỗng `—`.
      Số liệu `gop_db`: mẫu ncc_ck có 718 phiếu NCC nước ngoài (718/718 có swift) và 1.876 phiếu
      trong nước (0 phiếu có swift).
- [x] **Bug 2 — mất Chi nhánh + Thành phố ở mẫu `ncc_ck`** (`_id/print.vue:267-271` nằm trong nhánh
      `else`). Template 406 của ERP CÓ `{{CHI_NHANH}}` + `{{THANH_PHO}}`, set vô điều kiện. Cả
      1.876 phiếu trong nước đều có dữ liệu 2 cột này → đang bị giấu. Thứ tự ERP: Thành phố trước Chi nhánh.
- [x] **Bug 3 — BE không trả cờ để FE phân biệt.** `BillPaymentRequestPrintResource` khối `bank`
      không có `customer_type` của NCC, `findForShow()` cũng không eager-load (Entity không có
      quan hệ `supplier` cấp phiếu) → thêm `bank.is_foreign_supplier`, query `customers` theo
      `supplier_id` giống cách `companyName()` đang làm.
- [x] **Bỏ phần HRM tự thêm** (user chốt "fix lại giống ERP" 2026-08-20): dòng *Địa chỉ ngân hàng*
      và khối *ngân hàng trung gian* (`mid_*`) — template 406 KHÔNG có placeholder nào cho chúng.
      Gỡ luôn `bank_address` + 5 key `mid_*` khỏi PrintResource để không còn dữ liệu chết.
- [x] Verify: `php -l` + parse `vue-template-compiler`; đối chiếu lại số phiếu từng nhánh bằng SQL.

**Không dính lỗi này:** màn chi tiết (`_id/index.vue` dùng lại `BillPaymentRequestForm` readonly →
theo đúng luật NCC nước ngoài, khớp `ng-if="form.type_supplier_transfer_foreign"` của ERP) ·
mẫu `ncc_tm` (735/735 phiếu loại 1 tiền mặt không có số tài khoản nên khối ngân hàng không hiện —
đúng như template 405 vốn không có placeholder ngân hàng) · file Excel (blade export không in khối ngân hàng).

- [x] **Đồng bộ nhãn + thứ tự khối ngân hàng của MÀN IN theo template ERP** (user chốt 2026-08-20):
      *Chủ tài khoản* → *Số tài khoản* → *Ngân hàng* → *Thành phố* → *Chi nhánh* (trước đó HRM để
      *Số tài khoản* / *Tên tài khoản* / *Tên ngân hàng*). ⚠️ FORM vẫn giữ bộ nhãn riêng
      (*Số tài khoản* / *Tài khoản* / *Tên ngân hàng*) — ERP cũng khác nhau giữa form và mẫu in,
      **không đồng bộ 2 nơi**.

### Task BF.3 — Dropdown "Loại tiền" hiện kèm mã tiền tệ (2026-08-21) — @khoipv
User chốt sửa đồng bộ với màn Phiếu đề nghị thu tiền (Task 8.3 của `finance-bill-income-request`):
ô chọn Loại tiền hiện `MÃ — Tên` cho **tất cả** loại tiền. Phạm vi: **chỉ dropdown**, không đụng
nhãn cột bảng chi tiết, cột "Loại tiền" ở danh sách và bản in.

- [x] `BillPaymentRequestForm.vue::loadOptions()`: option `name` = `${code} — ${name}`; giữ tên thuần
      ở khoá `short_name`. API `finance/currencies/getAll` đã trả sẵn `code` → **không sửa BE**.
- [x] `currencyName()` đọc `short_name` — computed này truyền xuống `BillPaymentRequestDetailTable`
      qua prop `currency-name` làm header cột 150px, dùng `name` đã ghép là vỡ layout.
- [x] Verify: compile template + babel parse — 0 lỗi; không còn chỗ nào đọc `selectedCurrency.name` trần.
- [ ] User mở trình duyệt xác nhận.

### Task BF.4 — Lỗi validate của dòng chi tiết đã xoá vẫn bám sang dòng mới (2026-08-21) — @khoipv
Sửa đồng bộ với Task 8.7 của `finance-bill-income-request` (user báo bug ở màn thu tiền, chốt sửa
luôn màn chi tiền). `formErrors` khoá theo VỊ TRÍ dòng (`details.0.contractable_id`) mà `removeDetail()`
chỉ `splice` mảng → xoá dòng đang báo "Bắt buộc nhập" rồi thêm dòng mới là thấy y nguyên câu lỗi,
chưa kịp bấm Lưu. Bảng chi tiết nhận lỗi qua prop `:field-errors="formErrors"` nên hiện luôn.

- [x] `BillPaymentRequestForm.vue`: thêm `shiftDetailErrors(removedIndex)` (xoá lỗi dòng bị xoá + dồn
      index dòng sau) và `clearAllDetailErrors()`; `removeDetail()` gọi ngay sau `splice`.
- [x] Gọi `clearAllDetailErrors()` ở 2 chỗ thay trắng bảng: `pendingAction` của confirm đổi đối tượng
      (`form.details = []`) và lúc nạp lại bảng từ **chuyến giao hàng**
      (`delivery-trip-accounting-details` — thay toàn bộ dòng, lỗi cũ không còn ứng với dòng nào).
- [x] Verify: compile template + babel parse — 0 lỗi. Logic dồn index đã test ở màn thu tiền
      (1 dòng lỗi bị xoá → sạch · xoá dòng giữa của 3 → `details.2.*` tụt về `details.1.*` ·
      lỗi cấp phiếu `reason`/`details` giữ nguyên).
- [ ] User mở trình duyệt xác nhận.

**Ghi chú kỹ thuật:** 2 helper hiện **chép ở cả 2 form** thay vì đưa lên `utils/mixins/formValidateMixin.js`
— mixin là file dùng chung, chưa được user chốt cho đụng. Nếu màn thứ 3 cần thì gom lên mixin.

### Checkpoint — 2026-08-20 (Task BF.2 — khối ngân hàng màn in)
Vừa hoàn thành: sửa khối ngân hàng màn in về đúng luật ERP — 2 file:
`hrm-api/Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestPrintResource.php`
(thêm `isForeignSupplier()` + `bank.is_foreign_supplier`, bỏ `bank_address` + 5 key `mid_*`) ·
`hrm-client/pages/finance/bill-payment-requests/_id/print.vue` (`bankRows()` đổi điều kiện, thêm
Thành phố + Chi nhánh cho mọi mẫu, bỏ Địa chỉ NH + khối NH trung gian).
Gỡ thêm computed `template` ở FE vì sau khi sửa không còn nơi dùng — key `template` BE vẫn trả
(mô tả mẫu ERP của phiếu, giữ để đối chiếu).
Đợt sau trong cùng buổi: đổi nhãn + thứ tự 3 dòng đầu khối ngân hàng màn in cho khớp template ERP
(*Chủ tài khoản* / *Số tài khoản* / *Ngân hàng*), FE compile lại sạch.

Verify đã chạy: `php -l` sạch · `vue-template-compiler` + `@babel/parser` parse sạch, 0 tham chiếu
sót tới `this.template` / `bank_address` / `mid_*` · chạy `BillPaymentRequestPrintResource` thật qua
tinker trên 3 phiếu đại diện (customer_type 1 / 2 / 3): cờ `is_foreign_supplier` ra đúng
false / false / true, phiếu NCC nước ngoài giữ swift `ICICINBBCTS` + phí, 2 phiếu còn lại có
Chi nhánh + Thành phố thật.

**Chưa kiểm chứng trên trình duyệt** (user tự mở): mở phiếu NCC trong nước loại 1 + CK xem đã hết 4
dòng `—` và đã có Chi nhánh + Thành phố; mở phiếu NCC nước ngoài xem còn đủ Phí / IBAN / Swift.

Ghi chú dữ liệu: 35 phiếu có NCC để `customer_type = 1` nhưng ngân hàng lại ở nước ngoài (vd id=1,
IDFC FIRST BANK / Ấn Độ) → sẽ KHÔNG in Swift/IBAN. Đây là dữ liệu danh mục NCC phân loại thiếu,
ERP cũng xử lý y hệt — muốn in thì sửa `customer_type` của NCC, không sửa màn in.

Đang làm dở: không.
Bước tiếp theo: user test trình duyệt rồi tự commit 2 repo (Claude không commit).
Blocked: không.

## Checkpoint

### Checkpoint — 2026-08-15 (ĐỢT SỬA THEO PHẢN HỒI USER — 10 hạng mục, ĐÃ COMMIT)

Vừa hoàn thành: 10 hạng mục chỉnh sửa sau khi user dùng thật, chia 3 nhóm.

**A. Khối File đính kèm — làm lại theo khuôn "Import tài liệu kèm biên bản"** (`MeetingReport.vue`),
BỎ cột "Tên tài liệu" (Task 6.4 bước 5-7):

| # | Việc | Ghi chú |
| --- | --- | --- |
| 1 | Lưới `STT · Upload/File · Dung lượng · Xóa` + nút "Thêm tài liệu" tạo dòng trống | bỏ badge "Chờ lưu" (user yêu cầu) |
| 2 | Giới hạn đuôi/dung lượng chuyển thành **tooltip** (hover nút "Thêm tài liệu" + ô "Chọn tệp") | bỏ dòng chữ xám + dòng "Chưa có tài liệu nào" |
| 3 | **Upload NGAY khi chọn file** — route mới `POST /upload-files`, lưu phiếu gửi `attachment_urls[]` | vì `FilePreviewModal` xem trước PDF/Office qua Google & Office Viewer, cần URL công khai |
| 4 | **Dung lượng file đã lưu** — route mới `GET /{id}/attachment-sizes` (HEAD S3 song song) | 1 file 110ms · 11 file 840ms |
| 5 | Lỗi validate hiện **tại khối file** (prop `errorMessage` + viền đỏ card) | trước chỉ toast chung chung |

⇒ **17 route** (15 + 2 mới).

**B. Bám sát ERP + sửa lỗi hiển thị:**

| # | Việc |
| --- | --- |
| 6 | **Người tạo / Phòng ban hiện ở màn TẠO** (ERP `form.blade.php` :117-125) — lấy từ `meta.creator` của BE, KHÔNG tra `state.departments` (danh sách đó chỉ có phòng ban `status = 1`) |
| 7 | **Bỏ ô "Ghi chú" cấp phiếu** (ERP chỉ có cột Ghi chú trong bảng chi tiết) → card đổi thành "Lịch sử duyệt", chỉ hiện ở màn xem. Vẫn nạp + gửi lại cột `note` để không xoá dữ liệu phiếu ERP |
| 8 | 🐛 Lỗi 422 hiện ra `[ "Bắt buộc nhập" ]` — `errorOf()` của 2 component con trả thẳng MẢNG của Laravel |
| 9 | 🐛 Bảng chi tiết trống cao 377px — thủ phạm là `.table-responsive { min-height: 50vh }` GLOBAL, không phải padding (2 lần đầu sửa nhầm chỗ) |
| 10 | Ô "Tỷ giá" khoá để nền trắng khác mọi ô khoá khác → đè `::v-deep .v2-currency-input:disabled` ở màn này (không sửa component dùng chung) |

**C. 1 sửa file DÙNG CHUNG (đã hỏi user và được duyệt):** `SaleHubSidebar::openScreen()` so
`$route.path` → **`$route.fullPath`** ⇒ 2 mục menu chỉ khác query mới chuyển qua lại được (Task 6.5).

**Dữ liệu (user yêu cầu, DB local):** thêm `employee_manage_departments` id 368 (NV 13 – phòng 111 –
công ty 1) để tài khoản test duyệt được phiếu 4197; bật lại `departments.id = 111` `status 0 → 1`.
Snapshot 2 bảng ở `scratchpad/emd_employee13_backup.json` + `department111_backup.json`.

Đang làm dở: không.

Bước tiếp theo: không còn việc kỹ thuật nào treo. ✅ **User đã test xong và xác nhận popup Chi tiết
chuyến xe hiện đủ 13 cột (2026-08-15)** — điểm treo duy nhất còn lại của feature đã đóng.
Việc còn lại thuần dọn dẹp khi anh không cần test nữa: hoàn tác 2 thay đổi dữ liệu DB local
(`employee_manage_departments` id 368 · `departments.id = 111` `status 1 → 0`) và xoá 8 phiếu mẫu
`TEST.DNTT-CHI.*`.

Blocked: không.

**Trạng thái repo: ĐÃ COMMIT (user tự commit, không phải Claude)** — `hrm-api` `6eed9d2a6`,
`hrm-client` `8c0ffb424`, cùng thông điệp "Phiếu đề nghị thanh toán", nhánh `gop_db`, cây làm việc sạch.

---

### Checkpoint — 2026-08-15 (ĐÃ TEST PLAYWRIGHT — bắt 3 lỗi thật, đã sửa)

User yêu cầu test trình duyệt (khác lệ thường "user tự test"). Chạy Playwright trên
`localhost:3000` với tài khoản **DNS Admin (employee 13)**.

**🐛 3 lỗi FE chỉ lộ khi chạy thật — đã sửa:**

| # | Lỗi | Nguyên nhân | Cách sửa |
| --- | --- | --- | --- |
| 1 | Vue warn *"computed property errors is already defined as a prop"*, prop bị che | **vee-validate v2 cài mixin TOÀN CỤC** thêm computed `errors` + `fields` vào MỌI component ⇒ đặt tên prop là `errors` là đụng | đổi prop → **`fieldErrors`** ở `BillPaymentRequestDetailTable` + `BankInfoSection` |
| 2 | **Chặn nghiệp vụ**: hình thức CK không mở được popup hợp đồng (ô báo *"Chọn nhà cung cấp trước"*) | CK chọn NCC ở **cấp phiếu**, cột đối tượng theo dòng bị ẩn nên `detail.supplier_id` luôn rỗng | thêm prop **`partyId`** vào bảng chi tiết; `contractPickerReady()` xét party cấp phiếu khi CK |
| 3 | Popup "Chi tiết chuyến xe" mở ra **rỗng** | `b-modal` bắn `@show` NGAY khi gọi `show()`, prop `detail` chưa kịp cập nhật → `onShow()` thoát sớm **và xoá `row`** | `$nextTick` trước khi `show()` + watcher `detail` + không xoá `row` trước khi biết có id |

📌 **2026-08-15 — user báo "phiếu 4197 chờ TP duyệt mà không thấy nút duyệt".** Không phải bug:
`canApproveAtCurrentStatus()` ở nhánh TP đòi **phiếu thuộc phòng ban mình quản lý**, mà phiếu 4197 nằm ở
phòng **111 (PHÒNG CỘNG TÁC VIÊN_NV, `status = 0`)** — không có trong 22 phòng DNS Admin (NV 13) quản lý.
Quyền TP thì có, công ty thì khớp (đều = 1).

⚠️ **Ràng buộc phòng ban này là HRM tự thêm, ERP KHÔNG có** — ERP `show.blade.php:33` chỉ xét
`can('Trưởng phòng duyệt…') && status == 2`; ERP chỉ lọc phòng ban ở `canView()` (:674-683) và ở tab
"Chờ duyệt" (:348-357). Theo CLAUDE.md lẽ ra phải hỏi trước khi thêm phân quyền theo cấp.

**User chốt: GIỮ ràng buộc trong code, cấp thêm phòng ban cho tài khoản.** Đã `INSERT` 1 dòng
`employee_manage_departments` (id 368: employee 13 – department 111 – company 1), snapshot 23 dòng cũ ở
`scratchpad/emd_employee13_backup.json`. Verify sau khi cấp: `canApprove` = true, `canCancel` = true,
`nextStatuses` = [3], phiếu 4197 xuất hiện ở tab Chờ duyệt.

📌 Ngoài ra sửa **seeder dữ liệu test**: phiếu mẫu trước đây rơi vào phòng ban của người lập (111),
mà tài khoản đó **không quản lý** phòng đó ⇒ nhánh "TP duyệt" của `canApproveAtCurrentStatus()`
chặn đúng luật nhưng không test được. Seeder nay lấy **phòng mà chính người lập đang quản lý**
(`employee_manage_departments`).

**✅ Luồng duyệt 5 cấp — chạy THẬT trên trình duyệt, đối chiếu DB sau mỗi bước:**

| Bước | Thao tác UI | Kết quả |
| --- | --- | --- |
| 1 | Sửa tiền dòng 1 → **TP Duyệt** | status 2 → 3, cột TP ghi **900.000** (số vừa sửa) |
| 2 | Nhập **5.000.000** (vượt trần) → **KT công nợ duyệt** | status 3 → 4, DB ghi **900.000** = đúng trần cấp trước ⇒ **trần cắt ở BE ăn thật** |
| 3 | **Chuyển duyệt BGĐ** | status 4 → 5 (nhánh 2 nút của KT trưởng hiện đúng) |
| 4 | **BGĐ Duyệt** | status 5 → 6, đủ 4 cột người duyệt = 13 |
| 5 | **Không duyệt** ở cấp **TP** | status → **1 "Đang tạo"** ⇒ giữ đúng bẫy ERP; footer đổi sang Sửa/Xóa |
| 6 | **Không duyệt** ở cấp **KT công nợ** | status → **10 "Không duyệt"**, ghi đúng cột `note_accountant_dept` |
| 7 | Bấm Không duyệt khi chưa nhập ghi chú | lỗi inline **"Bắt buộc nhập"** + viền đỏ |
| 8 | Nhãn ô ghi chú trong modal | đổi theo cấp: *"Ghi chú của Trưởng phòng"* → *"…Kế toán công nợ"* |

Ô nhập của cấp đang duyệt luôn **điền sẵn số tiền cấp trước** (kiểm ở cả 4 cấp).

**✅ Các phần khác đã xác nhận trên trình duyệt:**
- **Danh sách 4 chế độ**: Tất cả / Của tôi / Chờ duyệt / Đã duyệt — đổi tab đổi cả tiêu đề + dữ liệu;
  cột "Số tiền" đổi theo trạng thái đúng (phiếu status 6 hiện tiền KT trưởng, status 5 hiện tiền KT công nợ).
- **Form tạo mới**: đổi TM → CK thì hiện ô "Nhà cung cấp" ở Thông tin chung + khối ngân hàng, và
  bảng chi tiết **bỏ cột NCC** (đúng ma trận spec 4.6).
- **Nhánh NCC nước ngoài**: chọn NCC `customer_type = 3` → khối ngân hàng tự đổi sang 2 select +
  12 ô read-only; chọn ngân hàng → **tự điền 6 trường** (số TK / tài khoản / tên NH / swift / IBAN / địa chỉ).
- **Popup chọn NCC** (9.547 dòng) và **popup hợp đồng mua** (lọc đúng theo NCC, có cột công nợ).
- **Loại chi 12**: nút "Lấy dữ liệu" sinh **14 dòng** chuyến xe, có checkbox + check-all, cột
  Tổng cước / Đã thanh toán / Số tiền còn lại tính đúng (2.160.000 − 2.000.000 = 160.000).
- **Màn in**: letterhead tải được, 3 mẫu chọn đúng, cột duyệt chưa tới lượt in `_`, 5 ô chữ ký
  ngược thứ tự như ERP. Đo theo skill `print-page`: **tràn mép phải 0px**, viền đủ 4 cạnh
  (`border-collapse: collapse`, 1px mọi ô).
- **Guard "chưa lưu"** bật khi rời form đang nhập dở.
- **Console**: 0 lỗi ở màn danh sách / in; màn form+chi tiết còn **1 warning CÓ SẴN** của
  `ChooseErpCustomerModal` (*computed "fields" already defined in data*) — lỗi của component dùng
  chung, hiện ở mọi màn nhúng nó, không phải của feature này.

**✅ Popup Chi tiết chuyến xe — ĐÃ XÁC NHẬN BẰNG MẮT (user bấm thật, 2026-08-15): hiện đủ 13 cột.**
(Trong phiên test trước chỉ chứng minh được bằng cách gọi thẳng `onShow()` vì Nuxt dev không rebuild
kịp bundle của `BillPaymentRequestForm` — nay đã bấm lại sau khi restart, khớp kết quả.)

📌 **NCC có dữ liệu để test loại chi 12** (công ty 1, tra bằng chính `accountingDetails()`):
`37TNGXBI` NGUYỄN KHÁNH TOÀN (id 14059 — **14 dòng**, 24.276.112) · `29TPHXNA-10` HOÀNG MINH HUY
(id 7040 — 25 dòng) · `29TPHPTH-12` TÂN PHÁT (id 620 — **2.764 dòng**, API 2,6s, chỉ dùng khi cần thử tải nặng).
⚠️ NCC **11810 / 11735 có phát sinh nhưng đã trả hết** ⇒ "Lấy dữ liệu" ra 0 dòng — đừng tưởng lỗi.

**Dữ liệu sau khi test** (phiếu mẫu, không phải dữ liệu nghiệp vụ): 01 → status 6 · 02 → status 1 ·
05 → status 10 · 07 → status 6. Muốn về trạng thái ban đầu thì xoá theo câu lệnh ở docblock seeder
rồi chạy lại seeder.

---


### Checkpoint — 2026-08-15 (**HOÀN THÀNH 8/8 PHASE — 29/29 task**)

**Vừa hoàn thành: Phase 6 (FE form) + Phase 7 (FE chi tiết/duyệt/in) + Phase 8 (seeder + rà soát).**

| Phase | Sản phẩm | Bằng chứng |
| --- | --- | --- |
| 6 | `BillPaymentRequestForm` + `BankInfoSection` + `BillPaymentRequestDetailTable` + `AttachmentSection` + 2 trang vỏ | compile template + parse script **sạch 12/12 file** |
| 7 | `_id/index.vue` (chi tiết) · `ApproveActions` · `RejectModal` · `DeliveryTripDetailModal` · `_id/print.vue` | như trên; màn in bám đủ 8 quy tắc skill `print-page` |
| 8 | `BillPaymentRequestTestDataSeeder` + rà soát tổng thể | DRY-RUN không ghi; chạy thật ra **đúng 8 phiếu**, mỗi phiếu 2 dòng |

**Rà soát tổng thể (Task 8.2) — kết quả:**
- **Contract FE ↔ BE**: dựng script đối chiếu tự động (dump khoá 3 Resource bằng tinker rồi diff
  với field FE đọc). 🐛 **Bắt được 1 lỗi thật**: `BillPaymentRequestDetailResource` **thiếu**
  `accounting_code` + 2 id phiếu hạch toán ⇒ mở lại phiếu loại 12 sẽ **mất cột "Hạch toán"** và
  sửa xong là **đứt liên kết chuyến xe**. Đã bổ sung cả BE lẫn `mapDetail()` của FE.
  Sau khi vá: không còn field nào FE đọc mà BE không trả (các khoá còn báo là `item.key/label` của
  tab chế độ và `text/fullname` của popup chọn KH — nguồn khác, không phải resource này).
- **Quét fail-open** `pages/finance/bill-payment-requests/`: **rỗng**.
- **Quét ràng buộc**: không có `mysql2` / `DB_CONNECTION_SECOND`, không đụng bảng
  `..._product_export_requests`, không route nào gắn `checkPermission` (3 lệnh chỉ khớp trong
  **comment** giải thích, không phải code chạy).
- **`php -l`** toàn bộ file BE của feature: sạch.
- **Smoke test HTTP** sau khi hoàn thiện (server thật, tài khoản dev): `GET /{id}` 200 ·
  `/print-data` (template `ncc_tm`, 5 ô chữ ký, cờ cột duyệt đúng) · `/party-banks`
  (NCC nước ngoài `customer_type = 3`, 1 ngân hàng) · `/delivery-trip-accounting-details` 14 dòng ·
  `/{id}/export` 200 (80 KB) · 4 chế độ danh sách: all **4.029** · mine **8** · pending **123** ·
  approved **4**.

**Bổ sung ngoài plan (đều đã ghi lý do tại chỗ):**
1. **Endpoint BE mới `GET /party-banks`** — spec 4.5 đòi khối ngân hàng tự điền từ `supplier_banks`
   (380 dòng) và từ cột ngân hàng của `customers`, nhưng Phase 4 chưa có API nào trả dữ liệu đó
   ⇒ không có thì khối ngân hàng của form là ô trống vĩnh viễn.
2. **`ContractSearchModal` thêm prop `extraParams`** (thuần thêm, mặc định `{}`) để loại chi 2
   gửi `only_mine=1` — không đụng hành vi màn Đề nghị thu tiền.
3. **`BillPaymentRequestDetailTable` thêm `approvalMode` + `editableMoneyKey`** — màn chi tiết hiện
   3 cột tiền của các cấp, cột của cấp ĐANG duyệt thành ô nhập (mặc định điền sẵn số cấp trước).
4. **`reject_comment` thêm vào print resource** để bản in hiện lý do trả lại.

**Tổng kết feature:** BE **15 route** · 30 file mới + 5 file sửa ở `hrm-api`;
FE **12 file mới** + 2 file sửa ở `hrm-client`.

**⚠️ CHƯA KIỂM CHỨNG (cần user mở trình duyệt):** toàn bộ phần FE mới chỉ verify bằng
compile + đối chiếu contract, **chưa chạy thật trên trình duyệt** (theo lệ đã chốt: user tự test UI).
Cụ thể cần mắt người xác nhận:
- Luồng tạo phiếu 4 loại chi (đổi Loại chi/Hình thức TT có xoá đúng dữ liệu nhánh cũ không).
- Khối ngân hàng NCC nước ngoài (2 select + 12 ô read-only tự điền).
- Loại 12: nút "Lấy dữ liệu", checkbox chọn dòng, popup Chi tiết chuyến xe 13 cột.
- Luồng duyệt 5 cấp trên màn chi tiết (nút theo cấp, ô nhập tiền của đúng cấp).
- Màn in: đo tràn mép phải / viền / logo theo skill `print-page` (chỉ chạy được trên trình duyệt).
- Upload file trong luồng tạo/sửa phiếu (endpoint đã test riêng bằng curl, chưa test qua UI).

**Dữ liệu test sẵn sàng:** 8 phiếu `TEST.DNTT-CHI.01..08` (4 loại chi ở status 2 + 4 phiếu ở
status 3/4/5/6), người lập `employee_id = 13`. Câu lệnh dọn nằm ở docblock seeder.

**Blocked:** không.

---



### Checkpoint — 2026-08-15 (PHASE 5 XONG — FE danh sách + menu)

**Vừa hoàn thành: Phase 5 (2/2 task). Cộng dồn 23/29 task. Lần đầu đợt này đụng `hrm-client`.**

| Task | Nội dung | Bằng chứng |
| --- | --- | --- |
| 5.1 | `pages/finance/bill-payment-requests/index.vue` — 1 file, **4 chế độ** đọc từ `?mode=` | template compile **errors: none**, script parse OK, grep fail-open rỗng |
| 5.2 | 3 mục menu trong `components/subsystem-menu/finance.js` | nạp thật file menu: đúng 3 mục, không mục nào thiếu link |

**Đáng nhớ (đã ghi chi tiết trong 2 task):**
- 🐛 **Lệnh verify template trong plan sai** — `split('<template>')[1]` cắt nhầm ở
  `<template #cell-...>` nên báo lỗi giả. Phải lấy tới `</template>` cuối cùng trước `<script>`.
- 🐛 **`localStorageKey` không được khai bằng computed**: `filterStateMixin` đã khai trong `data()`,
  trùng tên thì Vue giữ data + bỏ computed ⇒ 4 chế độ ghi đè bộ lọc của nhau. Gán trong
  `restoreSavedFilters()` theo `mode`.
- **Thêm thanh 4 chế độ** ở `#left-actions` (menu chỉ có 2 lối vào, thiếu đường tới `mine`/`approved`).
- Cột **Số tiền không cho sort** vì BE chưa có nhánh sort cho cột tổng (bật ra thì bấm không đổi).
- Mục menu chờ duyệt **không gate `isShow`** như màn Đề nghị thu tiền — màn này có 5 vai duyệt.

**Đang làm dở:** không.

**Bước tiếp theo:** **Phase 6 — FE form tạo/sửa** (Task 6.1 khung form + Thông tin chung → 6.2
`BankInfoSection` → 6.3 bảng chi tiết → 6.4 `AttachmentSection`).
⚠️ Task 6.4 nhớ bám khuôn HRM: file gửi kèm trong `store`/`update` bằng multipart (`attachments[]`),
sửa có file thì `POST` + `_method=PUT`, gỡ file gọi `DELETE /{id}/files` với `file_url`.
⚠️ Các link ở màn danh sách (`/create`, `/{id}`, `/{id}/edit`, `/{id}/print`) **chưa có trang** —
sẽ dựng ở Phase 6/7, hiện bấm vào là 404 (đúng thứ tự phase, không phải lỗi).

**Trạng thái repo (nhánh `gop_db`, CHƯA COMMIT):**
`hrm-api` 4 file `M` + 27 file mới · `hrm-client` **1 file mới**
(`pages/finance/bill-payment-requests/index.vue`) + **1 file `M`**
(`components/subsystem-menu/finance.js`).

**Blocked:** không.

---

### Checkpoint — 2026-08-15 (PHASE 4 XONG — **BE HOÀN TẤT**)

**Vừa hoàn thành: Phase 4 (3/3 task). Cộng dồn 21/29 task — toàn bộ backend đã xong.**

| Task | Nội dung | Bằng chứng |
| --- | --- | --- |
| 4.1 | File đính kèm: `upload()` / `remove()` + FormRequest + 2 endpoint | `parse()` đúng trên **3.432 phiếu / 11.587 file**, 0 lỗi; 422 + 403 đúng chỗ |
| 4.2 | `BillPaymentRequestPrintResource` + `GET /{id}/print-data` | 5 phiếu: 3 template đúng, cờ cột + chữ ký đúng theo trạng thái |
| 4.3 | `BillPaymentRequestExport` + blade + `GET /{id}/export` | tải 3 file thật, **mở lại bằng PhpSpreadsheet**, tổng tiền khớp DB |

**Tổng API của màn: 14 route** (4 đọc danh sách/chi tiết · 5 ghi · 2 loại chi 12 ·
**1 gỡ file** (`DELETE /{id}/files` — không có endpoint upload riêng, file gửi kèm trong
`store`/`update` theo khuôn HRM) · 1 print-data · 1 export).

**Đáng chú ý:**
- Đọc được **repo ERP tại `D:/laragon/www/erp`** → Task 4.3 bám đúng cột động của ERP thay vì đoán.
  (Lần sau cần đối chiếu hành vi ERP thì có sẵn source ở đó — trước giờ toàn suy từ spec.)
- Bản in và file Excel **dùng chung một nguồn số** (`BillPaymentRequestPrintResource`) nên không
  thể lệch nhau.
- Cột "Số tiền duyệt" luôn `_` vì màn Phiếu chi ngoài phạm vi — đúng ERP, không phải thiếu sót.

**🔁 Sửa lại sau khi user chốt (2026-08-15):** phần file đính kèm làm **đúng khuôn HRM đang chạy**
(`ProductTransferRequest`) thay vì thiết kế upload-trước-lấy-URL — chi tiết ở Task 4.1.
Đã chạy vòng đời file **thật lên S3** (upload → append → gỡ → object biến mất) và dọn sạch, không
để lại file rác. Không còn khoản "chưa kiểm chứng" nào của Phase 4.

**Đang làm dở:** không.

**Bước tiếp theo:** **Phase 5 — FE danh sách + menu** (Task 5.1 `index.vue` 4 chế độ, 5.2 menu),
rồi Phase 6 (form), Phase 7 (chi tiết + in), Phase 8 (seeder test + rà soát).
Đây là lần đầu đợt này đụng `hrm-client`.

**Trạng thái repo (`hrm-api`, nhánh `gop_db`, CHƯA COMMIT):** 4 file `M` + **27 file mới**
(thêm so với checkpoint trước: `Transformers/.../BillPaymentRequestPrintResource.php`,
`Exports/BillPaymentRequestExport.php`, `Resources/views/exports/bill_payment_request.blade.php`,
`Http/Requests/BillPaymentRequest/BillPaymentRequestUploadRequest.php`).
`hrm-client` **chưa đụng gì**.

**Blocked:** không.

---

### Checkpoint — 2026-08-15 (PHASE 3 XONG — hết BE lõi)

**Vừa hoàn thành: toàn bộ Phase 3 — loại chi 12 (vận chuyển), 4/4 task. Cộng dồn 18/29 task.**

| Task | Nội dung | Bằng chứng |
| --- | --- | --- |
| 3.1 | 8 entity read-only chuyến xe + bảng giá cước | `php -l` sạch, đếm + chạy thật quan hệ 3 tầng |
| 3.2 | `accountingDetails()` + `paidMoneyForDetail()` | **4/4 NCC khớp SQL thuần tuyệt đối** (14 / 25 / 0 / 2.764 dòng) |
| 3.3 | `tripDetail()` popup 13 cột | đủ 13 khoá, 22/30 chuyến ra cước > 0, ca thiếu giá **không nổ** |
| 3.4 | 2 endpoint + route | 11 route, đặt trước `/{id}`, 3 ca thiếu tham số → 422 |

**Đã gỡ TODO** của Task 1.5: nhánh loại 12 trong `detailPaymentMoney()` gọi thật
`DeliveryTripPaymentService::paidMoneyForDetail()` (công thức HẸP khi mở lại phiếu).

**3 chỗ plan/spec ghi sai đã sửa khi làm** (đều chỉ lộ ra khi đối chiếu `information_schema`):
1. Chuỗi morph là `App\Model\**Warehouse**\DeliveryTripAccounting`, không phải `...\Delivery\...`
   → viết theo spec là query ra **0 dòng**.
2. `warehouse_exports`/`warehouse_imports` **không có** `delivery_trip_id`, cũng **không có** bảng
   `activities` → phải đi qua pivot `activity_has_delivery_trips` / `activity_has_other_delivery_trips`.
3. Nhân viên kinh doanh phải tra qua **`employees`** rồi mới sang `employee_infos` — tra thẳng
   `employee_infos` ra **người khác** (id trùng nhau trên DB gộp).

**Đang làm dở:** không.

**Bước tiếp theo:** **Phase 4 — file đính kèm + màn in + xuất Excel**
(Task 4.1 → 4.2 → 4.3). `BillPaymentAttachmentService` đã có sẵn `sync()` + `parse()` từ Phase 2,
Task 4.1 chỉ bổ sung `upload()` / `remove()` + 2 endpoint.

**Trạng thái repo (`hrm-api`, nhánh `gop_db`, CHƯA COMMIT):** 4 file `M` + **22 file mới**
(thêm so với checkpoint trước: 8 entity `Entities/Delivery/`, `Services/DeliveryTripPaymentService.php`).
`hrm-client` **chưa đụng gì**.

**Blocked:** không.

---

### Checkpoint — 2026-08-15 (PHASE 1 + PHASE 2 XONG)

**Vừa hoàn thành: toàn bộ Phase 2 (6/6 task), sau khi khép Phase 1 cùng ngày.**

| Task | Nội dung | Bằng chứng |
| --- | --- | --- |
| 2.1 | 2 FormRequest Store/Update (ma trận 4 loại chi × 2 hình thức) | Validator thật **15/15 ca** |
| 2.5 | `BillPaymentRequestNotifyService` (3 sự kiện) | người nhận 12–37/nhóm, nội dung ≤ 120 ký tự |
| 2.2 | `store` / `update` / `destroy` / `syncDetails` / `masterPayload` + `BillPaymentAttachmentService` | vòng đời HTTP thật |
| 2.3 | `BillPaymentApprovalService::approve()` + FormRequest | trần cắt ở BE: 99.999.999 → 500.000 |
| 2.4 | `reject()` + FormRequest ghi chú theo cấp | TP→status 1, cấp sau→status 10 |
| 2.6 | 5 action ghi + 5 route + verify | **6/6 bước vòng đời 200**, **10/10 ca xấu bị chặn** |

**Điểm đáng nhớ của đợt này:**
- Duyệt 5 cấp chạy thật với **6 tài khoản khác nhau**, mỗi cấp ghi đúng cột tiền riêng và đúng
  cột người duyệt; người lập **không cần quyền nào** vẫn tạo được phiếu.
- Trần số tiền **cắt ở BE** (ERP chỉ cắt ở FE) — đã chứng minh bằng số thật.
- Giữ đúng bẫy ERP: **TP không duyệt → phiếu về "Đang tạo"**, không phải "Không duyệt".
- Dữ liệu test đã dọn sạch, bảng về đúng **4.040 phiếu**.

**Đang làm dở:** không.

**Bước tiếp theo:** **Phase 3 — loại chi 12 (vận chuyển)**: Task 3.1 (8 entity read-only chuyến xe
+ bảng giá cước) → 3.2 (`DeliveryTripPaymentService::accountingDetails()` + `paidMoneyForDetail()`)
→ 3.3 (popup 13 cột) → 3.4 (2 endpoint loại 12).
⚠️ Khi làm **Task 3.2 phải gỡ TODO** trong `BillPaymentRequestService::detailPaymentMoney()`
(nhánh loại 12 đang tạm trả `money_payed = 0`).

**Trạng thái repo (`hrm-api`, nhánh `gop_db`, CHƯA COMMIT):** 4 file `M`
(`FinanceServiceProvider`, `Routes/api.php`, `BillIncomeRequestService`, `PermissionsTableSeeder`)
+ **13 file mới** (2 entity chính · 2 entity morph · 5 service · 2 Resource · 1 Controller ·
1 seeder · 4 FormRequest — tính theo đường dẫn: `Entities/BillPaymentRequest/`,
`Entities/Contract/WarehouseImport|WarehouseExport`, `Services/BillPayment*`,
`Transformers/BillPaymentRequestResource/`, `Http/Controllers/V1/BillPaymentRequestController.php`,
`Http/Requests/BillPaymentRequest/`, `Database/Seeders/BillPaymentRequestPermissionSeeder.php`).
`hrm-client` **chưa đụng gì** (FE bắt đầu từ Phase 5).

**Blocked:** không.

**Chờ user chốt (không chặn):** cột "Khách hàng" ở lưới luôn rỗng với **loại chi 6** (luật ERP đọc
khách hàng, nhưng loại 6 trả tiền cho nhân viên) — đã trả kèm `employee_name` để bật khi user đồng ý.

---

### Checkpoint — 2026-08-15 (PHASE 1 XONG)

**Vừa hoàn thành: TOÀN BỘ Phase 1 (8/8 task).**

| Task | Nội dung | Bằng chứng |
| --- | --- | --- |
| 1.1 | 2 entity morph + morphMap 8→10 | (buổi trước) review sạch |
| 1.2 | 2 entity chính + **vòng sửa 2**: 1 Important + 2 Minor | guest 4 scope → `1 = 0` (trước: `approved` khớp 4.036/4.040) |
| 1.3 | 9 quyền id 1153–1161 + seeder gán role | `9 quyền / 59 dòng role_has`, chạy lại không sinh thêm |
| 1.4 | `BillPaymentDebtService` | **1.035 dòng** đối chiếu SQL thuần, **lệch 0** |
| 1.5 | Service đọc + 2 Resource | 116 phiếu đối chiếu cột tiền theo trạng thái, lệch 0 |
| 1.6 | Controller + 4 route | đúng thứ tự, `/pending`·`/approved` trước `/{id}` |
| 1.7 | Verify HTTP thật | 3 mức quyền, `total` khớp SQL tuyệt đối (4.021 / 3.786 / 0) |
| 1.8 | 3 endpoint popup dùng lại | dùng lại được cả 3; thêm `only_mine` thuần thêm |

**Kết quả nổi bật:**
- Phạm vi quyền chạy đúng qua HTTP: NV36 (tổng công ty) **4.021** = SQL · NV147 (công ty)
  **3.786** = SQL · NV25 (0 quyền) **0** và mở phiếu người khác ra **403**.
- `pending` của NV36 ra 116 chứ không phải 119 vì 3 phiếu status 2 thuộc phòng ban NV36
  không quản lý — nhánh TP duyệt lọc đúng theo `employee_manage_departments`.
- Quyền mới đã gán cho **role 18 Super admin** (thêm so với plan) để FE `checkPermission.js`
  không đá super admin về 404 — đúng bug đã gặp ở màn Đề nghị thu tiền.

**Đang làm dở:** không. Phase 1 khép lại.

**Bước tiếp theo:** Phase 2 theo thứ tự đã chốt ở Ruling #4: **2.1 (FormRequest) → 2.5 (thông báo)
→ 2.2 (service ghi) → 2.3 (duyệt theo cấp) → 2.4 (không duyệt) → 2.6 (controller ghi + verify
vòng đời)**.

**Trạng thái repo (`hrm-api`, nhánh `gop_db`, CHƯA COMMIT — đúng quy tắc dự án):**
- `M Modules/Finance/Providers/FinanceServiceProvider.php`
- `M Modules/Finance/Routes/api.php`
- `M Modules/Finance/Services/BillIncomeRequestService.php` *(thuần thêm `only_mine`)*
- `M Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` *(+9 quyền)*
- `?? Modules/Finance/Entities/BillPaymentRequest/` (2 file) · `?? .../Contract/WarehouseImport.php`
  · `?? .../Contract/WarehouseExport.php`
- `?? Modules/Finance/Services/BillPaymentDebtService.php` · `?? .../BillPaymentRequestService.php`
- `?? Modules/Finance/Transformers/BillPaymentRequestResource/` (2 file)
- `?? Modules/Finance/Http/Controllers/V1/BillPaymentRequestController.php`
- `?? Modules/Finance/Database/Seeders/BillPaymentRequestPermissionSeeder.php`

`hrm-client` **chưa đụng gì** (FE bắt đầu từ Phase 5).

**Blocked:** không.

**Chờ user chốt (không chặn):** cột "Khách hàng" ở lưới **luôn rỗng với loại chi 6** vì luật ERP
đọc khách hàng, trong khi loại 6 trả tiền cho nhân viên (0/429 phiếu có tên KH, 67/429 có tên NV).
Đã giữ hành vi ERP + trả kèm `employee_name` để bật lên được ngay khi user đồng ý.

---

### Checkpoint — 2026-08-14 (cuối buổi)

**Vừa hoàn thành:**
- Brainstorming → spec đầy đủ (user duyệt) → plan 8 phase / 29 task (file này).
- **Task 1.1 — XONG, review sạch** (Spec ✅ / Quality Approved).
  Tạo `Modules/Finance/Entities/Contract/WarehouseImport.php` + `WarehouseExport.php`;
  sửa `Modules/Finance/Providers/FinanceServiceProvider.php` (morphMap 8 → **10** class).
  Verify: `php -l` sạch · tinker count `8887 | 30266` · `MAP OK`. Reviewer query thẳng DB xác nhận
  2 chuỗi morph khớp byte-by-byte + đúng 25/15 dòng.
- **Task 1.2 — CODE XONG, ĐÃ REVIEW: Spec OK / Quality Changes requested (1 Important).**
  Tạo `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php` +
  `BillPaymentRequestDetail.php`.
  Verify của implementer: `php -l` sạch · tinker `TPE.DNTT0825.00001 | details=1 | status=8` ·
  resolve đủ **10** `contractable_type` không exception · `typeForSelect=[1,2,6,12]` · 4 scope build được.

**Đang làm dở:** Task 1.2 đã có kết luận review (về sau khi dừng buổi) — **Spec ✅**, nhưng
**Quality: Changes requested** với **1 finding Important CHƯA SỬA**:

> 🐛 **`searchByFilter()` scope `approved` fail-open khi chưa đăng nhập** —
> `BillPaymentRequest.php:360-368`. `auth()->id()` null thì Laravel đổi `where('manage_approved_id', null)`
> thành `whereNull(...)`, 4 vế `orWhere` thành chuỗi `orWhereNull` ⇒ reviewer đo trên DB thật:
> khớp **4.036/4.040 phiếu** (gần cả bảng). Route có auth middleware nên khó khai thác, nhưng Entity
> là chốt quyền duy nhất theo thiết kế và CLAUDE.md bắt fail-closed; `canView()` đã guard mà
> `searchByFilter()` thì chưa.
> **Cách sửa (1 dòng, đầu hàm):** `if (!$employeeId) { return $query->whereRaw('1 = 0'); }`

Kèm 2 Minor nên sửa cùng lượt: `canEdit()` so lỏng `==` với `auth()->id()` (null == null → true;
hiện DB 0 dòng `created_by` NULL nên chưa khai thác được) · scope `pending` khi user không gắn
`employee_info` thì `$companyId` null → `whereNull('company_id')`.

→ **Việc đầu tiên của buổi sau: sửa 1 Important + 2 Minor này (vòng sửa 2 của Task 1.2), chạy
re-review có phạm vi, rồi mới sang Task 1.3.** KHÔNG cần chạy lại full review Task 1.2.

**Bước tiếp theo (thứ tự đã chốt, xem Rulings bên dưới):**
`review lại 1.2` → 1.3 → 1.4 → 1.5 → 1.6 → 1.7 → **1.8** → 2.1 → **2.5** → 2.2 → 2.3 → 2.4 → 2.6 → Phase 3…

**Trạng thái repo:** `hrm-api` có 4 đường dẫn **CHƯA COMMIT** (đúng quy tắc dự án):
`M Modules/Finance/Providers/FinanceServiceProvider.php` ·
`?? Modules/Finance/Entities/BillPaymentRequest/` (2 file) ·
`?? Modules/Finance/Entities/Contract/WarehouseImport.php` · `?? .../WarehouseExport.php`.
`hrm-client` **sạch**. Cả 2 repo ở nhánh `gop_db`, baseline `3290300ee` / `1f8fd9f38`.

**Blocked:** không.

---

### Rulings đã ra trong buổi (đọc trước khi làm tiếp)

1. **Không tạo git worktree** — làm thẳng trên `gop_db` cả 2 repo (worktree không có symlink `.plans`/`.claude`/`docs`).
2. **Không commit sau mỗi task** — theo quy tắc dự án. Review package dựng từ `git diff` cây làm việc, không dùng dải commit.
3. **Subagent chạy model Fable** (user dặn 2026-08-06).
4. **Đổi thứ tự Phase 2**: `2.1 → 2.5 → 2.2 → 2.3 → 2.4 → 2.6` vì `store()` inject `BillPaymentRequestNotifyService` qua constructor. `BillPaymentAttachmentService` tạo sớm ở 2.2 với 2 method `sync()` + `parse()`; Task 4.1 bổ sung `upload()` / `remove()` + 2 endpoint.
5. **Chạy Task 1.8 TRƯỚC Task 2.1** — 2.1 dựng `allowedContractTypes()` có `InsurancePrincipleForm`, nhưng 1.8 mới quyết định có tạo entity đó không; gọi `getMorphClass()` trên class chưa tồn tại là fatal. `allowedContractTypes()` chỉ liệt kê class ĐÃ tồn tại.
6. 🐛 **LỖI CỦA PLAN đã vá (Critical)** — khối 5 nhánh phạm vi quyền + khối ẩn phiếu nháp trong `searchByFilter()` **chỉ áp khi `$scope === 'all'`**. Bản đầu của plan bảo "giữ y hệt" nên áp cho cả 4 chế độ ⇒ người duyệt không có quyền `Xem tất cả phiếu … của …` rơi vào `created_by = me` ⇒ tab **Chờ duyệt** / **Đã duyệt** rỗng ⇒ luồng duyệt 5 cấp chết im lặng. Đã sửa code **và** sửa plan (Task 1.2 Bước 4). Bằng chứng: nhân viên id 63 (0 quyền) → SQL `pending` = `where company_id = ? and (1 = 0)`, không còn `created_by = ?`.
7. **`allowedContractTypes(2)` / `(6)` CÓ hợp đồng bán HRM là đúng** — spec 5.2/5.3 + quyết định #4 của user.
8. **`BillPaymentRequestDetail::customer()` dùng `App\Models\TpCustomer`** (bám file mẫu thật), không phải class trong snippet minh hoạ của plan.

### Nợ nhỏ ghi sổ (không chặn, xử lý ở task sau cùng feature)

- Docblock `FinanceServiceProvider::registerMorphMap()` mới chỉ nhắc `objectable_type` của màn Đề nghị thu tiền, chưa nhắc `contractable_type` của màn này.
- `WarehouseImport` / `WarehouseExport` không có accessor `getDisplayCodeAttribute()` như `FirmContract` → **đã đưa thành yêu cầu bắt buộc trong brief Task 1.5**: Resource lấy mã hợp đồng theo thứ tự `contract_code` (snapshot) trước, rồi mới `optional($this->contractable)->code`.

---

### Task phụ — Fix conflict rebase `gop_db` (2026-08-15) — [x]

- [x] Gỡ conflict `Modules/Finance/Routes/api.php` — giữ **cả 2** nhóm route (`product-import-requests` + `product-import-direct-transfers` của HEAD và `bill-payment-requests` của commit `f552f1197`); conflict chỉ do 2 nhánh cùng chèn khối route ở cuối file.
- [x] Gỡ conflict `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — **đụng id thật**: cả 2 nhánh cùng lấy dải `1153+`.
  - Giữ **Đề nghị thanh toán = 1153–1161** (đã nằm trên DB `gop_db`, `MAX(id)` guard `api` = 1161, kèm gán role; `BillPaymentRequestPermissionSeeder` + `BillPaymentRequestTestDataSeeder` hard-code dải này).
  - Dời **Yêu cầu nhập hàng → 1162–1168** (7 quyền, chưa có bản guard `api` trên DB; code chỉ tham chiếu theo TÊN qua hằng `ProductImportRequest::PERMISSION_*` nên đổi id không ảnh hưởng).
- [x] Kiểm chứng: `php -l` sạch 2 file · không còn marker · không có id hay cặp (name + guard) trùng mới sinh ra.
- [ ] **Người dùng tự chạy** `git rebase --continue` ở `hrm-api` (dự án cấm AI commit). File đã `git add` sẵn.

**Lưu ý phát sinh:** `php artisan route:list` KHÔNG chạy được trên nhánh này — lỗi có sẵn từ `RequestUpdateTimeSheetController.php:51` gọi `isCurrentEmployeeHasPermission()` lúc boot khi chưa có user (`PermissionHelper.php:23`), không liên quan tới conflict.

---

### Task phụ — Cột Hành động + Tuỳ chỉnh cột màn danh sách (2026-08-18) — @khoipv

Yêu cầu user: bỏ nút **Xem chi tiết** ở cột Hành động, thêm **Cấu hình cột hiển thị**.
Phạm vi: CHỈ `hrm-client/pages/finance/bill-payment-requests/index.vue` (không đụng BE —
`columnCustomizationMixin` lưu qua `human/column-customizations`, bảng key-value, không cần migration).

- [x] Bỏ action `view` khỏi `getRowActions()` + gỡ nhánh `case 'view'` chết trong `handleRowAction()`
      (lối vào chi tiết vẫn còn: `<nuxt-link>` ở cột Mã phiếu)
- [x] Gắn `columnCustomizationMixin` + `columnScreenKey: 'finance_bill_payment_requests'`
- [x] Đổi computed `tableColumns()` → `allColumns()`; thêm `locked: true` cho `index` / `code` / `actions`
- [x] Thêm nút icon `ri-layout-column-line` (`title="Cấu hình cột hiển thị"`) vào slot `#actions`
      + đặt `<ColumnCustomizationModal v-if="columnFieldsLoaded">` cuối template
- [x] `mounted()`: `await Promise.all([this.loadColumnFields(), this.loadData()])`
- [x] Verify: compile template + kiểm tra không còn tham chiếu `tableColumns` cũ

**Ghi nhận:** BE không phải sửa gì — `ColumnCustomizationService::normalizeScreenKey()` nhận mọi
khoá khớp `[a-z0-9_]{1,100}`, dữ liệu vào bảng key-value `user_column_settings` (1 dòng / user / màn).
Đã kiểm chứng: `vue-template-compiler` + `@babel/parser` parse sạch file `index.vue`.
**Chưa kiểm chứng trên trình duyệt** (user tự test): popup cấu hình, kéo thả thứ tự, cột ẩn/hiện sau F5.

### Task phụ — Thêm cột Người / Ngày cập nhật vào bảng tuỳ chỉnh cột (2026-08-18) — @khoipv

Yêu cầu user: bổ sung 2 cột **Ngày cập nhật** + **Người cập nhật** cho màn danh sách ĐNTT.
`BillPaymentRequestListResource` chưa trả 2 field này ⇒ phải sửa cả BE, không chỉ FE.

- [x] Entity `BillPaymentRequest`: thêm quan hệ `employee_update()` (`belongsTo Employee, updated_by`)
- [x] Entity `applySort()`: whitelist thêm `updatedAt` / `updated_at` → cột `updated_at`
      (không thêm thì bật `sortable` ở FE là bấm không ăn)
- [x] `BillPaymentRequestService::searchByFilter()`: eager-load thêm `employee_update.info` (chống N+1)
- [x] `BillPaymentRequestListResource`: trả `updated_by_name` + `updated_at` (`d/m/Y H:i`)
- [x] FE `index.vue`: thêm 2 cột vào `allColumns` (trước cột Trạng thái, mặc định HIỆN,
      `updatedAt` có `sortable`) + 2 template cell
- [x] Verify

**Kiểm chứng (chạy thật trên DB `gop_db`):**
- Dữ liệu: `SELECT COUNT(*) … FROM bill_payment_requests` → **4.051/4.051** dòng có `updated_by`
  trỏ đúng `employees` và `updated_at` khác NULL — 0 dòng rỗng, 0 dòng mồ côi.
- Gọi thẳng Service + Resource với `sort_by=updatedAt`: SQL ra
  `… order by \`updated_at\` desc limit 5` ✅, dữ liệu trả về đúng
  (`updated_at='27/07/2026 17:40'`, `updated_by_name='Nguyễn Thị Ngọc Hà'`).
- Không N+1: `per_page=5` và `per_page=50` cùng ra **13 query** (lần chạy đầu 27 là do warm-up config/permission).
- `php -l` sạch 3 file BE · `vue-template-compiler` + `@babel/parser` parse sạch `index.vue`.
- **Chưa kiểm chứng trên trình duyệt** (user tự test): 2 cột hiện đúng chỗ, bấm sort cột Ngày cập nhật,
  tắt/bật 2 cột ở popup Cấu hình cột.

### Task phụ — Đồng bộ định dạng cột ngày ở lưới (2026-08-18) — @khoipv

Yêu cầu user: format lại **Ngày lập** + **Ngày nhận** cho khớp Ngày cập nhật → cả 3 cột ngày
của lưới dùng `d/m/Y H:i`.

- [x] `BillPaymentRequestListResource`: `created_at` và `manage_approved_time` → `d/m/Y H:i`
- [x] FE `index.vue`: nới `createdAt` + `manageApprovedTime` từ 110px → **140px** (110px là xuống dòng)
- [x] Verify

**Kiểm chứng:**
- Kiểu cột: `created_at` = `timestamp`, `manage_approved_time` = `datetime` → giờ:phút là dữ liệu
  THẬT, **0/4.051 dòng** rơi vào `00:00:00` (không phải giờ độn thêm).
- `manage_approved_time` NULL ở **44/4.051** phiếu (chưa qua TP duyệt) → FE vẫn hiện `—`.
- Chạy thật Service + Resource: `lap='27/07/2026 10:49' · nhan='27/07/2026 10:55' · capnhat='27/07/2026 17:40'`.
- `BillPaymentRequestListResource` chỉ có **1 nơi dùng** (`BillPaymentRequestController:389`) → không
  ảnh hưởng màn chi tiết / in / xuất Excel (`BillPaymentRequestExport` là class riêng).
- `php -l` sạch · `vue-template-compiler` + `@babel/parser` parse sạch.
- **Chưa kiểm chứng trên trình duyệt** (user tự test): 3 cột ngày không xuống dòng ở 140px.

### Task phụ — Việt hoá thông báo Select2 của ô lọc KH / NCC (2026-08-18) — @khoipv

Yêu cầu user: ô lọc Khách hàng / Nhà cung cấp hiện "Please enter 2 or more characters" (text mặc
định của Select2) → đổi sang tiếng Việt.

Nguồn: `components/V2BaseSelectRemote.vue` **không truyền `language`** cho Select2, trong khi
`V2BaseSelect.vue` đã có sẵn khối Việt hoá. **File dùng chung 18 màn** → đã hỏi và
**user chốt 2026-08-18: sửa thẳng component chung** để toàn hệ thống nhất quán.

- [x] Thêm computed `select2Language` vào `V2BaseSelectRemote.vue` — copy ĐÚNG bộ chữ của
      `V2BaseSelect.vue` (`noResults` / `searching` / `inputTooShort` / `inputTooLong` /
      `maximumSelected` / `loadingMore` / `errorLoading`) để 2 kiểu select trên cùng màn không lệch giọng
- [x] Truyền `language: this.select2Language` vào `settings` lúc khởi tạo Select2
- [x] Verify

**Kiểm chứng:**
- Chỉ đổi CHỮ hiển thị — `minimumInputLength`, `ajax`, `dropdownParent` và mọi hành vi khác giữ nguyên.
- Màn ĐNTT truyền `:minimum-input-length="2"` cho cả 2 ô ⇒ chưa gõ gì thì hiện
  **"Vui lòng nhập thêm 2 ký tự"**.
- `vue-template-compiler` + `@babel/parser` parse sạch component.
- **Chưa kiểm chứng trên trình duyệt** (user tự test): gõ 1 ký tự vào ô KH/NCC xem câu tiếng Việt,
  và soát nhanh 17 màn còn lại dùng `V2BaseSelectRemote` (Báo giá, Hợp đồng, Yêu cầu nhập hàng,
  Đề nghị thu tiền…) — chỉ đổi chữ nên không kỳ vọng lệch gì.

### Task phụ — Điều tra "lọc KH không ra MEXMON" + đổi tiêu đề cột (2026-08-18) — @khoipv

User báo: phiếu `TPE.DNTT0726.00256` hiện "MEXMON - MEXMON TECHNOLOGIES" ở cột **Khách hàng**,
nhưng gõ `MEXMON` vào ô lọc Khách hàng thì không ra.

**KẾT LUẬN: KHÔNG phải lỗi code — bộ lọc chạy đúng.** MEXMON là **nhà cung cấp**:

| Bằng chứng (đo trên DB `gop_db`) | Kết quả |
| --- | --- |
| `customers.id = 40745` (MEXMON TECHNOLOGIES) | `is_customer = 0` · `is_supplier = 1` |
| Phiếu `TPE.DNTT0726.00256` (id 4179) | `type = 1` (Chi trả NCC) · `supplier_id = 40745` · `customer_id = NULL` |
| SQL của `assign/customers/search` (`CustomerService::searchForSelect2` → `index()`) | có `where customers.is_customer = ?` bind `1` |
| Bảng `suppliers` | **0 dòng** — KH và NCC nằm chung bảng `customers`, phân biệt bằng 2 cờ trên |

Chạy thật: ô **Khách hàng** q=MEXMON → **0** kết quả · ô **Nhà cung cấp** q=MEXMON → **1** kết quả (id 40745)
· lọc `supplier_id=40745` → **10 phiếu, có 00256** ✅ · lọc `customer_id=40745` → 0 phiếu.

**Nguồn gây hiểu nhầm (đã sửa):** cột `objectName` đặt tiêu đề "Khách hàng" nhưng nội dung là KH
**hoặc** NCC tuỳ loại chi (loại 1 và 12 luôn là NCC — đúng luật `objectName()` port từ ERP).

- [x] Đổi tiêu đề cột `objectName` → **"Khách hàng / Nhà cung cấp"** (bằng màn Đề nghị thu tiền).
      User chốt 2026-08-18. CHỈ đổi chữ tiêu đề — dữ liệu, `objectName()` và 2 ô lọc giữ nguyên.
- [x] Verify: `vue-template-compiler` + `@babel/parser` parse sạch.
- [ ] **Chưa kiểm chứng trên trình duyệt** (user tự test): tiêu đề cột mới hiện đúng cả trên lưới
      lẫn trong popup Cấu hình cột.

**Không làm** (user không chọn): gộp 2 ô lọc KH + NCC thành 1 ô tìm cả hai — phải sửa BE và lệch
khỏi cả ERP lẫn màn Đề nghị thu tiền.

### Task phụ — Sửa sắp xếp cột lưới (2026-08-18) — @khoipv

Yêu cầu user: bỏ sort 2 cột **Loại chi** + **Hình thức TT**, bổ sung sort cột
**Khách hàng / Nhà cung cấp**.

🐛 **Phát hiện khi làm: 3 cột đang bật `sortable` mà bấm KHÔNG ăn.** `V2BaseDataTable` emit đúng
`column.key`, nhưng whitelist `applySort()` lại khai theo tên khác:

| FE gửi (`key` cột) | Map BE có | Kết quả trước khi sửa |
| --- | --- | --- |
| `typeName` | `type` | ❌ rơi về `order by created_at desc` |
| `typePaymentName` | `typePayment` | ❌ rơi về `order by created_at desc` |
| `requestStatus` | `status` | ❌ rơi về `order by created_at desc` |
| `code` · `createdAt` · `updatedAt` | khớp | ✅ |

- [x] FE: bỏ `sortable` khỏi `typeName` + `typePaymentName`; BE: bỏ luôn `type` / `typePayment`
      khỏi map (hết nơi dùng)
- [x] BE: thêm `requestStatus => status` — cột Trạng thái vốn hiện mũi tên sort mà bấm không đổi gì
      (**ngoài yêu cầu user, nhưng cùng đúng một lỗi map, sửa 1 dòng**)
- [x] BE: thêm `applyObjectNameSort()` — dựng lại đúng 5 nhánh của `objectName()` bằng SQL
- [x] FE: bật `sortable` cho cột `objectName`
- [x] Verify

**2 cách viết đã thử và LOẠI (ghi trong docblock để không ai dọn ngược):**
1. `LEFT JOIN` thẳng bảng chi tiết + `customers` → nổ
   `SQLSTATE[23000] Column 'created_by' in where clause is ambiguous` — `searchByFilter()` lọc bằng
   tên cột trần, mà `customers` cũng có `created_by`.
2. Subquery tương quan trong `ORDER BY` → chạy đúng nhưng **14,2 giây**:
   `bill_payment_request_details` **chỉ có index PRIMARY**, không có index trên
   `bill_payment_request_id` ⇒ 8.216 dòng bị quét lại cho từng phiếu trong 4.051 phiếu.

**Cách đang dùng:** derived table quét bảng chi tiết đúng 1 lần rồi join theo phiếu — **0,046s**
(nhanh ~300 lần), và chỉ lộ 3 cột đặt tên riêng nên không đụng tên cột nào của phiếu.

**Kiểm chứng:**
- Thứ tự SQL khớp giá trị Resource hiển thị trên **toàn bộ 4.051 phiếu** — hỏi lại chính MySQL:
  **0 cặp liền kề sai thứ tự** theo collation `utf8mb4_unicode_ci` của cột. (So bằng `strcmp` của
  PHP thì thấy "lệch" 18 dòng dạng `CỒNG TY` vs `CÔNG TY` — đó là byte-order của PHP, không phải
  lỗi; MySQL sắp theo kiểu tiếng Việt mới là thứ tự người dùng mong đợi.)
- Chạy kèm bộ lọc (`supplier_id`, `customer_id`, `status`, khoảng tiền, mã phiếu) và cả **4 chế độ**
  (`all`/`mine`/`pending`/`approved`): không nhánh nào vỡ.
- Sort toàn tập 4.051 phiếu: **0,52s**; 1 trang 6 dòng: **0,06–0,12s**.
- 430 phiếu có ô này rỗng (377 loại 6 TM + 53 loại 2/6 CK) dồn lên đầu khi sắp A→Z — đúng kiểu quen thuộc.
- `php -l` sạch · `vue-template-compiler` + `@babel/parser` parse sạch.
- **Chưa kiểm chứng trên trình duyệt** (user tự test): bấm mũi tên sort trên cột KH/NCC và cột
  Trạng thái, xác nhận 2 cột Loại chi / Hình thức TT không còn hiện mũi tên.

**Nợ ghi sổ (không chặn):** `bill_payment_request_details` thiếu index trên `bill_payment_request_id`
— bảng dùng chung 2 cổng ERP+HRM nên KHÔNG tự thêm; nếu sau này cần tối ưu thì hỏi user trước.

---

### Checkpoint — 2026-08-18 (đợt sửa UI màn danh sách — **HOÀN THÀNH, ĐÃ COMMIT**)

**Vừa hoàn thành:** 6 việc user yêu cầu trong buổi, tất cả ở màn danh sách
`/finance/bill-payment-requests` (5 task phụ ghi ở trên):

1. Bỏ nút "Xem chi tiết" cột Hành động + gỡ nhánh `case 'view'` chết.
2. Popup **Cấu hình cột hiển thị** — `columnCustomizationMixin`, khoá `finance_bill_payment_requests`,
   khoá `locked` 3 cột (STT · Mã phiếu · Hành động). **BE không phải sửa gì**
   (`ColumnCustomizationService` nhận mọi khoá `[a-z0-9_]{1,100}`, lưu ở `user_column_settings`).
3. 2 cột **Người / Ngày cập nhật** — BE thêm quan hệ `employee_update()`, eager-load
   `employee_update.info`, Resource trả `updated_by_name` + `updated_at`.
4. 3 cột ngày về chung `d/m/Y H:i` + nới 140px.
5. Tiêu đề cột `objectName` → **"Khách hàng / Nhà cung cấp"**.
6. Sắp xếp: bỏ sort Loại chi + Hình thức TT · thêm sort cột KH/NCC (`applyObjectNameSort()`)
   · sửa map cho cột Trạng thái (lỗi có sẵn).

Ngoài ra sửa **1 file dùng chung** (user chốt): `components/V2BaseSelectRemote.vue` — Việt hoá
thông báo Select2, ảnh hưởng 18 màn, chỉ đổi chữ.

**File đã đụng (user đã tự commit 2026-08-18: `hrm-api` `decc26df7` · `hrm-client` `ba4518877`):**
- `hrm-api`: `Modules/Finance/Entities/BillPaymentRequest/BillPaymentRequest.php` ·
  `Modules/Finance/Services/BillPaymentRequestService.php` ·
  `Modules/Finance/Transformers/BillPaymentRequestResource/BillPaymentRequestListResource.php`
- `hrm-client`: `pages/finance/bill-payment-requests/index.vue` · `components/V2BaseSelectRemote.vue`

**Đang làm dở:** không.

**User đã test trình duyệt 2026-08-18 — ĐẠT đủ 6 điểm:**
(a) cột Hành động không còn "Xem chi tiết", link Mã phiếu vẫn vào chi tiết ·
(b) popup Cấu hình cột: tắt/bật cột, kéo đổi thứ tự, F5 giữ nguyên ·
(c) 2 cột Người / Ngày cập nhật hiện đúng chỗ ·
(d) 3 cột ngày hiện `dd/mm/yyyy hh:mm`, không xuống dòng ở 140px ·
(e) sort cột KH/NCC + cột Trạng thái ăn thật, 2 cột Loại chi / Hình thức TT hết mũi tên ·
(f) ô lọc KH/NCC báo "Vui lòng nhập thêm 2 ký tự".
User tự commit cả 2 repo (Claude không commit): `hrm-api` `decc26df7` · `hrm-client` `ba4518877`
— cả 2 cây làm việc sạch, đúng 5 file ở trên.

**Blocked:** không.

**Bước tiếp theo:** không còn việc của đợt này. **Feature đóng ở trạng thái HOÀN THÀNH.**
Còn nợ (không chặn, để đợt sau nếu user yêu cầu): SRS / testcase / HDSD cho màn này ·
chưa đối chiếu trực tiếp giao diện ERP · index cho `bill_payment_request_details`
(bảng dùng chung 2 cổng, phải hỏi user) · dọn dữ liệu test còn sót trên DB local
(`employee_manage_departments` id 368 · `departments.id = 111` · 8 phiếu `TEST.DNTT-CHI.*`).

### Task phụ — Lưu nháp không bắt buộc bảng chi tiết + file đính kèm (2026-08-22) — @khoipv
User chốt: nút **Lưu nháp** (`status = 1`) chỉ để cất dở dang → bỏ bắt buộc **bảng chi tiết** và
**file đính kèm**. Nút **Lưu và gửi duyệt** (`status = 2`) giữ nguyên ràng buộc cũ.
Cùng cách đã làm ở màn Đề nghị thu tiền (`finance-bill-income-request` Task 8.5).

- [x] `BillPaymentRequestStoreRequest::rules()` (UpdateRequest kế thừa nên có luôn): thêm cờ
      `$isDraft`; `details` → `nullable|array` khi nháp; `attachment_urls` bỏ nhánh `required`
      khi nháp (nhánh "loại chi 1 bắt buộc file" chỉ còn hiệu lực lúc gửi duyệt).
- [x] Dòng chi tiết **đã thêm** vẫn phải đủ hợp đồng + số tiền — nới nốt phần đó chỉ đẻ dòng rác.
- [x] FE **không phải sửa**: `save()` chỉ chạy vee-validate (rule định dạng), required do BE quyết
      theo `status` (`BillPaymentRequestForm.vue:1336`).
- [x] Không có rủi ro cột NOT NULL như `reason` ở Task 8.5: `bill_payment_requests.attachments` là
      `text NULL`, `uploadAttachments()` trả `null` khi không có file, `syncDetails()` chạy bình
      thường với mảng rỗng.
- [x] Verify ma trận rule (Validator thật, loại chi 1 + chuyển khoản — nhánh DUY NHẤT bắt buộc file):
      · nháp, không chi tiết, không file → **PASS**
      · nháp, có chi tiết, không file → **PASS**
      · gửi duyệt, không chi tiết, không file → FAIL đúng 2 khoá `details`, `attachment_urls`
      · gửi duyệt, có chi tiết, không file → FAIL `attachment_urls`
      · gửi duyệt, đủ cả 2 → PASS
      · nháp, dòng chi tiết thiếu tiền/hợp đồng → vẫn FAIL 3 khoá cấp dòng
- [x] Verify SQL thật: gọi `store()` với `details = []`, `attachment_urls = []` → tạo được phiếu
      (`status = 1`, `attachments = NULL`, 0 dòng chi tiết). Chạy trong transaction rồi `rollBack()`
      — số phiếu trước/sau đều 4.052, không để lại dữ liệu rác. `php -l` sạch.
- [ ] User mở trình duyệt xác nhận.

### Task phụ — Loại chi 6 (Chi thưởng HĐ) + CK: bỏ ô Nhân viên, tự đổ ngân hàng người lập (2026-08-22) — @khoipv
User báo 2 điểm lệch ERP ở màn `create` khi chọn **Chi thưởng thực hiện hợp đồng** + **CK**:
(1) tự dưng có ô "Nhân viên nhận tiền"; (2) khối Thông tin ngân hàng trống trơn.

Đối chiếu ERP (`resources/views/income_expenditure/bill_payment_requests/` +
`partials/classes/IncomeExpenditure/BillPaymentRequest.blade.php`):
- Ô **Nhân viên** chỉ hiện ở nhánh `type_employee_transfer` = **loại chi 10 + đối tượng Nhân viên**
  (`form.blade.php:167`). Loại 6 là `type_employee_has_contract` (:142) — KHÔNG có ô này.
- Khối ngân hàng hiện cho `type_employee_has_contract_transfer` (`form.blade.php:372`) và dữ liệu do
  `changeForm()` tự nạp: `addInfoEmployee({id: creator_id})` (:322-326) → `formJs.blade.php:89-117`
  đổ `employee_id/name/code` + `account_number`, `account_name`, `bank_name`, `bank_branch`,
  `bank_province` từ `employee_infos` của **NGƯỜI LẬP PHIẾU**. Các ô đều CHỈ ĐỌC (ERP in ra text).

- [x] BE `BillPaymentRequestService::currentEmployeeInfo()`: `meta.creator` trả thêm `employee_id`,
      `employee_code` và 6 trường ngân hàng của người lập. Gộp vào meta sẵn có thay vì thêm endpoint —
      màn form đã gọi API danh sách 1 lần lúc mở.
      ⚠️ Cột tỉnh của `employee_infos` tên là **`bank_province`** (id), không phải `bank_province_id`
      như bảng `customers`; tên tỉnh join `provinces`.
- [x] FE `BillPaymentRequestForm.vue`: bỏ ô "Nhân viên nhận tiền"; thêm `creatorInfo` vào data và
      `applyCreatorBankInfo()` — gọi NGAY SAU `clearInfoBank()` ở cả 2 nhánh của `askResetForm()`
      (đổi loại chi / đổi hình thức) và 1 lần lúc `loadOptions()` xong ở màn Tạo. Điền trước
      `clearInfoBank()` là bị xoá trắng.
- [x] Verify BE: `meta()` của nhân viên id 13 trả đủ 6 trường, khớp `employee_infos`
      (`010999888765` · Vietcombank · Thành Công · tỉnh id 1 → "Thành phố Hồ Chí Minh").
- [x] Verify FE trên trình duyệt thật (localhost:3000, đi qua đúng `onTypeChange` + `onTypePaymentChange`):
      không còn nhãn "Nhân viên nhận tiền"; khối ngân hàng hiện và **đã điền** — ô trên màn hình đọc ra
      `010999888765`, `Vietcombank`, `Thành Công`, `Thành phố Hồ Chí Minh`; `employee_id = 13`.
      Template + script parse sạch, `php -l` sạch.
- [x] **Bổ sung sau khi user hỏi lại (2026-08-22):** khối ngân hàng cũng **bỏ bắt buộc khi Lưu nháp**,
      giữ nguyên khi Gửi duyệt (user chọn phương án 2).
      Đối chiếu trước khi sửa: ERP **CÓ** bắt buộc 6 trường này cho nhánh `type_employee_has_contract_transfer`
      (`erp/.../BillPaymentRequestStoreRequest.php:83-89`, rule không xét trạng thái) — HRM trước đó đã
      port đúng. Lý do vẫn nới: các ô CHỈ ĐỌC, giá trị tự nạp từ hồ sơ, người dùng không có cách nào
      tự điền để cất phiếu dở dang.
      Sửa: thêm `!$isDraft &&` vào `requiredIf` của `account_number`, `account_name`, `bank_name`,
      `bank_branch`, `bank_province_id`, `bank_province_name`, `bank_id`, `swift_code`, `cost`.
      Verify ma trận (Validator thật): loại 6 + CK nháp trống trơn → **PASS** · gửi duyệt thiếu ngân
      hàng → FAIL đúng 6 khoá · gửi duyệt đủ → PASS · NCC nước ngoài nháp trống → PASS · NCC nước
      ngoài gửi duyệt thiếu → FAIL `account_*`, `bank_id`, `swift_code`, `cost`. `php -l` sạch.
- [ ] User mở trình duyệt xác nhận.

**Lưu ý dữ liệu (không phải lỗi code):** chỉ **127/1.101** hồ sơ `employee_infos` có số tài khoản.
Người lập chưa khai ngân hàng thì khối này vẫn trống và gửi duyệt sẽ bị 422 (`account_name`… required)
— ERP y hệt: ô chỉ đọc, sửa bằng cách cập nhật hồ sơ nhân sự. Tài khoản test id 13 đang thiếu đúng ô
"Tên tài khoản" nên ô đó trống.

### Task phụ — Loại chi 6: không bắt chọn khách hàng trước, port nguồn hợp đồng `payment_TTHHD` (2026-08-22) — @khoipv
User báo: ERP không bắt chọn khách hàng rồi mới chọn hợp đồng, HRM lại bắt. Đúng — và sai tới 2 tầng.

**ERP** (`BillPaymentRequestDetail.blade.php:546-553`): cả 2 điều kiện "Chưa chọn khách hàng" đều có
`&& this.parent.type != 6` → loại 6 được MIỄN ở cả TM lẫn CK. Thay vào đó popup đổi nguồn sang
`type = 'payment_TTHHD'` và có thêm **cột + ô lọc Khách hàng** (`:576-594`).

**HRM sai:**
1. `BillPaymentRequestDetailTable.vue::contractPickerReady()` xét nhánh CK trước
   (`if (!this.isCash) return !!this.partyId`) — loại 6 không có đối tượng cấp phiếu nên `partyId`
   luôn rỗng → ô hợp đồng khoá vĩnh viễn. Dòng `return true` cho loại 6 nằm dưới, không bao giờ chạy tới.
2. Chưa port nguồn `payment_TTHHD` — loại 6 đang dùng chung `search-contracts` (lọc `customer_id`,
   BE trả 422 nếu thiếu) nên kể cả gỡ khoá thì popup vẫn rỗng.

- [x] BE `BillPaymentRequestService::searchBonusContracts()` — port nguyên nhánh `payment_TTHHD`
      (`SearchContractService.php:154`, `:331-360`, `:451-456`): UNION 3 nguồn — `firm_contracts`
      (id thuộc bút toán TK **3351** + vụ việc **TTHHD** + `employee_id` = người lập, HOẶC
      `firm_support_accounting_employees` của mình / phòng mình làm trưởng phòng; `status NOT IN
      (1,2,4,5)`, `type IN (1,4,7,8)`) · `wr_service_contracts` (tương tự với `wr_support_accounting_*`,
      `status NOT IN (0,1,2)`, `type IN (1,2)`) · `opening_contracts` (`created_by` = người lập).
      Fail-closed: thiếu người đăng nhập / TK 3351 / vụ việc TTHHD → trả paginator RỖNG, không bao
      giờ liệt kê mọi hợp đồng.
      **Số tiền còn lại** = SUM(Có) − SUM(Nợ) TK 3351 lọc vụ việc TTHHD + người lập, port
      `AccountDetail::getDataForBillPaymentRequest(3351, ...)` đúng bộ tham số form ERP gửi cho loại 6.
      ⚠️ Nguồn HĐ bán ở nhánh này là **`firm_contracts`** chứ KHÔNG phải `hrm_contracts`: 23.111 dòng
      `account_details` TK 3351/TTHHD và 22.312 dòng `firm_support_accounting_employees` đều trỏ
      `App\Model\Sale\Firm\Contract\FirmContract`; `hrm_contracts` (42 dòng, toàn HĐ seed) không có
      bút toán nào → lấy nguồn đó là popup luôn rỗng. Morph string trùng chuỗi ERP nên 2 cổng đọc được nhau.
- [x] BE route `GET /bill-payment-requests/bonus-contracts` + `bonusContracts()` (payload cùng khuôn
      với 2 popup hợp đồng của màn thu tiền để dùng lại `ContractSearchModal`).
- [x] BE `BillPaymentRequest::allowedContractTypes(6)` — thêm `WrServiceContract` (ERP union cả nguồn
      này; thiếu class thì dòng chọn từ đó lưu sẽ 422).
- [x] FE `ContractSearchModal.vue` — thêm prop **`bonusMode`** (thuần thêm): đổi endpoint, bỏ điều kiện
      phải có `objectId`, hiện cột **Khách hàng** + ô lọc khách hàng, đổi nhãn cột tiền thành
      "Số tiền còn lại", ẩn cột "Giá trị hợp đồng" (ERP cũng không có). Không truyền cờ → màn Đề nghị
      thu tiền chạy y như cũ.
- [x] FE `contractPickerReady()` — loại 6 trả `true` TRƯỚC nhánh CK; `BillPaymentRequestForm.vue`
      truyền `:bonus-mode="isBonus"`.
- [x] KHÔNG chặn hợp đồng còn lại = 0: ERP cố ý bỏ (`FirmContract.php:1662-1667`, đoạn chặn đã comment,
      luôn `return [true, ...]` cho loại 6).
- [x] Verify BE trên dữ liệu thật: nhân viên id 331 (có bút toán TTHHD) → **712 hợp đồng**; lọc theo mã
      → 327; lọc theo `customer_id` → 3. Nhân viên id 25 (không quyền thưởng) → **2** (chỉ HĐ đầu kỳ do
      mình tạo, đúng ERP). Đối chiếu số tiền: HĐ `HĐDA_TPE_HN_DA_25_0105_...` của nhân viên 781 →
      **730.190.015**, khớp đúng SQL tổng hợp TK 3351.
- [x] Verify FE trên trình duyệt (localhost:3000, loại chi 6 + CK): ô hợp đồng mở được ngay
      (`contractPickerReady = true`), popup gọi `bonus-contracts`, cột đúng thứ tự ERP
      `STT | Số đơn hàng/Hợp đồng | Khách hàng | Ngày lập | Số tiền còn lại`, 12 dòng cho tài khoản
      đang đăng nhập; bấm chọn → dòng chi tiết nhận `contract_code`, `contractable_id = 2655`,
      `contractable_type = App\Model\Accounting\OpeningContract` (nằm trong whitelist loại 6).
      `php -l` 4 file + parse 3 file FE đều sạch.
- [ ] User mở trình duyệt xác nhận.

### Task phụ — Bỏ dấu (*) ở khối Thông tin ngân hàng (2026-08-22) — @khoipv
User chốt: bỏ dấu sao cho đồng nhất ERP. Đối chiếu `form.blade.php`: trong khối ngân hàng, ERP chỉ
để `required-label` ở **2 ô CHỌN ĐƯỢC** — "Ngân hàng" (`:234`) và "Phí" (`:203`); mọi dòng thông tin
tài khoản đều là `<b class="form-label">`, không dấu sao.

- [x] `BankInfoSection.vue`: bỏ `<Required />` ở **5 dòng nhánh trong nước** (Số tài khoản / Tên tài
      khoản / Tên ngân hàng / Chi nhánh / Thành phố) và **6 dòng nhánh NCC nước ngoài**; bỏ luôn cờ
      `required: true` trong `foreignFields` (không còn chỗ nào đọc).
- [x] GIỮ dấu sao ở "Ngân hàng" (select) và "Phí" — ERP có, và đây là 2 ô người dùng thật sự chọn.
- [x] Chỉ đổi hiển thị: BE vẫn bắt buộc khi **Gửi duyệt**, bỏ bắt buộc khi **Lưu nháp** (task trên).
- [x] Verify trên trình duyệt (loại chi 6 + CK): nhãn khối ngân hàng đọc ra
      `Số tài khoản · Tên tài khoản · Tên ngân hàng · Chi nhánh · Thành phố` — **0 nhãn còn dấu sao**.
      Parse template + script sạch.
- [ ] User xác nhận.


### Checkpoint — 2026-08-22 (đợt sửa theo phản hồi user)
Vừa hoàn thành: **5 task phụ** (nhánh `gop_db`, chưa commit).
· Lưu nháp không bắt buộc **bảng chi tiết + file đính kèm** (rule động theo `status`).
· Lưu nháp cũng không bắt buộc **khối ngân hàng** (9 trường) — user chọn phương án 2; ERP thực tế
  CÓ bắt (`BillPaymentRequestStoreRequest.php:83-89`), ta cố ý nới vì các ô này chỉ đọc.
· Loại chi 6 + CK: **bỏ ô "Nhân viên nhận tiền"** (ERP không có) và **tự đổ ngân hàng của người lập**
  qua `meta.creator` (port `addInfoEmployee({id: creator_id})`).
· Loại chi 6: **không bắt chọn khách hàng trước** + port nguồn hợp đồng `payment_TTHHD`
  (endpoint mới `bonus-contracts`, popup thêm cột/ô lọc Khách hàng, `bonusMode` thuần thêm).
· Khối ngân hàng **bỏ dấu (*)** ở các dòng thông tin tài khoản, giữ ở "Ngân hàng" + "Phí" như ERP.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt xác nhận cả 5 việc.
Blocked: không. Lưu ý: nguồn HĐ bán của nhánh loại 6 là `firm_contracts` (ERP) chứ không phải
`hrm_contracts` — lý do + số liệu ghi trong task tương ứng.

### Task phụ — "Chọn NCC rồi mà không lấy thông tin ngân hàng" (2026-08-22) — @khoipv
User báo loại chi 1 + CK, chọn NCC xong khối ngân hàng vẫn trống.

**Điều tra (đo trên trình duyệt + DB):** luồng KHÔNG hỏng — `applyParty()` → `loadPartyBanks()` →
`party-banks` trả đủ dữ liệu; NCC `29TPHPTH-1` đổ đúng `0531188050005 · MB · Long Biên · Hà Nội`.
Ba thứ khiến nhìn như hỏng:
1. **API mất ~2,5-2,8 giây** mà khối ngân hàng đứng im không báo gì. Đo thêm: `currencies` 2,47s,
   danh sách phiếu 2,47s → **overhead chung của môi trường local**, không phải endpoint này chậm
   (SQL của nó chỉ **17ms**: customers 16ms + supplier_banks 1ms + provinces 1ms).
2. **NCC nước ngoài** (`customer_type = 3`) đi nhánh khác: phải tự chọn ngân hàng trong dropdown
   (ERP y hệt — `formJs.blade.php:129-131` chỉ nạp danh sách `is_main`, không tự điền). NCC chưa khai
   tài khoản thì dropdown rỗng và **không có dòng nhắc nào** (nhánh trong nước đã có sẵn).
3. Dữ liệu mỏng: **880/9.547 NCC** có số tài khoản; 463 NCC nước ngoài trong khi cả bảng
   `supplier_banks` chỉ có 380 dòng.

- [x] `BankInfoSection.vue`: thêm prop `loading` + chỉ báo "Đang lấy thông tin ngân hàng của đối
      tượng nhận tiền..." (b-spinner), thay cho khối đứng trống ~2,5s.
- [x] `BankInfoSection.vue`: thêm dòng nhắc cho **nhánh NCC nước ngoài** khi chưa khai tài khoản nào.
- [x] `BillPaymentRequestForm.vue`: state `partyBanksLoading` (bật/tắt quanh `loadPartyBanks`) + toast
      lỗi khi API hỏng (trước đây chỉ `console.error`, người dùng không biết gì).
- [x] Verify trên trình duyệt, 3 tình huống: NCC trong nước có ngân hàng → chỉ báo hiện rồi đổ đúng
      STK · NCC trong nước không có STK → chỉ báo + dòng nhắc cũ · NCC nước ngoài chưa khai bank →
      chỉ báo + **dòng nhắc mới**. Parse 2 file FE sạch.
- [x] User cho biết NCC: `43TPHPAN-58 — KHÁCH HÀNG TEST` (id 232389 trên DB dev) → **tìm ra bug thật**,
      xem task ngay dưới.

### Task phụ — `party-banks` đọc SAI nguồn tài khoản ngân hàng (2026-08-22) — @khoipv
Truy tiếp ca `43TPHPAN-58`: hồ sơ khách hàng bên ERP **có 2 tài khoản** (`900811 – test nè`,
`1515 – test tiếp nè`) khai ở khối "Tài khoản cá nhân" → bảng **`customer_has_bank_accounts`**
(quan hệ ERP `Customer::customer_accounts()`, `Customer.php:460-463`). HRM `party-banks` chỉ đọc mấy
cột `account_number/account_name/bank_name/bank_branch/bank_province_id` nằm thẳng trên `customers`
(đều NULL với khách hàng này) + `supplier_banks` (0 dòng) → trả rỗng.

Đo mức ảnh hưởng trên DB: **880** NCC có dữ liệu ở cột cũ · **335** NCC có ở
`customer_has_bank_accounts` · **215 NCC chỉ có ở bảng mới** → 215 NCC này đang ra trắng.

- [x] BE `partyBanks()`: query thêm `customer_has_bank_accounts` (join `provinces` lấy tên tỉnh),
      trả về khoá mới `accounts`. Giữ nguyên `info` (cột cũ) và `banks` (NCC nước ngoài).
- [x] FE `BillPaymentRequestForm.vue`: state `partyAccounts` + `selectedAccountId`;
      `loadPartyBanks()` ưu tiên `accounts` — có thì đổ tài khoản đầu, không có mới rơi về `info`;
      thêm `applyPartyAccount()` + `onPartyAccountChange()`.
- [x] FE `BankInfoSection.vue`: props `accounts` / `selectedAccountId`; đối tượng có **>1 tài khoản**
      thì hiện dropdown "Tài khoản ngân hàng" (`Chủ TK - Số TK - Ngân hàng`) để đổi.
      ⚠️ Khác ERP có chủ đích (user chốt phương án 1): ERP `addInfoCustomer()` chỉ tự điền khi có
      ĐÚNG 1 tài khoản, từ 2 trở lên bỏ trống luôn và không cho chọn — đúng ca của user (2 tài khoản)
      nên port y nguyên thì vẫn trắng.
- [x] Verify trên trình duyệt, 5 ca: NCC 2 tài khoản + cột cũ rỗng (đúng dạng ca user) → đổ
      `020101268668 · Sacombank · Hà Nội` **+ có dropdown** · NCC 1 tài khoản → tự điền, không dropdown ·
      NCC chỉ có cột cũ → vẫn đổ được · NCC không có gì → trống + dòng nhắc · đổi tài khoản trong
      dropdown → 5 ô nhảy sang `116002984759 · Vietinbank`. `php -l` + parse 2 file FE sạch.
- [x] Lưu ý hành vi đổi: NCC có **cả 2 nguồn** thì nay lấy theo `customer_has_bank_accounts` (nguồn
      user nhập qua màn Khách hàng) chứ không lấy cột cũ — vd NCC id 34 đổi từ `MB 0531188050005`
      sang `Vietcombank 1015255543`.
- [ ] User mở trình duyệt xác nhận (cần deploy lên `hrm-crm.eteksofts.com` mới thấy).

### Task phụ — Xuất Excel: bỏ dòng thừa + nới cột + wrap text (2026-08-22) — @khoipv
User báo file Excel phiếu đề nghị thanh toán thừa dòng "Đối tượng nhận tiền", nhiều cột hẹp quá làm
mất chữ; yêu cầu nới cột, dài quá thì xuống dòng chứ đừng che.

**Đo trên file thật trước khi sửa** (dựng file rồi đọc lại bằng PhpSpreadsheet, skill export-excel
mục 7): cột A rộng **6** nhưng chứa nhãn "Hình thức thanh toán:" **21 ký tự**; `D = 18` trong khi
tiêu đề "Số tiền đề nghị chi" dài **19**; số hợp đồng **39 ký tự** trong cột 26; **không ô nào bật
wrap** → 9 ô bị cắt.

- [x] Blade: **bỏ dòng "Đối tượng nhận tiền"** — ERP `billpayment_request_export.blade.php` không có,
      và tên đối tượng đã nằm trong bảng chi tiết (cột NCC/KH/Nhân viên).
- [x] Blade: khối thông tin chung đổi sang **nhãn gộp 2 cột** (`colspan="2"`) đúng như ERP (`:23-49`)
      — cột A phải giữ hẹp vì là STT của bảng chi tiết.
- [x] `BillPaymentRequestExport::columnWidths()`: bỏ bộ cứng A..J, **tính theo tiêu đề thật** của
      từng phiếu (bảng có 9-13 cột tuỳ loại chi): STT = 6 · cột chữ dài (Số hợp đồng · Ghi chú ·
      NCC/KH/Nhân viên · Số chuyến xe · Hạch toán) = 34 · còn lại `len(tiêu đề) + 3`, kẹp trong 14-34.
- [x] `registerEvents()` (`WithEvents` mới thêm): **wrap text + canh trên toàn sheet**, vùng tính từ
      `getHighestRow()/getHighestColumn()` chứ không cắm cứng số dòng (skill mục 5).
- [x] Nhân tiện đúng skill mục 1: `exportData()` trả thêm `money_columns`, blade gắn
      `data-format="#,##0"` cho ô tiền → hết cảnh "số này có dấu phẩy, số kia không", SUM được.
- [x] Verify bằng cách đọc lại file thật (script có tính cả vùng ô gộp): **0 ô bị cắt · 0 ô tiền
      thiếu định dạng · dòng "Đối tượng nhận tiền" đã bỏ**. Bề rộng ra
      `A=6 B=34 C=17 D=22 E=14 F=14 G=19 H=18 I=16 J=34`.
- [x] Chạy đủ **8 bố cục** (loại chi 1/2/6/12 × TM/CK): 9-10 cột, tiền có định dạng ở mọi phiếu,
      không phiếu nào thiếu. `php -l` 2 file PHP sạch. Đã gỡ disk `scratch` tạm khỏi `config/filesystems.php`.
- [ ] User mở file xác nhận.

### Task phụ — Nút Xóa ở bảng File đính kèm không đúng chuẩn button (2026-08-22) — @khoipv
User báo nút Xóa trong bảng file đính kèm chưa đồng bộ với project.

Đối chiếu skill `button-convention` (mục 6 + bảng icon mục 3) và tiền lệ
`pages/assign/contracts/components/ContractImplementSection.vue:35`: nút **chỉ có icon** phải dùng
`V2BaseIconButton`, icon Xóa là `ri-delete-bin-line`. Bản cũ dùng `V2BaseButton quaternary danger`
với icon `ri-delete-bin-6-line` — sai cả component lẫn icon.

- [x] Nút **Xóa** → `V2BaseIconButton danger size="sm"` + icon `ri-delete-bin-line`.
- [x] Đổi luôn 3 nút icon còn lại **cùng dòng** (Xem trước · Tải xuống · Thay đổi) sang
      `V2BaseIconButton` — sửa mỗi nút Xóa thì 1 dòng có 2 kiểu nút, nhìn còn lệch hơn cũ.
      Nút Tải xuống đổi icon `ri-download-2-line` → `ri-download-line` cho khớp bảng icon.
- [x] Nút **Thêm tài liệu**: icon chuyển vào slot `#prefix` (skill mục 1 — mọi `V2BaseButton` phải
      có icon qua slot này), trước đây gắn `<i>` inline trong nội dung nút.
- [x] Verify trên trình duyệt: bảng render ra `Button(ri-add-line, "Thêm tài liệu")` +
      `IconButton(ri-eye-line)` + `IconButton(ri-download-line)` + `IconButton(ri-refresh-line)` +
      `IconButton(ri-delete-bin-line)` với class `v2-icon-btn--danger` cho nút Xóa.
      Grep xác nhận không còn `quaternary` / `ri-delete-bin-6`. Parse template + script sạch.
- [ ] User xác nhận.

### Task phụ — Ô nhập tiền dùng sai dấu phân cách (2026-08-22) — @khoipv
User báo ô "Số tiền đề nghị chi" sai quy tắc: phải `.` cho hàng nghìn, `,` cho thập phân.

Đo hiện trạng: **hiển thị** khắp repo đã đúng chuẩn VN (117 chỗ `toLocaleString('vi-VN')` → `1.234.567`),
nhưng **ô nhập** thì ngược — `V2BaseCurrencyInput` (`:83-85`) format `,` nghìn / `.` thập phân, và
`BaseCurrencyInput` bản cũ (`:108`) dùng `toLocaleString('en')`. Cùng một số mà ô nhập hiện
`1,234,567` còn bảng bên cạnh hiện `1.234.567`.

⚠️ `V2BaseCurrencyInput` là **component dùng chung — 31 màn**. Đã hỏi user trước khi sửa
(CLAUDE.md), user chọn **sửa component dùng chung**.

- [x] `formatCurrency()`: hàng nghìn `.`, thập phân `,`.
- [x] `parseRawValue()`: bỏ `.` rồi đổi `,` → `.` để `Number()` hiểu.
- [x] `onInput()`: nhánh `precision = 0` chặn `,` (thay vì chặn `.`); nhánh "đang gõ dở phần thập
      phân" đổi mốc từ `.` sang `,` — không đổi thì dấu `,` vừa gõ bị nuốt ngay.
- [x] Giá trị **emit ra ngoài vẫn là số thuần** (`Number`) → payload gửi BE không đổi một chữ.
- [x] Verify logic: hiển thị `1000→1.000` · `1234567,89` · `62211.6→62.211,6`; parse
      `1.234.567,89 → 1234567.89`; **khứ hồi 6/6 giá trị khớp tuyệt đối** (số → hiển thị → parse → số).
- [x] Verify gõ thật trên trình duyệt (ô Số tiền đề nghị chi): gõ `1234567` → hiện `1.234.567`,
      emit `1234567` · gõ lại `1.234.567` → giữ nguyên, emit `1234567` · gõ `1234567,89` →
      `1.234.567,89`, emit `1234567.89` · blur giữ nguyên định dạng. Parse component sạch.
- [ ] User xác nhận. **Lưu ý regression:** đổi ở component dùng chung nên cần rà nhanh vài màn khác
      có ô nhập tiền (báo giá, hợp đồng, BOM, dự án tiền khả thi…).
- [ ] `BaseCurrencyInput` (bản cũ, `toLocaleString('en')`) CHƯA sửa — user chọn phạm vi chỉ
      `V2BaseCurrencyInput`. Màn nào còn dùng bản cũ vẫn hiện dấu phẩy.

### Task phụ — Bảng chi tiết: thêm thanh cuộn ngang phía TRÊN (2026-08-22) — @khoipv
User yêu cầu bảng chi tiết có thanh cuộn ngang ở trên, giống bảng của
`customer-care/warranty-repair-requests/create`.

- [x] Bọc bảng bằng component dùng chung **`V2BaseTableScroll`** (đúng cái màn tham chiếu dùng,
      `WarrantyRepairRequestForm.vue:161`) — thanh cuộn ở CẢ trên và dưới, đồng bộ 2 chiều, tự ẩn
      khi bảng không tràn. `body-class` giữ nguyên 2 class cũ `table-responsive table-auto-height`
      để không mất fix "khoảng trống 341px dưới bảng" của 2026-08-15.
- [x] **Đổi `width` → `min-width` cho 14 cột nội dung** của header. Bọc component không thôi là chưa
      đủ: `width` chỉ là gợi ý, màn hẹp thì trình duyệt bóp cột cho vừa khung nên bảng không bao giờ
      tràn và thanh cuộn không bao giờ hiện (đo lần đầu: khung 852 = bảng 852). Đây cũng chính là
      lý do cột bị bóp hẹp làm chữ ép xuống nhiều dòng. 3 cột hẹp (checkbox / STT / nút thêm dòng)
      vẫn để `width`.
- [x] Verify trên trình duyệt ở khung hẹp 900px: loại chi 12 (nhiều cột nhất) → bảng **1006** > khung
      **852** → thanh trên **hiện**, nằm đúng phía trên bảng; kéo thanh trên → bảng chạy theo, kéo
      bảng 60px → thanh trên về 60. Loại chi 1 không tràn → thanh **tự ẩn** (đúng thiết kế). Parse sạch.
- [ ] User xác nhận.

**Đã áp luôn cho màn Đề nghị thu tiền** (user chốt 2026-08-22) — xem
`.plans/gop-db/finance-bill-income-request/plan.md` Task 8.12.

### Task phụ — Cột "Số tiền" ở danh sách hiện MÃ loại tiền (2026-08-22) — @khoipv
User yêu cầu phần đơn vị ở cột Số tiền chỉ để mã loại tiền.

Bảng `currencies` có 2 cột: `code` là **mã chuẩn** (INR, EUR, USD…) còn `name` là **tên gọi**
(RUPEE, EURO…). Lưới đang hiện `name` nên phiếu tiền Ấn Độ ra "220 RUPEE" thay vì "220 INR".
(9/11 dòng trong bảng để `code` trùng `name` nên trước giờ không lộ.)

- [x] BE `BillPaymentRequestListResource`: trả thêm `currency_code` (giữ nguyên `currency_name`,
      không phá màn nào đang dùng).
- [x] FE `index.vue` slot `#cell-totalMoney`: hiện `currency_code`, **lùi về** `currency_name` nếu BE
      chưa deploy field mới (skill `select-and-input-state` mục 5 — FE mới + BE cũ luôn có đường lùi).
- [x] Verify trên trình duyệt: API trả `INR / VNĐ / IDR`, lưới hiện `220 INR` · `16.512.112 VNĐ` ·
      `56.546 IDR` · `3.240.324.324 VNĐ` — trước đó dòng đầu là "220 RUPEE". `php -l` + parse sạch.
- [ ] User xác nhận.

### Task phụ — Đổi NCC nhưng tài khoản ngân hàng cũ không bị xoá (2026-08-22) — @khoipv
User báo: hình thức CK, chọn NCC + chọn ngân hàng, sau đó đổi sang NCC khác thì thông tin tài khoản
của NCC trước vẫn còn.

Nguyên nhân: `loadPartyBanks()` reset `partyBanks/partyAccounts/partyType` nhưng **không xoá các
trường ngân hàng trên `form`**. Nhánh trong nước may mắn không lộ vì luôn gọi `applyPartyAccount()`
ghi đè 6 ô; nhánh **NCC nước ngoài** thì người dùng tự chọn ngân hàng trong dropdown nên **không có
gì ghi đè** → `bank_id`, `swift_code`, `account_number`, `mid_*` của NCC trước ở nguyên. ERP không
dính vì `addInfoSupplier()`/`addInfoCustomer()` gọi `clearInfoBank()` ngay đầu.

- [x] Tách hằng `BANK_FIELDS` (18 trường khối ngân hàng) ra khỏi `CLEARED_FIELDS`; `CLEARED_FIELDS`
      spread lại nên hành vi "đổi loại chi/hình thức" giữ nguyên.
- [x] Thêm `clearBankFields()` — xoá trắng đúng nhóm ngân hàng + xoá lỗi 422 của các ô đó, **giữ
      nguyên đối tượng nhận tiền vừa chọn** (không dùng `clearInfoBank()` vì hàm đó xoá luôn
      `supplier_id` mà `applyParty()` vừa gán).
- [x] Gọi `clearBankFields()` ngay đầu `loadPartyBanks()`, trước khi biết đối tượng mới có gì.
- [x] Verify trên trình duyệt, 4 bước:
      · NCC nước ngoài + chọn ngân hàng → `140-009-783890 · SHINHAN BANK · bank_id 62 · SHBKKRSE`
      · đổi sang NCC không có tài khoản → **sạch toàn bộ** (trước fix vẫn giữ SHINHAN)
      · đổi sang NCC có tài khoản → đổ đúng TK mới, `bank_id`/`swift` = null
      · chiều ngược trong nước → nước ngoài: 5 ô trong nước về null, chờ chọn ngân hàng
      Parse sạch.
- [ ] User xác nhận.

### Task phụ — Đổi tỷ giá không tính lại cột quy đổi VND (2026-08-22) — @khoipv
User báo ở màn Tạo: chọn loại tiền + có tỷ giá, nhập số tiền ở bảng chi tiết, sau đó **sửa lại tỷ
giá** thì cột quy đổi VND vẫn giữ số cũ.

Nguyên nhân: `recalcExchange(detail)` chỉ được gọi từ 2 chỗ — `onCurrencyChange()` (đổi loại tiền)
và `onAmountChange()` (gõ tiền từng dòng). Ô "Tỷ giá (VND)" chỉ `v-model="form.exchange_rate"`,
component không có `watch` nào nên sửa tỷ giá không kích hoạt tính lại dòng nào.

- [x] Thêm `watch: { 'form.exchange_rate' }` trong `BillPaymentRequestForm.vue` → chạy
      `recalcExchange()` cho toàn bộ `form.details` (dòng Tổng cộng `request_exchange` ăn theo).
- [x] Cờ `suppressExchangeRecalc` bật trong `loadDetail()`, tắt ở `$nextTick` của `finally` — tránh
      lần gán `form` khi nạp phiếu cũ ghi đè `payment_money_request_exchange` BE đã lưu; watcher
      cũng bỏ qua khi `readonly`.
- [x] Verify: `vue-template-compiler` + `@babel/parser` parse sạch.
- [ ] User mở trình duyệt xác nhận.

### Task phụ — Nút Duyệt / Không duyệt ở màn danh sách (2026-08-22) — @khoipv
User yêu cầu bổ sung nút **Duyệt** và **Không duyệt** ra cột Hành động của lưới, chỉ cho phiếu đủ
điều kiện. **User chốt: 2 nút chỉ ĐIỀU HƯỚNG sang màn chi tiết rồi duyệt ở đó**, không duyệt tắt từ
danh sách — vì số tiền từng cấp phải xem/sửa được trước khi duyệt (API `approve` bắt buộc `details`
gồm id + số tiền từng dòng).

- [x] BE `BillPaymentRequestListResource`: trả thêm `is_can_approve` + `is_can_cancel`, dùng đúng 2
      hàm màn chi tiết đang dùng (`canApproveAtCurrentStatus()` / `canCancel()`) để không lệch điều kiện.
- [x] `is_can_approve` siết thêm `status ∈ {2,3,4,5}`: `canApproveAtCurrentStatus()` còn trả true cho
      **"Chờ tạo phiếu chi" (6)**, mà `ApproveActions.vue` không có nút duyệt cho trạng thái đó →
      hiện nút ở lưới thì bấm vào chi tiết không thấy gì để duyệt.
- [x] FE `index.vue`: thêm 2 action `approve` / `reject` dùng `to` → render `<nuxt-link>` như nút Sửa
      (chuột phải mở tab mới được); icon `ri-check-line` / `ri-close-circle-line` theo skill
      `button-convention`. Giữ nhánh trong `handleRowAction` cho chỗ gọi trực tiếp.
- [x] Không phát sinh N+1 đáng kể: `currentEmployeeHasPermission()` có cache tĩnh theo
      (nhân viên, quyền) nên cả trang chỉ 1 lượt query quyền.
- [x] Verify trên trình duyệt — cờ BE theo từng trạng thái:
      Đang tạo / Đã hủy / Không duyệt / Duyệt phiếu chi → **không nút** ·
      Chờ TP duyệt · Chờ KT trưởng duyệt → **cả 2 nút** ·
      Chờ tạo phiếu chi → **chỉ Không duyệt** (khớp đúng màn chi tiết).
      DOM lưới: dòng "Chờ TP duyệt" render `<a ri-check-line href=/finance/bill-payment-requests/4198>`
      + `<a ri-close-circle-line href=...4198>`; dòng "Đang tạo" vẫn là Sửa/In; dòng "Đã hủy" chỉ In/Xuất.
      `php -l` + parse FE sạch.
- [x] **Bổ sung nút "Tạo phiếu chi" (user hỏi ngay sau đó):** BE trả thêm `is_can_create_bill_payment`
      với ĐÚNG 3 vế của màn chi tiết — trạng thái "Chờ tạo phiếu chi" · chưa có phiếu chi nào trỏ tới
      (luật 1 đề nghị 1 phiếu chi) · có quyền Kế toán thanh toán. Tránh N+1: hỏi 1 lượt
      `whereIn('bill_payment_request_id', $ids)` cho cả trang thay vì gọi `existsForRequest()` từng
      dòng, quyền kế toán tính 1 lần ngoài vòng lặp.
      FE thêm action `create_bill_payment` (icon `ri-add-line`) trỏ
      `/finance/bill-payments/create?bill_payment_request_id={id}` — cùng đích với nút ở màn chi tiết.
      Verify: 12 phiếu trên trang chỉ 2 phiếu "Chờ tạo phiếu chi" có cờ; DOM dòng đó render
      `ri-add-line → /finance/bill-payments/create?bill_payment_request_id=4195` cạnh nút Không duyệt.
- [ ] User xác nhận.

### Task phụ — Popup "Chi tiết chuyến xe": nới rộng cột (2026-08-22) — @khoipv
User yêu cầu nới cột trong popup chi tiết chuyến xe (loại chi 12).

- [x] `DeliveryTripDetailModal.vue`: đổi **13 cột** từ `width` → `min-width` và nới thêm
      (170/180/200/100/120/**140+140**/150/130/150/260/190/280 — tổng **2.210px**, trước là 1.910px).
      `width` chỉ là gợi ý nên trong khung modal hẹp hơn bảng, trình duyệt bóp cột lại và chữ bị chèn.
- [x] Bọc `V2BaseTableScroll` — 13 cột không thể vừa bề ngang modal, có thanh cuộn ngang ở CẢ trên và
      dưới thì không phải kéo xuống đáy mới cuộn được (đồng bộ 2 bảng chi tiết đã làm cùng ngày).
- [x] Verify trên trình duyệt (mở popup bằng chuyến xe thật `delivery_trip_id = 349`): khung **1.106px**
      < bảng **2.211px** → thanh cuộn trên **hiện**; từng cột đo đúng bề rộng mới; dòng dữ liệu đọc ra
      đủ 13 ô (`TPE_CXCH_00349 | TPE_HTCXCH_00362 | Xe tải có mui - 8 tấn | 337 | 0 | 9.608.544 | 0 |
      2.000.000 | 160.000 | 2.160.000 | Liên Ninh, Hà Nội - Hà Tĩnh, Hà Tĩnh | …`). Parse sạch.
- [ ] User xác nhận.

### Task phụ — Lịch sử thay đổi (skill `entity-history`) (2026-08-22) — @khoipv

Yêu cầu user: bổ sung **Xem lịch sử thay đổi** cho màn Đề nghị thanh toán, ngay sau khi làm xong
cho màn Đề nghị thu tiền. Áp **cùng 2 quyết định** user đã chốt cho màn kia, không hỏi lại:
bảng chi tiết log **diff từng dòng** (`~` sửa / `-` bỏ / `+` thêm) · **không gắn permission riêng**.

Hạ tầng dùng lại 100% (bảng chung `catalog_histories`, endpoint `catalog-histories/{table}/{id}`,
`CatalogHistoryModal`, `SystemInfoSection`) — **không migration, không permission mới**.

- [x] **BE-1** `CatalogHistoryService::TABLES` — khai `bill_payment_requests` + nhãn tiếng Việt
      (Loại chi · Hình thức thanh toán · Lý do chi · Ghi chú · Tiền tệ · Tỷ giá · Trạng thái ·
      Đến ngày · 3 cột đối tượng `*_name` · 12 cột khối ngân hàng · Phí chuyển tiền) + 2 khoá ẢO
      dạng BẢNG: `attachment_rows`, `details_rows`.
      Theo dõi bản `*_name` chứ KHÔNG phải `*_id`: log tự chứa, đổi tên ngân hàng / KH về sau
      không làm sai log cũ.
- [x] **BE-2** `BillPaymentRequestService` — `use LogsCatalogHistory` + `catalogTable()` /
      `catalogColumns()` / `catalogDisplay()` + `attachmentRows()` + `detailRows()` +
      `historySnapshot()` (thuần, cho ảnh TRƯỚC) + `applyHistoryVirtuals()` (gán khoá ảo, cho ảnh
      SAU). Log ở `store()` / `update()` / `destroy()`.
      · `attachment_rows`: cột `attachments` của ERP là chuỗi URL nối bằng `', '` — log nguyên
        chuỗi thì thêm 1 file là in lại cả danh sách; tách thành bản ghi/file nên chỉ in `+`/`-`.
- [x] **BE-3** `BillPaymentRequest` — `statusName()` + `logStatusHistory()` (có thêm `$extraOld` /
      `$extraNew` để đính kèm dữ liệu vào cùng dòng log, bọc try/catch + `Log::error` vì phần lớn
      chỗ gọi nằm trong transaction hạch toán).
- [x] **BE-4** `BillPaymentApprovalService` — duyệt theo cấp ghi **1 dòng log gộp**: trạng thái +
      **số tiền cấp này vừa duyệt cho từng dòng chi tiết** (`MONEY_LABEL_BY_COLUMN`). Chỉ ghi
      "Chờ TP duyệt → Chờ KT công nợ duyệt" mà thiếu số tiền là mất đúng thông tin quan trọng nhất
      của màn này. `reject()` ghi log kèm **lý do không duyệt** (`reject_comment`) — skill §4.1.
- [x] **BE-5** 4 chỗ đổi trạng thái phiếu TỪ MÀN KHÁC cũng ghi log (thiếu thì timeline đứt quãng):
      `BillPaymentWriteService` (→ Chờ duyệt phiếu chi) · `BillPaymentApprovalFlowService`
      (→ Duyệt phiếu chi; → Đã hủy **kèm lý do hủy**) · `BillPaymentAuthorizationWriteService`
      (uỷ nhiệm chi → Duyệt phiếu chi).
- [x] **FE-1** `index.vue` — hành động **Lịch sử** (`ri-history-line`, không gắn quyền) trong menu ⋮
      + `CatalogHistoryModal` (`modal-id="history-bill-payment-request"`). Có ở cả 4 chế độ xem.
- [x] **FE-2** `components/BillPaymentRequestForm.vue` — thêm slot `after-content` **TRƯỚC**
      `V2Footer` (footer `position: fixed` + spacer 66px; cắm khối sau nó thì bị đè và hở khoảng
      trắng).
- [x] **FE-3** `_id/index.vue` — khối `SystemInfoSection` (`entity-type="bill_payment_requests"`)
      cắm vào slot đó.

**Lỗi bắt được trong lúc verify (đã sửa):** `historySnapshot()` bản đầu gán 2 khoá ảo lên model
TRƯỚC `save()` → `SQLSTATE[42S22] Unknown column 'attachment_rows' in field list`. Tách làm 2 hàm:
hàm dựng snapshot **không đụng model**, hàm gán khoá ảo chỉ gọi SAU lần `save()` cuối. Rà lại màn
Đề nghị thu tiền và **chuyển luôn log `create` ra ngoài transaction** cho cùng lý do.
Sửa thêm: tên bản ghi ghép bằng `array_filter` — dòng không có đối tượng (754/47.329 dòng trên DB
gộp) trước đó ra tên bắt đầu bằng `" / "`.

**Verify (tinker, chạy trong transaction rồi rollback — không để lại dấu vết):**
- `update()` đổi Lý do chi + số tiền 1 dòng → 1 dòng log gộp, `~` chỉ in đúng cột đã đổi.
- Lưu lại **y hệt** (2 lần liên tiếp) → **0 log**.
- `store()` → 1 log `create`; `destroy()` → 1 log `delete`.
- Duyệt cấp TP → 1 log: `Chờ TP duyệt → Chờ kế toán công nợ duyệt` + `~ <tên dòng>: Số tiền TP
  duyệt: 0 → 55.546`. `reject()` → log kèm ghi chú "Thiếu hợp đồng đính kèm".
- Tệp đính kèm: gỡ 1 + thêm 1 → đúng 1 dòng `-` và 1 dòng `+`, không in lại cả danh sách.
- `filter-options`: 3 nhóm cố định + 783 người thực hiện.
- FE: compile template + parse script 3 file — OK.

Chưa tự test trình duyệt (theo thoả thuận) — user tự xác nhận popup ⋮ → Lịch sử và khối Lịch sử ở
màn chi tiết. Chưa commit.

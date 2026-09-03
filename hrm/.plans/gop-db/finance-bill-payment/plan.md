# Plan — Phiếu chi tiền (ERP → HRM)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development` (khuyến nghị) hoặc `superpowers:executing-plans` để thực thi từng task. Step dùng checkbox (`- [ ]`) để theo dõi.

- Người phụ trách: @khoipv
- Nhánh: `gop_db` (cả 2 repo — **KHÔNG tạo branch riêng**)
- Spec: `docs/superpowers/specs/gop-db/2026-08-19-finance-bill-payment-design.md` (ĐÃ DUYỆT 2026-08-19)
- Design tóm tắt: `.plans/gop-db/finance-bill-payment/design.md`

**Goal:** Port màn ERP "Phiếu chi tiền" (`admin/income-expenditure/bill_payments`, bảng `bill_payments`) sang HRM tại `Modules/Finance` + `pages/finance/bill-payments` — đủ 5 loại chi, 1 màn danh sách duy nhất, tạo/sửa/xóa nháp, gửi duyệt, duyệt **kèm ghi bút toán sổ cái**, hủy, in 2 liên, xuất Excel.

**Architecture:** BE bám nguyên bộ `BillIncome*` trong `Modules/Finance` (Entity + Service + FormRequest + Resource + Controller V1), quyền kiểm bằng trait `ChecksEmployeePermission` chứ không dùng middleware. Nghiệp vụ chia **2 nhánh**: nhánh A (loại 1/2/6/12, lập từ Đề nghị thanh toán, duyệt 1 cấp) và nhánh B (loại 4 Chi thu nhập nhân viên, lập trực tiếp, duyệt 2 cấp). Mỗi nhánh có **1 service ghi sổ cái riêng**, cả hai tách hàm **thuần** `buildEntries()` trả mảng dòng đã đủ cột — unit test được không cần DB, đây là cơ chế kiểm chứng chính. FE bám khuôn `pages/finance/bill-incomes/`.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL (DB gộp `gop_db`, connection mặc định) · PHPUnit 9.5 · Nuxt 2 / Vue 2 / Bootstrap-Vue.

---

## Global Constraints

Mọi task đều phải tuân thủ, không nhắc lại trong từng task:

- Nhánh git phải là `gop_db` ở **CẢ** `hrm-api` và `hrm-client` — kiểm `git branch --show-current` trước khi sửa file; sai nhánh thì **DỪNG**, báo user.
- **KHÔNG git commit / push** — user tự commit. Plan này cố ý **không có step commit**; thay bằng step verify.
- **KHÔNG tạo nhánh mới.**
- KHÔNG đổi schema 3 bảng `bill_payments` / `bill_payment_details` / `bill_payment_detail_product_export_requests`, **KHÔNG migration**.
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`. Model `TpXxx` **được dùng** nếu chạy trên connection mặc định — cụ thể `App\Models\TpCustomer` (bảng `customers`) là luồng khách hàng duy nhất; **đừng** thay bằng `Modules\Timesheet\Entities\Customer` (id lệch).
- KHÔNG nới `$guarded` của `Modules/Finance/Entities/Accounting/AccountDetail.php` (entity **CHỈ ĐỌC**, `BillPaymentDebtService` phụ thuộc) — ghi sổ cái qua `AccountDetailEntry` đã có.
- KHÔNG sửa `registerMorphMap()` ngoài việc **THÊM 5 cặp** ở Task 2. Không đụng 11 cặp đã có.
- KHÔNG gắn middleware `checkPermission` cho route nào của màn này — gate trong Controller/Entity (spec §7.2).
- `ValidationException` **KHÔNG** được catch — để bay lên cho FE nhận 422 chuẩn Laravel.
- KHÔNG chạy `PermissionsTableSeeder` trên DB local (`run()` truncate bảng, và seeder đang có sẵn lỗi trùng id 1117/1118).
- Cờ quyền FE **fail-closed**: khởi tạo `false`, cấm gán literal `true`. Pattern bị chặn khi review: `can[A-Za-z]*\s*=\s*true`.
- **KHÔNG tự test bằng Playwright** — verify bằng `php -l` + phpunit + tinker (BE) và `vue-template-compiler` + `@babel/parser` (FE); user tự mở trình duyệt. Báo rõ phần chưa kiểm chứng.
- **Dữ liệu nghiệp vụ đã lưu: KHÔNG sửa.** Mọi bản ghi test tạo ra phải xóa sạch. Baseline đếm thật 2026-08-19: `bill_payments` **1.302** · `bill_payment_details` **3.307** · `bill_payment_detail_product_export_requests` **0**.
- Mọi text hiển thị tiếng Việt. Toast dùng đúng câu ERP ghi trong spec §12.
- Migration PHP (nếu có) phải có PHPDoc trên `up()`/`down()` — nhưng feature này **không có migration**.
- ⚠️ **Tên quan hệ trộn 2 kiểu — bẫy đã dính 1 lần, đọc kỹ:**
  - Entity **MỚI** của feature này (`BillPayment`, `BillPaymentDetail`) dùng **camelCase**: `details`, `billPaymentRequest`, `employeeCreate`, `approvedBy`, `accountingApprovedBy`, `accountHas`, `paymentDepartment`, `customer`, `supplier`, `employee`, `contractable`, `productExportRequests`.
  - Entity **CŨ** `BillPaymentRequest` (feature trước, **KHÔNG được sửa**) dùng **snake_case**: `details`, `currency`, `employee_create`, `employee_update`, `approved_by`.
  → Eager load xuyên 2 entity phải viết `billPaymentRequest.employee_create.info`, **KHÔNG** phải `billPaymentRequest.employeeCreate.info`. Sai tên là Eloquent ném `Call to undefined relationship` lúc chạy, `php -l` không bắt được.
- FE trước khi code phải đọc: `.claude/skills/erp-to-hrm-screen/SKILL.md`, `list-page`, `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`, `select-and-input-state`, `print-page`, `notification-convention`. Icon phải đối chiếu font local: `grep "^\.ri-xxx:before" hrm-client/assets/scss/custom/plugins/icons/_remixicon.scss`.

---

## Bảng tra id dùng trong mọi step verify

Nhiều step verify cần id nhân viên / phiếu cụ thể. **Chạy khối lệnh này MỘT LẦN ở đầu, ghi kết quả ra giấy**, rồi thay vào chỗ `<...>` của các task. Đừng đoán id.

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "
-- <id kế toán thanh toán>
SELECT e.id, ei.fullname, 'Kế toán thanh toán' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Kế toán thanh toán' LIMIT 3;
-- <id thủ quỹ>
SELECT e.id, ei.fullname, 'Thủ quỹ duyệt phiếu chi' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Thủ quỹ duyệt phiếu chi' LIMIT 3;
-- <id kế toán trưởng>
SELECT e.id, ei.fullname, 'Kế toán trưởng duyệt phiếu chi' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Kế toán trưởng duyệt phiếu chi' LIMIT 3;
-- <id nhân viên có quyền tổng cty> / <chỉ có quyền công ty> / <không quyền>
SELECT e.id, MAX(p.name = 'Xem tất cả phiếu chi của tổng công ty') tong_cty,
       MAX(p.name = 'Xem tất cả phiếu chi của công ty') cong_ty
  FROM employees e
  LEFT JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  LEFT JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  LEFT JOIN permissions p ON p.id = rhp.permission_id
 GROUP BY e.id HAVING tong_cty = 1 OR cong_ty = 1 LIMIT 5;
-- <id phòng ban có phiếu loại 4>
SELECT payment_department_id, COUNT(*) n FROM bill_payments
 WHERE type = 4 AND payment_department_id IS NOT NULL GROUP BY payment_department_id ORDER BY n DESC LIMIT 3;
-- <id phiếu status 1 / 2 / loại 4 status 5>
SELECT id, code, type, status FROM bill_payments WHERE status IN (1,2) OR (type = 4 AND status = 5);
"
```

⚠️ **Trạng thái 5 hiện có 0 dòng** và `status = 1` chỉ có **1 dòng** — các step cần phiếu ở 2 trạng thái đó phải **tự tạo phiếu test trong transaction rồi rollback**, không mượn dữ liệu thật.

⚠️ **Auth guard cache theo tiến trình**: mỗi danh tính chạy **1 lệnh tinker riêng**. Gộp nhiều `loginUsingId()` trong 1 process thì lần 2 trở đi vẫn dùng danh tính đầu — đừng kết luận nhầm là fail-open.

---

# Phase 1 — Nền tảng Backend: xem được danh sách + chi tiết

## Task 1: Entity `BillPayment` + 2 entity chi tiết

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php`
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentDetail.php`
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentDetailProductExportRequest.php`

**Interfaces:**
- Consumes: `Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest` (đã có) · `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (đã có) · `Modules\Finance\Entities\Account\Account` · `Modules\Human\Entities\Employee`.
- Produces: class `Modules\Finance\Entities\BillPayment\BillPayment` — 5 hằng `STATUS_*`, hằng `STATUSES`, 4 hằng `PERMISSION_*`, hằng `TYPE_PAYMENT_EMPLOYEE = 4`; quan hệ `details()`, `billPaymentRequest()`, `employeeCreate()`, `approvedBy()`, `accountingApprovedBy()`, `accountHas()`, `paymentDepartment()`; static `generateCode(): string`. Task 2-23 dùng class này.

**Khuôn để copy:** `hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php` — copy nguyên cấu trúc docblock, `boot()`, `$fillable`, hằng số; đổi tên bảng/cột.

- [x] **Step 1: Kiểm tra branch cả 2 repo**

```bash
git -C D:/laragon/www/hrm/hrm-api branch --show-current
git -C D:/laragon/www/hrm/hrm-client branch --show-current
```
Kỳ vọng: cả 2 in `gop_db`. Khác → **DỪNG**, báo user.

- [x] **Step 2: Đếm baseline dữ liệu**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT (SELECT COUNT(*) FROM bill_payments) bp, (SELECT COUNT(*) FROM bill_payment_details) bpd, (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Kỳ vọng: `bp = 1302`, `bpd = 3307`. Lệch → dừng, báo user (có người ghi song song).

- [x] **Step 3: Viết `BillPayment.php`**

Yêu cầu bắt buộc trong file:

```php
class BillPayment extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'bill_payments';

    const STATUS_CREATING = 1;                    // Đang tạo
    const STATUS_AWAITING_APPROVE = 2;            // Chờ chi tiền (chờ Thủ quỹ)
    const STATUS_APPROVED = 3;                    // Đã duyệt
    const STATUS_CANCEL = 4;                      // Hủy
    const STATUS_AWAITING_ACCOUNTING_APPROVE = 5; // Chờ KT trưởng duyệt (CHỈ nhánh B)

    /** Bộ màu đổi so với ERP (ERP để danger cho cả 1/2/4/5) — spec §5.2. */
    public const STATUSES = [
        ['id' => self::STATUS_CREATING, 'name' => 'Đang tạo', 'type' => 'secondary'],
        ['id' => self::STATUS_AWAITING_APPROVE, 'name' => 'Chờ chi tiền', 'type' => 'warning'],
        ['id' => self::STATUS_APPROVED, 'name' => 'Đã duyệt', 'type' => 'success'],
        ['id' => self::STATUS_CANCEL, 'name' => 'Hủy', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_ACCOUNTING_APPROVE, 'name' => 'Chờ KT trưởng duyệt', 'type' => 'warning'],
    ];

    /** Loại chi lập trực tiếp, KHÔNG qua Đề nghị thanh toán (nhánh B). */
    const TYPE_PAYMENT_EMPLOYEE = 4;

    /** Loại chi lập từ Đề nghị thanh toán (nhánh A). */
    const TYPES_FROM_REQUEST = [1, 2, 6, 12];

    /** Tên giữ NGUYÊN VĂN ERP. Bản HRM guard `api` id 1503-1506 khai ở Task 2. */
    const PERMISSION_TREASURER = 'Thủ quỹ duyệt phiếu chi';
    const PERMISSION_CHIEF_ACCOUNTANT = 'Kế toán trưởng duyệt phiếu chi';
    const PERMISSION_VIEW_ALL_COMPANY = 'Xem tất cả phiếu chi của tổng công ty';
    const PERMISSION_VIEW_COMPANY = 'Xem tất cả phiếu chi của công ty';

    /** Quyền tạo/sửa/xóa — dùng LẠI quyền đã có (id 1152), không khai mới. */
    const PERMISSION_ACCOUNTANT = 'Kế toán thanh toán';
}
```

`$fillable` liệt kê đủ 24 cột của bảng (spec §4): `code`, `bill_payment_request_id`, `receiver`, `account_has`, `date_accounting`, `status`, `created_by`, `updated_by`, `company_id`, `department_id`, `part_id`, `approved_id`, `sum_payment_money_request_exchange`, `sum_payment_money_approve_exchange`, `type`, `type_payment`, `type_money_id`, `exchange_rate`, `reason`, `payment_department_id`, `accounting_approved_id`.

`boot()` copy nguyên pattern của `BillIncome::boot()` (`BillIncome.php:79-99`):

```php
protected static function boot()
{
    parent::boot();

    // 3 cột đơn vị tổ chức gán ở `creating` — KHÔNG bắt chước ERP gán ở `created` rồi save()
    // lần 2 (2 câu ghi, để lại bản ghi nửa vời nếu lần 2 lỗi). Gán ĐÈ vô điều kiện, KHÔNG dùng
    // `??`: 3 cột nằm trong $fillable, client gửi `0`/`""` thì `??` giữ nguyên và bản ghi lọt
    // khỏi mọi nhánh lọc theo cấp.
    static::creating(function (self $model) {
        $info = optional(auth()->user())->info;
        $model->company_id = optional($info)->company_id;
        $model->department_id = optional($info)->department_id;
        $model->part_id = optional($info)->part_id;
        $model->created_by = $model->created_by ?: auth()->id();
    });

    static::saving(function (self $model) {
        $model->updated_by = auth()->id() ?? $model->updated_by;
    });
}
```

**KHÔNG** khai accessor `getDateAccountingAttribute()` trả `d/m/Y` như ERP — giữ `Y-m-d`, format ở Resource (lý do: cột này ghi thẳng vào sổ cái).

`generateCode()` — bọc transaction + `lockForUpdate()`, copy pattern `BillIncomeRequest::generateCode()`:

```php
/**
 * Mã phiếu `<mã công ty>.PC<mm><yy>.<5 số>` — ví dụ `TP.PC0825.00001`.
 * ERP dùng autoGenerateCode() KHÔNG khoá; 2 cổng cùng sinh mã dễ trùng nên HRM khoá dòng.
 */
public static function generateCode(): string
{
    $companyCode = optional(optional(auth()->user())->info)->company->code ?? '';
    $prefix = $companyCode . '.PC' . now()->format('my') . '.';

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

⚠️ Bám **đúng bản production** `BillIncomeRequest::generateCode()` (:392-411). KHÔNG dùng `orderByDesc('code')` rồi `substr` — `code` là chuỗi nên `'...00009' > '...00010'`, sinh mã trùng ngay khi vượt 9 phiếu/tháng.

- [x] **Step 4: Viết `BillPaymentDetail.php`**

`$table = 'bill_payment_details'`. `$fillable` liệt kê **đúng** các cột có thật trong bảng (spec §4).

⚠️ **KHÔNG** khai 4 cột `payment_market_cost`, `payment_extra`, `cost_debt_id`, `type_payment_employee` — **không tồn tại trong DB**, ERP truyền vào nhưng bị `$fillable` lọc âm thầm.
⚠️ **KHÔNG** port `saveCommissionEmployee()` và 4 quan hệ `diff_employees()` / `commission_months()` / `commission_quarters()` / `commission_bonus_quarters()` — code chết, `where('type_payment_employee', N)` trên cột không tồn tại, gọi vào là nổ SQL.

Quan hệ cần có: `billPayment()`, `customer()` (→ `App\Models\TpCustomer`), `supplier()`, `employee()`, `contractable()` (`morphTo`), `account()` (→ `Account`, khoá `account_dept`), `productExportRequests()`.

- [x] **Step 5: Viết `BillPaymentDetailProductExportRequest.php`**

`$table = 'bill_payment_detail_product_export_requests'`, `$fillable = ['bill_payment_detail_id', 'product_export_request_id', 'allocated_value', 'allocated_value_exchange']`. Docblock ghi rõ: **0 dòng dữ liệu thật, port theo yêu cầu 1:1, không test chạy thật được**.

- [x] **Step 6: Verify — lint + đọc dữ liệu thật qua entity**

```bash
php -l Modules/Finance/Entities/BillPayment/BillPayment.php
php -l Modules/Finance/Entities/BillPayment/BillPaymentDetail.php
php -l Modules/Finance/Entities/BillPayment/BillPaymentDetailProductExportRequest.php
```
Kỳ vọng: `No syntax errors detected` cả 3.

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
\$b = BillPayment::with('details')->find(1);
echo BillPayment::count(), ' | ', \$b->code, ' | details=', \$b->details->count(), PHP_EOL;
"
```
Kỳ vọng: in `1302 | <mã phiếu> | details=<số>`. Nổ `Call to undefined relationship` → sai tên quan hệ, xem Global Constraints.

---

## Task 2: Quyền + morphMap

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm sau dòng khai id 1502)
- Modify: `hrm-api/Modules/Finance/Providers/FinanceServiceProvider.php:54-68` (thêm 5 cặp vào `Relation::morphMap`)
- Create: `hrm-api/Modules/Finance/Entities/Contract/ProductExport.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/DeliveryTripAccounting.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/OtherDeliveryTripAccounting.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/DeclareDebtBeginning.php`

**Interfaces:**
- Produces: 4 entity morph target + 5 khoá morphMap mới. Task 9 và 14 ghi các `*_type` này vào sổ cái.

- [x] **Step 1: Thêm 4 quyền vào seeder**

Chèn ngay **sau** dòng khai id 1502 (`Thủ quỹ duyệt phiếu thu`):

```php
        // Màn Phiếu chi tiền — 4 quyền ERP ĐÃ CÓ ở guard `web` (id 100207 / 100319 / 100220 /
        // 100221) nhưng app chạy guard `api` nên phải khai bản `api` riêng. Giữ NGUYÊN VĂN tên
        // của ERP để 2 cổng đối chiếu quyền không lệch và để trait ChecksEmployeePermission
        // (so theo `name`, không lọc guard) bắt được cả 13 role đang gán bản `web`.
        // Quyền TẠO/SỬA/XÓA dùng LẠI 'Kế toán thanh toán' (id 1152), KHÔNG khai mới.
        Permission::create(['id' => 1503, 'guard_name' => 'api', 'name' => 'Thủ quỹ duyệt phiếu chi', 'display_name' => 'Thủ quỹ duyệt phiếu chi', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 1]);
        Permission::create(['id' => 1504, 'guard_name' => 'api', 'name' => 'Kế toán trưởng duyệt phiếu chi', 'display_name' => 'Kế toán trưởng duyệt phiếu chi', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 2]);
        Permission::create(['id' => 1505, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu chi của tổng công ty', 'display_name' => 'Xem tất cả phiếu chi của tổng công ty', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 3]);
        Permission::create(['id' => 1506, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu chi của công ty', 'display_name' => 'Xem tất cả phiếu chi của công ty', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 4]);
```

- [x] **Step 2: Kiểm id 1503-1506 chưa bị dùng**

```bash
grep -n "'id' => 150[3-6]" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: đúng **4** dòng (4 dòng vừa thêm). Nhiều hơn → trùng id, đổi dải và báo user.

- [x] **Step 3: Chèn 4 quyền vào DB local bằng tay (KHÔNG chạy seeder)**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "
INSERT INTO permissions (id, name, display_name, guard_name, \`group\`, type, sort_order, created_at, updated_at) VALUES
 (1503,'Thủ quỹ duyệt phiếu chi','Thủ quỹ duyệt phiếu chi','api','Phiếu chi tiền',8,1,NOW(),NOW()),
 (1504,'Kế toán trưởng duyệt phiếu chi','Kế toán trưởng duyệt phiếu chi','api','Phiếu chi tiền',8,2,NOW(),NOW()),
 (1505,'Xem tất cả phiếu chi của tổng công ty','Xem tất cả phiếu chi của tổng công ty','api','Phiếu chi tiền',8,3,NOW(),NOW()),
 (1506,'Xem tất cả phiếu chi của công ty','Xem tất cả phiếu chi của công ty','api','Phiếu chi tiền',8,4,NOW(),NOW());"
```
Kỳ vọng: chạy xong không lỗi. Lỗi trùng khoá → id đã tồn tại, dừng và báo user.

- [x] **Step 4: Viết 4 entity morph target**

Mỗi file là entity mỏng, chỉ khai `$table` và `$fillable` rỗng (chỉ đọc), kèm docblock nói rõ nó là bảng của ERP. Ví dụ `ProductExport.php`:

```php
<?php

namespace Modules\Finance\Entities\Contract;

use Illuminate\Database\Eloquent\Model;

/**
 * Phiếu xuất hàng của ERP — chỉ dùng làm đích morph cho `account_details.billable_type`
 * ở nhánh phân bổ phiếu xuất hàng của phiếu chi (0 dòng dữ liệu thật).
 * CHỈ ĐỌC: không ghi qua entity này.
 */
class ProductExport extends Model
{
    protected $table = 'product_exports';
    protected $guarded = ['*'];
}
```

Tên bảng 3 entity còn lại — **SỐ ÍT**, đã verify trên DB thật: `delivery_trip_accounting` · `other_delivery_trip_accounting` · `declare_debt_beginning`. (Chỉ `product_exports` là số nhiều.)

- [x] **Step 5: Xác nhận 4 bảng tồn tại trước khi khai entity**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SHOW TABLES LIKE 'product_exports'; SHOW TABLES LIKE 'delivery_trip_accounting'; SHOW TABLES LIKE 'other_delivery_trip_accounting'; SHOW TABLES LIKE 'declare_debt_beginning';"
```
Kỳ vọng: in đủ 4 tên bảng. Thiếu bảng nào → **DỪNG**, báo user (không tự tạo bảng).

- [x] **Step 6: Thêm 5 cặp vào morphMap**

Trong `FinanceServiceProvider::registerMorphMap()`, thêm vào **cuối** mảng (giữ nguyên 11 cặp đã có):

```php
            // Chứng từ phiếu chi — để `account_details.invoiceable_type` ghi đúng chuỗi class ERP,
            // nếu không cổng ERP đọc sổ cái sẽ không resolve được chứng từ (spec §6).
            'App\Model\IncomeExpenditure\BillPayment'      => BillPayment\BillPayment::class,
            // 4 đích `billable_type` của phiếu chi (spec §6.1).
            'App\Model\Warehouse\ProductExport'            => FinanceContract\ProductExport::class,
            'App\Model\Warehouse\DeliveryTripAccounting'  => FinanceContract\DeliveryTripAccounting::class,
            'App\Model\Warehouse\OtherDeliveryTripAccounting' => FinanceContract\OtherDeliveryTripAccounting::class,
            'App\Model\Accounting\DeclareDebtBeginning'    => FinanceContract\DeclareDebtBeginning::class,
```

⚠️ Đầu file provider phải có `use` cho namespace mới, cạnh alias `FinanceContract` đã có:

```php
use Modules\Finance\Entities\BillPayment;
```
(alias `FinanceContract` cho `Modules\Finance\Entities\Contract` đã tồn tại sẵn — 4 entity mới nằm cùng namespace đó nên không cần thêm.)

⚠️ 4 chuỗi namespace ERP bên trái phải **khớp chính xác** tên class thật của ERP. Xác minh bằng:

```bash
grep -rn "^namespace" /d/laragon/www/erp/app/Model/Warehouse/ProductExport.php /d/laragon/www/erp/app/Model/Accounting/DeclareDebtBeginning.php
grep -rn "class DeliveryTripAccounting\b\|class OtherDeliveryTripAccounting\b" /d/laragon/www/erp/app/ --include=*.php
```
Lệch → sửa lại chuỗi theo kết quả grep, **không** đoán.

- [x] **Step 7: Verify**

```bash
php -l Modules/Finance/Providers/FinanceServiceProvider.php
php -l Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
php artisan tinker --execute="
echo count(Illuminate\Database\Eloquent\Relations\Relation::morphMap()), PHP_EOL;
echo DB::table('permissions')->whereIn('id',[1503,1504,1505,1506])->count(), PHP_EOL;
"
```
Kỳ vọng: số cặp morphMap **tăng đúng 5** so với trước (đếm trước khi sửa để so), và in `4`.

---

## Task 3: `BillPaymentService` (lọc + phạm vi quyền) + `BillPaymentListResource` + `index`

**Files:**
- Modify: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php` (thêm `applyScope()` + `existsForRequest()`)
- Create: `hrm-api/Modules/Finance/Services/BillPaymentService.php`
- Create: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm group `/bill-payments` sau group `/bill-incomes`, khoảng dòng 258)

**Interfaces:**
- Consumes: `BillPayment` (Task 1).
- Produces: `BillPaymentService::searchByFilter(Request $request)` trả **paginator** (bám khuôn `BillIncomeService`, KHÔNG trả Builder) · `BillPayment::applyScope(Builder $q): Builder` · `BillPayment::existsForRequest(int $requestId, ?int $exceptBillId = null): bool` · endpoint `GET /api/v1/finance/bill-payments`. Task sau cần Builder thô thì gọi thẳng `BillPayment::applyScope()`.

**Khuôn để copy:** `Services/BillIncomeService.php` (213 dòng) và `Transformers/BillIncomeResource/BillIncomeListResource.php` (81 dòng).

- [x] **Step 1: Viết `applyScope()` trong entity `BillPayment`**

```php
/**
 * Phạm vi dữ liệu màn danh sách — port ERP `searchByFilter()` nhánh `_type = all`
 * (`BillPayment.php:216-227`), là nhánh rộng nhất trong 4 chế độ cũ. 3 chế độ còn lại của ERP
 * nay là bộ lọc trên màn (user chốt gộp 1 màn, spec §2 quyết định #2).
 *
 * Phiếu NHÁP (status 1) của người khác LUÔN bị ẩn ở mọi cấp quyền.
 * Người dùng luôn thấy phiếu mình đã duyệt (approved_id / accounting_approved_id).
 */
public static function applyScope(Builder $query): Builder
{
    $employeeId = auth()->id();

    if (!static::currentEmployeeIsSuperAdmin()
        && !static::currentEmployeeHasPermission(self::PERMISSION_VIEW_ALL_COMPANY)) {
        if (static::currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY)) {
            $companyId = static::currentCompanyId();
            $query->where(function (Builder $q) use ($companyId, $employeeId) {
                $companyId === null ? $q->whereNull('company_id') : $q->where('company_id', $companyId);
                $q->orWhere('created_by', $employeeId)
                  ->orWhere('approved_id', $employeeId)
                  ->orWhere('accounting_approved_id', $employeeId);
            });
        } else {
            $query->where(function (Builder $q) use ($employeeId) {
                $q->where('created_by', $employeeId)
                  ->orWhere('approved_id', $employeeId)
                  ->orWhere('accounting_approved_id', $employeeId);
            });
        }
    }

    // Nháp của người khác luôn ẩn — đúng ERP :222-226.
    return $query->where(function (Builder $q) use ($employeeId) {
        $q->where('status', '!=', self::STATUS_CREATING)
          ->orWhere(function (Builder $q1) use ($employeeId) {
              $q1->where('status', self::STATUS_CREATING)->where('created_by', $employeeId);
          });
    });
}
```

- [x] **Step 2: Viết `BillPaymentService::searchByFilter()`**

Nhận đủ 12 khoá lọc, port từ ERP `searchByFilter()` :253-320:

`code` (like) · `code_bill_payment_request` (whereHas) · `type` · `created_by` · `created_by_request` (whereHas) · `status` · `department` · `object_id` (whereHas details: `customer_id` HOẶC `supplier_id`) · `money_from` / `money_to` (trên `sum_payment_money_approve_exchange`, bỏ dấu `,`) · `start_date` / `end_date` (trên `created_at`).

⚠️ ERP viết `->where('customer_id', ...)->whereOr('supplier_id', ...)` — `whereOr` **không phải** method của Laravel query builder, đây là **lỗi ERP**. HRM viết đúng:

```php
$query->whereHas('details', function (Builder $q) use ($objectId) {
    $q->where('customer_id', $objectId)->orWhere('supplier_id', $objectId);
});
```

Eager load: `['billPaymentRequest.employee_create.info', 'details', 'employeeCreate.info', 'paymentDepartment']`.

⚠️ **KHÔNG** eager load `billPaymentRequest.department` — entity `BillPaymentRequest` của feature trước **không khai quan hệ `department()`** (đã verify: chỉ có `details`, `currency`, `employee_create`, `employee_update`, 4 quan hệ approver) và **bị cấm sửa**. Dùng sẽ nổ `Call to undefined relationship` lúc chạy. Tra tên phòng ban theo lô bằng 1 query `DB::table('departments')`.

⚠️ **Ô lọc "Phòng ban" lệch ERP CÓ CHỦ Ý.** ERP lọc `bill_payments.department_id` (`searchByFilter()` :266-268) — đó là phòng ban của **kế toán lập phiếu** — trong khi cột hiển thị lại lấy phòng ban của **phiếu đề nghị** (nhánh A) hoặc `payment_department` (loại 4). Tức bộ lọc ERP không khớp chính cột nó đứng cạnh. HRM lọc theo **đúng cột đang hiện** (`payment_department_id` OR `billPaymentRequest.department_id`).

Sắp xếp mặc định `created_at DESC`. Cho phép sort: `code` · `sum_payment_money_approve_exchange` · `created_at` · `updated_at` · `status`.

- [x] **Step 3: Viết `BillPaymentListResource`**

Trả 14 field khớp cột màn danh sách (spec §11.1): `id` · `code` · `bill_payment_request_id` · `bill_payment_request_code` · `type` · `type_text` · `object_name` · `sum_payment_money_approve_exchange` · `created_by_request_name` · `department_name` · `created_at` (`d/m/Y H:i`) · `created_by_name` · `updated_at` (`d/m/Y H:i`) · `updated_by_name` · `status` · `status_text` · `status_type` + 7 cờ `is_can_*` (Task 4 điền, tạm trả `false` hết ở task này).

`object_name` port từ ERP `searchData()` :70-81, **mở rộng cho loại 12 và 4**:

```php
/**
 * Cột "Khách hàng / Nhà cung cấp" — nội dung đổi theo loại chi.
 * Tiêu đề cột đổi so với ERP ("Khách hàng") vì bảng `customers` chứa CẢ KH lẫn NCC
 * (`is_customer` / `is_supplier`) — spec §11.1.
 */
private function objectName(): ?string
{
    $detail = $this->details->first();
    if (!$detail) {
        return null;
    }

    $type = $this->billPaymentRequest->type ?? $this->type;

    if (in_array($type, [2, 6], true)) {
        return trim($detail->customer_code . '-' . $detail->customer_name, '-') ?: null;
    }
    if (in_array($type, [1, 12], true)) {
        return trim($detail->supplier_code . '-' . $detail->supplier_name, '-') ?: null;
    }

    return null; // loại 4 để trống (đối tượng là nhiều nhân viên)
}
```

- [x] **Step 4: Viết `BillPaymentController::index()` + route**

Controller kế thừa `ApiController` như `BillIncomeController`. Docblock đầu class phải ghi rõ **vì sao không dùng middleware `checkPermission`** (spec §7.2).

Route thêm vào `Routes/api.php`, ngay sau group `/bill-incomes`:

```php
    // Phiếu chi tiền (bảng ERP `bill_payments` trên DB gộp).
    // KHÔNG gắn middleware quyền — xem docblock BillPaymentController.
    Route::group(['prefix' => '/bill-payments'], function () {
        Route::get('/', [BillPaymentController::class, 'index']);
        // Route TĨNH phải khai TRƯỚC /{id} để không bị route động nuốt.
        Route::get('/accounts', [BillPaymentController::class, 'accounts']);
        Route::get('/search-payment-requests', [BillPaymentController::class, 'searchPaymentRequests']);
        Route::get('/payment-employees', [BillPaymentController::class, 'paymentEmployees']);
        Route::get('/{id}', [BillPaymentController::class, 'show']);
        Route::get('/{id}/print-data', [BillPaymentController::class, 'printData']);
        Route::get('/{id}/export', [BillPaymentController::class, 'export']);
        Route::post('/', [BillPaymentController::class, 'store']);
        Route::put('/{id}', [BillPaymentController::class, 'update']);
        Route::delete('/{id}', [BillPaymentController::class, 'destroy']);
        Route::post('/{id}/submit', [BillPaymentController::class, 'submit']);
        Route::post('/{id}/approve', [BillPaymentController::class, 'approve']);
        Route::post('/{id}/cancel', [BillPaymentController::class, 'cancel']);
    });
```

Ở task này chỉ implement `index()`; các action còn lại khai method rỗng ném `abort(501)` để route đăng ký được, Task sau điền dần.

- [x] **Step 5: Verify — lint + gọi thật**

```bash
php -l Modules/Finance/Services/BillPaymentService.php
php -l Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php
php -l Modules/Finance/Http/Controllers/V1/BillPaymentController.php
php artisan route:list --path=bill-payments
```
Kỳ vọng: 13 route hiện ra, `php -l` sạch.

- [x] **Step 6: Verify phạm vi quyền bằng dữ liệu thật**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
use Modules\Human\Entities\Employee;
foreach ([<id nhân viên có quyền tổng cty>, <id chỉ có quyền công ty>, <id không quyền>] as \$id) {
    auth()->loginUsingId(\$id);
    echo \$id, ' => ', BillPayment::applyScope(BillPayment::query())->count(), PHP_EOL;
}
"
```

⚠️ **Bẫy đã dính**: auth guard cache theo tiến trình — chạy nhiều danh tính trong **1** process thì lần 2 trở đi vẫn dùng danh tính đầu. Phải chạy **mỗi id 1 lệnh tinker riêng**, đừng gộp vòng lặp rồi kết luận là fail-open.

Kỳ vọng: người có quyền tổng công ty ≥ người chỉ có quyền công ty ≥ người không quyền; không ai thấy phiếu nháp của người khác.

---

## Task 4: Gate quyền (`BillPaymentAccess`) + `BillPaymentDetailResource` + `show`

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentAccess.php` (trait)
- Modify: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php` (dùng trait)
- Create: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentDetailResource.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`show()`)
- Modify: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php` (nối 7 cờ thật)

**Interfaces:**
- Produces: 7 method `canView()` · `canEdit()` · `canDelete()` · `canSubmit()` · `canApprove()` · `canCancel()` · `canExport()` trên `BillPayment`. **Màn danh sách và màn chi tiết đọc CÙNG bộ cờ này** — bẫy đã dính ở feature trước (2 màn lệch số nút).

- [x] **Step 1: Viết trait `BillPaymentAccess`**

```php
/** Người lập phiếu, đang ở trạng thái nháp, và có quyền kế toán thanh toán. */
public function canEdit(): bool
{
    return $this->status === self::STATUS_CREATING
        && $this->created_by === auth()->id()
        && static::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTANT);
}

public function canDelete(): bool
{
    return $this->canEdit();
}

public function canSubmit(): bool
{
    return $this->canEdit();
}

/**
 * Duyệt — tự nhận biết cấp theo trạng thái hiện tại.
 * status 5 (chỉ nhánh B) → Kế toán trưởng · status 2 → Thủ quỹ.
 */
public function canApprove(): bool
{
    if (!$this->isSameCompanyAsCurrentEmployee()) {
        return false;
    }
    if ($this->status === self::STATUS_AWAITING_ACCOUNTING_APPROVE) {
        return static::currentEmployeeHasPermission(self::PERMISSION_CHIEF_ACCOUNTANT);
    }
    if ($this->status === self::STATUS_AWAITING_APPROVE) {
        return static::currentEmployeeHasPermission(self::PERMISSION_TREASURER);
    }

    return false;
}

public function canCancel(): bool
{
    return $this->canApprove();
}
```

`canView()` port ERP `canView()` :760-796 (đã có docblock sẵn bên ERP, logic khớp `applyScope`).

`isSameCompanyAsCurrentEmployee()` — dùng `static::currentCompanyId()` của trait; **hai vế cùng `null` KHÔNG coi là cùng công ty** (trait đã ghi rõ lý do).

- [x] **Step 2: Viết `BillPaymentDetailResource`**

Ngoài field đầu phiếu, trả `details` (mảng dòng chi tiết đủ cột theo nhánh), `bill_payment_request` (tóm tắt phiếu đề nghị nguồn), và 7 cờ `is_can_*` lấy thẳng từ 7 method Task này. Ngày trả sẵn `d/m/Y` / `d/m/Y H:i`, tiền trả số thô (FE format).

- [x] **Step 3: Nối 7 cờ thật vào `BillPaymentListResource`**

Thay 7 giá trị `false` tạm ở Task 3 bằng `$this->canEdit()`, … — **đúng cùng 7 method**, không viết lại điều kiện.

- [x] **Step 4: Viết `show()`**

```php
public function show($id)
{
    $bill = BillPayment::with([...])->findOrFail($id);
    if (!$bill->canView()) {
        abort(403, 'Bạn không có quyền xem phiếu chi này.');
    }

    return $this->responseSuccess(new BillPaymentDetailResource($bill));
}
```

- [x] **Step 5: Verify — 7 cờ khớp giữa 2 màn**

```bash
php -l Modules/Finance/Entities/BillPayment/BillPaymentAccess.php
php -l Modules/Finance/Transformers/BillPaymentResource/BillPaymentDetailResource.php
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
auth()->loginUsingId(<id nhân viên có quyền Thủ quỹ>);
\$b = BillPayment::where('status', 2)->first();
echo json_encode(['edit'=>\$b->canEdit(),'delete'=>\$b->canDelete(),'submit'=>\$b->canSubmit(),'approve'=>\$b->canApprove(),'cancel'=>\$b->canCancel()]), PHP_EOL;
"
```
Kỳ vọng: `approve` và `cancel` = true, `edit`/`delete`/`submit` = false (phiếu đã gửi duyệt).

- [x] **Step 6: Verify không có cờ nào hard-code true**

```bash
grep -rnE "is_can_[a-z_]*'\s*=>\s*true" Modules/Finance/Transformers/BillPaymentResource/
```
Kỳ vọng: **0 kết quả**.

---

# Phase 2 — Tạo / sửa / xóa nháp + gửi duyệt (nhánh A)

## Task 5: Popup chọn Phiếu đề nghị chi + endpoint `accounts`

**Files:**
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`searchPaymentRequests()`, `accounts()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentService.php` (thêm `searchAvailableRequests()`)

**Interfaces:**
- Consumes: `BillPaymentRequest` (entity feature trước, **KHÔNG sửa**) — quan hệ snake_case.
- Produces: `GET /v1/finance/bill-payments/search-payment-requests` và `/accounts`. Task 19 (FE) dùng.

- [x] **Step 1: Viết `searchAvailableRequests()`**

Lọc **cứng** `status = BillPaymentRequest::STATUS_AWAITING_CREATE_BILL_PAYMENT` (= 6) — đúng ERP (`formJs.blade.php`: `d.status = 6`).

Loại bỏ phiếu **đã có phiếu chi** trỏ tới:

```php
$query->whereNotExists(function ($q) {
    $q->selectRaw('1')
      ->from('bill_payments')
      ->whereColumn('bill_payments.bill_payment_request_id', 'bill_payment_requests.id');
});
```
(bản SQL của cùng luật `existsForRequest()` — dùng ở tầng danh sách nên phải là subquery, không gọi được helper PHP theo từng dòng.)

⚠️ **KHÔNG lọc trạng thái phiếu chi** — đúng ERP: hủy phiếu chi là **ngõ cụt**, không lập lại được (spec §5.5 điểm hở #2, user chốt giữ nguyên).

⚠️ Luật "1 đề nghị chỉ 1 phiếu chi" xuất hiện ở **3 nơi** (task này · Task 6 `guardOneBillPerRequest()` · Task 23 cờ `is_can_create_bill_payment`). Viết lại 3 lần là chắc chắn lệch nhau. Khai **1 helper duy nhất** trên entity ở Task 3 và dùng chung cả 3 chỗ:

```php
/** Đề nghị $requestId đã có phiếu chi chưa. KHÔNG lọc trạng thái — xem spec §5.5 điểm hở #2. */
public static function existsForRequest(int $requestId, ?int $exceptBillId = null): bool
{
    return static::query()
        ->where('bill_payment_request_id', $requestId)
        ->when($exceptBillId, function ($q) use ($exceptBillId) { return $q->where('id', '!=', $exceptBillId); })
        ->exists();
}
```

Cho lọc theo `code`, `type`, khoảng ngày; phân trang 10.

- [x] **Step 2: Viết `accounts()`**

Trả danh sách tài khoản cho 2 ô `Tài khoản có` / `Tài khoản nợ`. Copy nguyên `BillIncomeController::accounts()`.

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
use Modules\Finance\Services\BillPaymentService;
auth()->loginUsingId(<id kế toán thanh toán>);
echo app(BillPaymentService::class)->searchAvailableRequests([])->count(), PHP_EOL;
"
mysql -h127.0.0.1 -uroot gop_db -e "
SELECT COUNT(*) ky_vong FROM bill_payment_requests r
WHERE r.status = 6 AND NOT EXISTS (SELECT 1 FROM bill_payments b WHERE b.bill_payment_request_id = r.id);"
```
Kỳ vọng: 2 số **bằng nhau**.

---

## Task 6: `BillPaymentWriteService` — tạo / sửa nháp (nhánh A)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentStoreRequest.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentUpdateRequest.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`store()`, `update()`)

**Interfaces:**
- Produces: `BillPaymentWriteService::store(array $data): BillPayment` · `update(BillPayment $bill, array $data): BillPayment` · **`public function syncDetails(BillPayment $bill, array $details): void`**.
  ⚠️ `syncDetails()` bắt buộc **public** — Task 10 gọi nó từ `BillPaymentApprovalFlowService` (service khác).
  `guardOneBillPerRequest()` là **private**, KHÔNG phải interface công khai.

**Khuôn để copy:** `Services/BillIncomeWriteService.php` (239 dòng).

- [x] **Step 1: Viết `BillPaymentStoreRequest`**

Luật theo spec §9.1 / §9.2, **rẽ nhánh theo `type`**:

```php
public function rules(): array
{
    $rules = [
        'type'        => 'required|integer',
        'account_has' => 'required|exists:accounts,id',
        'receiver'    => 'required|string|max:255',
        'details'     => 'required|array|min:1',
        'details.*.account_dept' => 'required|exists:accounts,id',
    ];

    if (in_array((int) $this->input('type'), BillPayment::TYPES_FROM_REQUEST, true)) {
        $rules['bill_payment_request_id'] = 'required|exists:bill_payment_requests,id';
        $rules['details.*.payment_money_approve'] = 'nullable|numeric|min:0';
        $rules['details.*.product_export_requests.*.allocated_value'] = 'required|numeric|min:0';
    }

    if ((int) $this->input('type') === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
        $rules['payment_department_id'] = 'required|exists:departments,id';
        $rules['type_payment']  = 'required';
        $rules['type_money_id'] = 'required';
        $rules['exchange_rate'] = 'required|numeric';
        $rules['reason']        = 'required|string';
        foreach (['payment_diff_employee', 'payment_commission_month', 'payment_commission_quarter',
                  'payment_commission_bonus_quarter', 'payment_delivery_money', 'payment_other_cost'] as $col) {
            $rules['details.*.' . $col] = 'required|numeric';
        }
    }

    return $rules;
}
```

`messages()` tiếng Việt cho từng khoá.

⚠️ **KHÔNG** khai luật `note` — bảng không có cột `note`, lý do hủy xử lý riêng ở Task 11.

- [x] **Step 2: Viết `BillPaymentUpdateRequest`**

Kế thừa luật của Store. ⚠️ **Đây là chỗ sửa lỗi ERP #2**: ERP khai `BillPaymentUpdateRequest` nhưng `update()` lại nhận `BillPaymentStoreRequest` nên luật update **chưa bao giờ chạy**. Controller HRM phải type-hint **đúng** `BillPaymentUpdateRequest`.

- [x] **Step 3: Viết `guardOneBillPerRequest()`**

```php
/**
 * 1 Đề nghị thanh toán chỉ được có 1 Phiếu chi. KHÔNG lọc theo trạng thái phiếu chi — đúng
 * ERP: hủy phiếu chi là ngõ cụt, đề nghị không lập lại phiếu khác được (spec §5.5 điểm hở #2,
 * user chốt GIỮ NGUYÊN, không phải bug cần sửa).
 */
private function guardOneBillPerRequest(int $requestId, ?int $exceptBillId = null): void
{
    if (BillPayment::existsForRequest($requestId, $exceptBillId)) {
        abort(422, 'Đề nghị thanh toán đã lập phiếu chi tiền.');
    }
}
```

- [x] **Step 4: Viết `syncDetails()`**

Port ERP `syncDetails()` :373-446 — xóa hết dòng cũ (kèm bảng phân bổ) rồi tạo lại, cộng dồn 2 cột tổng vào phiếu.

⚠️ **KHÔNG** truyền 4 cột `payment_market_cost`, `payment_extra`, `cost_debt_id`, `type_payment_employee` — không tồn tại trong DB (spec §4).

- [x] **Step 5: Viết `store()` + `update()`**

`store()`: bọc `DB::transaction`, sinh mã bằng `BillPayment::generateCode()`, `guardOneBillPerRequest()` (chỉ nhánh A), tạo phiếu ở `STATUS_CREATING`, `syncDetails()`.

⚠️ **Khác ERP có chủ ý**: ERP `store()` còn nhận `status` trong payload để vừa tạo vừa gửi duyệt. HRM **luôn tạo ở trạng thái nháp**; gửi duyệt là endpoint riêng (Task 8). FE bấm "Lưu và gửi duyệt" thì gọi 2 API tuần tự.

`update()`: gate `canEdit()`, trả **423** nếu không:

```php
if (!$bill->canEdit()) {
    abort(423, 'Phiếu chi đã bị khóa, không sửa được.');
}
```

- [x] **Step 6: Verify — tạo thật rồi xóa sạch**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
\$svc = app(Modules\Finance\Services\BillPaymentWriteService::class);
\$bill = \$svc->store([...payload nhánh A tối thiểu...]);
echo \$bill->code, ' | details=', \$bill->details()->count(), ' | status=', \$bill->status, PHP_EOL;
DB::rollBack();
echo 'rolled back', PHP_EOL;
"
```
Kỳ vọng: in mã đúng dạng `<cty>.PC<mmyy>.00001`, `status=1`, rồi rollback.

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT COUNT(*) FROM bill_payments;"
```
Kỳ vọng: **1302** — đúng baseline, không sót bản ghi test.

---

## Task 7: Xóa nháp (`destroy`)

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (`destroy()`)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`destroy()`)

**Interfaces:**
- Produces: `BillPaymentWriteService::destroy(BillPayment $bill): void` · `DELETE /v1/finance/bill-payments/{id}`.

- [x] **Step 1: Viết `destroy()`**

```php
/**
 * Sửa LỖI ERP #1: `BillPaymentController::delete()` không kiểm quyền lẫn trạng thái —
 * gọi thẳng URL là xóa được phiếu đã duyệt của người khác.
 */
public function destroy(BillPayment $bill): void
{
    if (!$bill->canDelete()) {
        abort(423, 'Phiếu chi đã bị khóa, không xóa được.');
    }

    DB::transaction(function () use ($bill) {
        $detailIds = $bill->details()->pluck('id');
        BillPaymentDetailProductExportRequest::whereIn('bill_payment_detail_id', $detailIds)->delete();
        $bill->details()->delete();
        $bill->delete();
    });
}
```

⚠️ **KHÔNG** trả trạng thái phiếu đề nghị về — đúng ERP, an toàn vì nháp chưa hề đụng phiếu đề nghị (spec §5.5 điểm hở #1).

- [x] **Step 2: Verify — thử xóa phiếu đã duyệt phải bị chặn**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
auth()->loginUsingId(<id kế toán thanh toán>);
\$b = BillPayment::where('status', 3)->first();
try { app(Modules\Finance\Services\BillPaymentWriteService::class)->destroy(\$b); echo 'FAIL - xóa được!', PHP_EOL; }
catch (\Throwable \$e) { echo 'OK ', \$e->getStatusCode(), PHP_EOL; }
"
```
Kỳ vọng: in `OK 423`. In `FAIL` → gate hỏng, dừng lại sửa.

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT COUNT(*) FROM bill_payments;"
```
Kỳ vọng: **1302**.

---

## Task 8: Gửi duyệt (`submit`) + đồng bộ ngược + chuông

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php`
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (`submit()`)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`submit()`)

**Interfaces:**
- Consumes: `ChecksEmployeePermission::employeeInfoIdsHavingPermission(string, ?int): int[]` (đã có trong trait).
- Produces: `BillPaymentWriteService::submit(BillPayment $bill): BillPayment` · `BillPaymentNotifyService::notifySubmitted(BillPayment $bill): void`.

**Khuôn để copy:** `Services/BillPaymentRequestNotifyService.php` (feature trước, cùng phân hệ).

- [x] **Step 1: Viết `submit()` — rẽ 2 nhánh**

```php
/**
 * Gửi duyệt. Nhánh A (loại 1/2/6/12) -> Chờ chi tiền (2), báo Thủ quỹ.
 * Nhánh B (loại 4)                   -> Chờ KT trưởng duyệt (5), báo Kế toán trưởng.
 *
 * ⚠️ KHÔNG gán `accounting_approved_id` ở đây. ERP gán = người ĐANG ĐĂNG NHẬP lúc gửi duyệt,
 * tức người LẬP phiếu chứ không phải người duyệt (`BillPaymentController::store()` :175-180 và
 * `update()` :233-236) — lỗi ERP #8, HRM ghi ở đúng bước KT trưởng bấm duyệt (Task 15).
 */
public function submit(BillPayment $bill): BillPayment
{
    if (!$bill->canSubmit()) {
        abort(423, 'Phiếu chi đã bị khóa, không gửi duyệt được.');
    }

    return DB::transaction(function () use ($bill) {
        $isPaymentEmployee = (int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE;

        $bill->status = $isPaymentEmployee
            ? BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE
            : BillPayment::STATUS_AWAITING_APPROVE;
        $bill->save();

        if (!$isPaymentEmployee) {
            // Đồng bộ ngược: đề nghị -> 7 "Chờ duyệt phiếu chi" (spec §5.5).
            BillPaymentRequest::query()
                ->where('id', $bill->bill_payment_request_id)
                ->update(['status' => BillPaymentRequest::STATUS_AWAITING_APPROVE_BILL_PAYMENT]);
        }

        $this->notifyService->notifySubmitted($bill);

        return $bill;
    });
}
```

- [x] **Step 2: Viết `BillPaymentNotifyService::notifySubmitted()`**

Người nhận = `BillPayment::employeeInfoIdsHavingPermission($permission, $bill->company_id)`.

⚠️ Chọn `$permission` theo **TRẠNG THÁI HIỆN TẠI của phiếu**, không theo `type` — vì Task 15 gọi lại
chính hàm này ở bước 2 nhánh B (lúc đó `type` vẫn là 4 nhưng người cần báo đã là **Thủ quỹ**):

```php
$permission = $bill->status === BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE
    ? BillPayment::PERMISSION_CHIEF_ACCOUNTANT   // status 5 -> KT trưởng
    : BillPayment::PERMISSION_TREASURER;         // status 2 -> Thủ quỹ (cả nhánh A lẫn bước 2 nhánh B)
```

Chọn theo `type` là bug: phiếu loại 4 sau khi KT trưởng duyệt sẽ báo nhầm lại cho chính KT trưởng, Thủ quỹ không bao giờ nhận được thông báo.

Nội dung theo `notification-convention`: `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`, tên phiếu ≤ 50 ký tự và **in đậm**, tổng ≤ 120 ký tự, deep-link `/finance/bill-payments/<id>`.

- [x] **Step 3: Verify — luồng gửi duyệt, rollback sau khi kiểm**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
use Modules\Finance\Entities\BillPayment\BillPayment;
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$bill = BillPayment::where('status', 1)->first();
\$reqId = \$bill->bill_payment_request_id;
app(Modules\Finance\Services\BillPaymentWriteService::class)->submit(\$bill);
echo 'bill=', \$bill->fresh()->status, ' request=', BillPaymentRequest::find(\$reqId)->status, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: in `bill=2 request=7`.

- [x] **Step 4: Verify `accounting_approved_id` KHÔNG bị gán khi gửi duyệt**

Trong cùng lệnh trên, in thêm `\$bill->fresh()->accounting_approved_id`. Kỳ vọng: `null`.

---

# Phase 3 — Duyệt + ghi sổ cái (nhánh A)

## Task 9: `BillPaymentAccountingService::buildEntries()` + unit test

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentAccountingService.php`
- Create: `hrm-api/Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php`

**Interfaces:**
- Consumes: `AccountDetailEntry` · `AccountDetailRef` (đã có).
- Produces: `BillPaymentAccountingService::buildEntries(array $input): array{entries: array, refs: array}` (**hàm thuần**, không DB không auth) · **`public function persist(array $built): void`** — chỉ insert, mọi dữ liệu cần thiết đã nằm trong `$built`. Task 10 gọi.

**Khuôn để copy:** `Services/BillIncomeAccountingService.php` (253 dòng) — copy nguyên cấu trúc `buildEntries()` / `creditEntry()` / `debitEntry()` / `persist()`, đảo chiều Nợ ↔ Có và đổi 4 nhánh theo loại chi.

- [x] **Step 1: Viết test TRƯỚC — nhánh loại 1 (chi trả NCC)**

```php
public function test_loai_1_ghi_1_dong_no_va_1_dong_co()
{
    $built = (new BillPaymentAccountingService())->buildEntries([
        'bill' => ['id' => 999, 'account_has' => 2, 'code' => 'TP.PC0825.00001', 'date_accounting' => '2026-08-19', 'company_id' => 1, 'department_id' => 2, 'part_id' => 3],
        'request' => ['type' => 1, 'type_money_id' => 1, 'exchange_rate' => 1, 'created_by' => 10],
        'creator' => ['id' => 10, 'company_id' => 1, 'department_id' => 2, 'part_id' => 3],
        'details' => [[
            'account_dept' => 31, 'supplier_id' => 7, 'payment_money_approve' => 1000000,
            'payment_money_approve_exchange' => 1000000, 'contractable_id' => null, 'contractable_type' => null,
        ]],
        'account_identify_numbers' => [2 => '1111', 31 => '3311'],
    ]);

    $this->assertCount(2, $built['entries']);
    $this->assertSame(AccountDetailEntry::TYPE_DEBT, $built['entries'][0]['type']);
    $this->assertSame(31, $built['entries'][0]['account_id']);
    $this->assertSame(AccountDetailEntry::TYPE_HAS, $built['entries'][1]['type']);
    $this->assertSame(2, $built['entries'][1]['account_id']);
    $this->assertSame(1000000.0, $built['entries'][1]['money_value']);
    $this->assertSame('App\Model\IncomeExpenditure\BillPayment', $built['entries'][0]['invoiceable_type']);
}
```

Viết thêm 3 test: **loại 6** (`employee_id` = người lập đề nghị, `work_id` = `TTHHD`, `group_id` = 1) · **loại 12** (`billable_type` = `DeliveryTripAccounting`, `supplier_id` lấy từ chuyến xe) · **dòng 0 đồng bị bỏ qua** (`payment_money_approve <= 0 && payment_money_approve_exchange <= 0` → `continue`).

- [x] **Step 2: Chạy test để chắc chắn nó FAIL**

```bash
cd D:/laragon/www/hrm/hrm-api && php artisan test Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php
```
Kỳ vọng: FAIL — `Class "BillPaymentAccountingService" not found`.

- [x] **Step 3: Viết `buildEntries()`**

Hằng số đầu class:

```php
const INVOICEABLE_TYPE   = 'App\Model\IncomeExpenditure\BillPayment';
const PRODUCT_EXPORT_TYPE = 'App\Model\Warehouse\ProductExport';
const DELIVERY_TRIP_TYPE  = 'App\Model\Delivery\DeliveryTripAccounting';
const OTHER_DELIVERY_TRIP_TYPE = 'App\Model\Delivery\OtherDeliveryTripAccounting';
const DECLARE_DEBT_TYPE   = 'App\Model\Accounting\DeclareDebtBeginning';
```
(4 chuỗi cuối phải khớp kết quả grep ở Task 2 Step 6.)

Cấu trúc port ERP `saveAccountsDetail()` :538-690, **4 nhánh** đúng thứ tự `if` của ERP: có phân bổ phiếu xuất hàng → loại 6 → loại 12 → còn lại. Mỗi dòng **Nợ** kèm 1 ref trỏ `account_has`. Sau vòng lặp, nếu tổng > 0 thì thêm **1 dòng Có** trên `account_has` kèm ref trỏ **từng `account_dept` khác nhau** (lọc trùng).

⚠️ Chiều Nợ/Có **ngược với phiếu thu**: phiếu chi ghi Nợ trên `account_dept` của từng dòng và Có trên `account_has` của phiếu.

15 cột denormalize (`identify_number`, `invoiceable_code`, `invoiceable_date_accounting`, `contractable_code`, …) điền **tường minh trong `buildEntries()`**, không dựa vào hook — giống `BillIncomeAccountingService`.

- [x] **Step 4: Chạy test để chắc chắn PASS**

```bash
php artisan test Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php
```
Kỳ vọng: 4 test PASS.

- [x] **Step 5: Viết `persist()`**

Chỉ insert, không tính toán: `AccountDetailEntry::create()` từng dòng, lấy id thật rồi `AccountDetailRef::create()` theo `entry_index`. Copy nguyên `BillIncomeAccountingService::persist()`.

- [x] **Step 6: Verify đối chiếu ngược với dữ liệu ERP đã ghi**

Với **5 phiếu đã duyệt của mỗi loại chi 1 / 2 / 6 / 12**: dựng lại bút toán bằng `buildEntries()` rồi diff từng trường với `account_details` + `account_detail_refs` mà cổng ERP đã ghi.

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
foreach ([1,2,6,12] as \$type) {
  \$bills = BillPayment::where('type', \$type)->where('status', 3)->limit(5)->get();
  foreach (\$bills as \$b) {
    \$erp = DB::table('account_details')
      ->where('invoiceable_type', 'App\\\\Model\\\\IncomeExpenditure\\\\BillPayment')
      ->where('invoiceable_id', \$b->id)->orderBy('id')->get();
    // dựng lại bằng buildEntries() và so từng cột: account_id, type, money_value,
    // money_value_exchange, customer_id, supplier_id, employee_id, contractable_*, billable_*, work_id
    echo \$b->code, ' erp_rows=', \$erp->count(), PHP_EOL;
  }
}
"
```
Kỳ vọng: **số dòng và từng trường khớp 100%**. Lệch dù 1 phiếu → **DỪNG**, báo user, không đi tiếp Task 10.

⚠️ Chỉ **ĐỌC**, tuyệt đối không ghi gì vào `account_details` ở step này.

---

## Task 10: Duyệt nhánh A (`approve`) — khóa dòng, ghi sổ, đồng bộ ngược

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentApproveRequest.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`approve()`)

**Interfaces:**
- Consumes: `BillPaymentAccountingService::buildEntries()` + `persist()` (Task 9).
- Produces: `BillPaymentApprovalFlowService::approve(int $id, array $details): BillPayment` · `syncPaymentMoneyApprove(BillPayment $bill, array $details): void`.

**Khuôn để copy:** `Services/BillIncomeApprovalService.php` (411 dòng).

- [x] **Step 1: Viết `approve()` — khóa dòng + chặn duyệt lại**

```php
/**
 * ⚠️ Ghi vào sổ cái DÙNG CHUNG với cổng ERP — duyệt 2 lần là nhân đôi bút toán, không hoàn
 * tác được. ERP không chặn (`BillPaymentController::update()` :255-275 chỉ đổi status).
 * HRM khóa dòng + kiểm lại trạng thái trong transaction, trả 409.
 */
public function approve(int $id, array $details): BillPayment
{
    return DB::transaction(function () use ($id, $details) {
        $bill = BillPayment::query()->lockForUpdate()->findOrFail($id);

        if (!$bill->canApprove()) {
            abort(403, 'Bạn không có quyền duyệt phiếu chi này.');
        }
        if ($bill->status === BillPayment::STATUS_APPROVED) {
            abort(409, 'Phiếu chi đã được duyệt trước đó.');
        }

        // Kiểm trần số tiền — sửa LỖI ERP #3: ERP chỉ chạy validatePaymentMoney() khi
        // `status != 4`, mà 4 là *Hủy* còn duyệt là 3, nên ERP KHÔNG hề kiểm lúc duyệt.
        $this->guardPaymentMoneyCeiling($bill, $details);

        $this->writeService->syncDetails($bill, $details);
        ...
    });
}
```

Nhánh A sau khi đổi trạng thái:
1. `status = STATUS_APPROVED`, `date_accounting = now()->format('Y-m-d')`, `approved_id = auth()->id()`.
2. Đề nghị → `STATUS_APPROVED_BILL_PAYMENT` (8).
3. `syncPaymentMoneyApprove()` — đồng bộ `payment_money_approve(_exchange)` xuống `bill_payment_request_details`, khớp **8 khóa** (spec §5.5), chỉ ghép khóa nào có mặt trong payload.
4. Ghi sổ: `$this->accountingService->persist($this->accountingService->buildEntries($input), ...)`.
5. Log riêng: mã phiếu · số dòng sổ cái · tổng tiền.
6. Chuông báo người lập.

- [x] **Step 2: Viết `guardPaymentMoneyCeiling()`**

Nhánh A: từng dòng `payment_money_approve ≤ payment_money_request`. Vượt → `abort(422, 'Số tiền chi không được vượt quá số dư!')` (nguyên văn ERP).

- [x] **Step 3: Verify — duyệt thật trong transaction rồi rollback**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id thủ quỹ>);
\$before = DB::table('account_details')->count();
\$bill = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class)->approve(<id phiếu status 2>, [...]);
\$after = DB::table('account_details')->count();
echo 'status=', \$bill->status, ' rows_added=', \$after - \$before, PHP_EOL;
DB::rollBack();
echo 'final=', DB::table('account_details')->count(), PHP_EOL;
"
```
Kỳ vọng: `status=3`, `rows_added` > 0, và `final` **bằng đúng** con số baseline trước khi chạy.

- [x] **Step 4: Verify chặn duyệt lại trả 409**

Gọi `approve()` lần 2 trên phiếu vừa duyệt (trong cùng transaction). Kỳ vọng: ném lỗi **409**, `account_details` không tăng thêm dòng nào.

- [x] **Step 5: Verify baseline sổ cái nguyên vẹn**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr, (SELECT COUNT(*) FROM bill_payments) bp;"
```
Kỳ vọng: khớp đúng baseline Task 1 Step 2.

---

## Task 11: Hủy phiếu (`cancel`)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentCancelRequest.php`
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (`cancel()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php` (**thêm `notifyCancelled()`**)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`cancel()`)

**Interfaces:**
- Produces: `BillPaymentApprovalFlowService::cancel(int $id, string $reason): BillPayment` · `BillPaymentNotifyService::notifyCancelled(BillPayment $bill, string $reason): void` (người nhận = **người lập phiếu**, lý do hủy nằm trong nội dung thông báo — đây là nơi DUY NHẤT lý do hủy tồn tại).

- [x] **Step 1: Viết `BillPaymentCancelRequest`**

```php
public function rules(): array
{
    return ['reason' => 'required|string|max:500'];
}

public function messages(): array
{
    return [
        'reason.required' => 'Vui lòng nhập lý do hủy phiếu chi.',
        'reason.max'      => 'Lý do hủy không được quá 500 ký tự.',
    ];
}
```

- [x] **Step 2: Viết `cancel()`**

```php
/**
 * Hủy phiếu chi.
 *
 * ⚠️ Lý do hủy KHÔNG được lưu xuống DB: bảng `bill_payments` không có cột `note`, còn cột
 * `reason` đang giữ *Lý do chi* — ghi đè là mất dữ liệu gốc. ERP cũng bắt nhập rồi bỏ đi
 * (`BillPaymentStoreRequest`: `'note' => Rule::requiredIf($this->status == 4)`).
 * User chốt 2026-08-19: giữ hành vi ERP, đưa lý do vào NỘI DUNG THÔNG BÁO CHUÔNG gửi người
 * lập, không thêm cột (feature này không migration). Spec §9.1.
 */
public function cancel(int $id, string $reason): BillPayment
{
    return DB::transaction(function () use ($id, $reason) {
        $bill = BillPayment::query()->lockForUpdate()->findOrFail($id);

        if (!$bill->canCancel()) {
            abort(403, 'Bạn không có quyền hủy phiếu chi này.');
        }

        $bill->status = BillPayment::STATUS_CANCEL;
        $bill->save();

        // Nhánh B không có phiếu đề nghị -> không đồng bộ ngược.
        if ($bill->bill_payment_request_id) {
            BillPaymentRequest::query()
                ->where('id', $bill->bill_payment_request_id)
                ->update(['status' => BillPaymentRequest::STATUS_CANCEL]);
        }

        $this->notifyService->notifyCancelled($bill, $reason);

        return $bill;
    });
}
```

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id thủ quỹ>);
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$bill = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class)->cancel(<id phiếu status 2>, 'Test hủy');
echo 'bill=', \$bill->status, ' request=', BillPaymentRequest::find(\$bill->bill_payment_request_id)->status, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: in `bill=4 request=9`.

---

# Phase 4 — Nhánh B: loại 4 "Chi thu nhập cho nhân viên"

## Task 12: `PaymentEmployeeLookupService` — hút số liệu nhân viên theo phòng ban

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PaymentEmployeeLookupService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`paymentEmployees()`)

**Interfaces:**
- Produces: `PaymentEmployeeLookupService::forDepartment(int $departmentId, ?int $accountId): array` · `GET /v1/finance/bill-payments/payment-employees?department_id=&account_id=`. Task 20 (FE) dùng.

**Nguồn ERP:** `AccountDetail::getDataAdPaymentEmployee()` :3933 (đọc), `BillPaymentController::getDataPaymentEmployee()` :320-390 (biến đổi).

- [x] **Step 1: Lấy bảng mã công việc**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT id, code, name FROM works WHERE code IN ('TTHHD','TNST','TNSQ','TT','TVC','CPK');"
```
Ghi lại 6 id thật. Thiếu mã nào → **DỪNG**, báo user (không tự chế mã).

- [x] **Step 2: Viết truy vấn `forDepartment()`**

`GROUP BY employee_id` trên `account_details`, mỗi khoản:

```sql
SUM(CASE WHEN work_id = :work AND type = 2 THEN money_value_exchange ELSE 0 END)
- SUM(CASE WHEN work_id = :work AND type = 1 THEN money_value_exchange ELSE 0 END)
```

6 khoản ↔ 6 mã công việc: `diff_employee`←`TTHHD` · `commission_month`←`TNST` · `commission_quarter`←`TNSQ` · `commission_bonus_quarter`←`TT` · `delivery_money`←`TVC` · `other_cost`←`CPK`.

Lọc theo phòng ban qua `employee_department_id`. **Bỏ** nhân viên có cả 6 khoản = 0 (đúng ERP :360-368).

- [x] **Step 3: Viết phần biến đổi output**

Mỗi nhân viên trả: `employee_id` · `employee_code` · `employee_name` · `account_number` · `bank_name` · `bank_branch` · 6 khoản đề nghị · 6 khoản `payment_*`. Quy tắc mặc định của ERP :341-355 — nếu **tổng 6 khoản > 0** thì `payment_*` = khoản tương ứng, ngược lại = 0.

- [x] **Step 4: Verify trên dữ liệu thật**

```bash
php artisan tinker --execute="
\$rows = app(Modules\Finance\Services\PaymentEmployeeLookupService::class)->forDepartment(<id phòng ban có phiếu loại 4>, null);
echo count(\$rows), PHP_EOL;
echo json_encode(\$rows[0] ?? null, JSON_UNESCAPED_UNICODE), PHP_EOL;
"
```
Kỳ vọng: ra danh sách nhân viên, không nhân viên nào có cả 6 khoản = 0.

- [x] **Step 5: Verify đối chiếu với 1 phiếu loại 4 đã duyệt**

Lấy 1 phiếu `type = 4, status = 3`, đọc `payment_department_id`, gọi `forDepartment()` với phòng ban đó và so **danh sách nhân viên** với `bill_payment_details` của phiếu. Lệch nhiều → xem lại cách lọc phòng ban (ERP lọc qua `employee_department_id` trên sổ cái, không phải qua bảng nhân sự).

---

## Task 13: Tạo / sửa / gửi duyệt nhánh B

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (nhánh loại 4 trong `store()` / `update()` / `syncDetails()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (mở rộng `guardPaymentMoneyCeiling()` cho 6 khoản nhánh B)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php` (người nhận là KT trưởng)

**Interfaces:**
- Consumes: `PaymentEmployeeLookupService` (Task 12).
- Produces: nhánh loại 4 của `store()` / `update()` / `submit()` — không tham số mới.

- [x] **Step 1: Nhánh loại 4 trong `store()`**

Bỏ qua `guardOneBillPerRequest()` (không có phiếu đề nghị). Khoá cứng theo ERP `changeType()` (`formJs.blade.php:44-50`):

```php
if ((int) $data['type'] === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
    $data['bill_payment_request_id'] = null;
    $data['account_has']  = 2;   // tài khoản tiền mặt 1111 — ERP khoá cứng ở FE, HRM khoá ở BE
    $data['type_money_id'] = 1;  // VND
}
```

⚠️ **Khoá ở BE, không chỉ ở FE** — ERP chỉ khoá ở FE nên gọi thẳng API là lách được.

- [x] **Step 2: `syncDetails()` cho nhánh B**

Ghi 12 cột thu nhập (6 đề nghị + 6 `payment_*`) + `employee_id/code/name` + `account_dept`. **Không** ghi `customer_id`/`supplier_id`/`contractable_*`.

- [x] **Step 3: Trần số tiền nhánh B trong `guardPaymentMoneyCeiling()`**

Port `validatePaymentMoney()` của ERP :448-467 — với mỗi trong 6 khoản:

```php
if (abs($detail[$requestCol]) < abs($detail[$paymentCol]) && (float) $detail[$paymentCol] != 0.0) {
    abort(422, 'Số tiền chi không được vượt quá số dư!');
}
```

- [x] **Step 4: Verify — tạo + gửi duyệt phiếu loại 4, rollback**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
\$svc = app(Modules\Finance\Services\BillPaymentWriteService::class);
\$bill = \$svc->store([...payload loại 4, lấy details từ PaymentEmployeeLookupService...]);
echo 'account_has=', \$bill->account_has, ' money=', \$bill->type_money_id, ' req=', var_export(\$bill->bill_payment_request_id, true), PHP_EOL;
\$svc->submit(\$bill);
echo 'status=', \$bill->fresh()->status, ' acc_approved=', var_export(\$bill->fresh()->accounting_approved_id, true), PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: `account_has=2 money=1 req=NULL`, rồi `status=5 acc_approved=NULL`.

- [x] **Step 5: Verify BE khoá cứng, không tin FE**

Gọi `store()` với `type = 4` nhưng payload cố tình gửi `account_has = 99`, `type_money_id = 7`. Kỳ vọng: bản ghi vẫn ra `account_has = 2`, `type_money_id = 1`.

---

## Task 14: `PaymentEmployeeAccountingService::buildEntries()` + unit test

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PaymentEmployeeAccountingService.php`
- Create: `hrm-api/Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php`

**Interfaces:**
- Produces: `PaymentEmployeeAccountingService::buildEntries(array $input): array{entries: array, refs: array}` (**hàm thuần**) · `persist(array $built): void`. Task 15 gọi.

**Nguồn ERP:** `BillPayment::saveAccountsDetailEmployee()` :691-732 + 2 helper `AccountDetail::createDataSaveDept()` :897 và `saveAccountDetail()` :989 — **cả 2 helper phải port**, đặt private trong service này, không nhét vào entity chỉ-đọc.

- [x] **Step 1: Đọc kỹ 2 helper ERP trước khi viết**

```bash
sed -n '897,1060p' /d/laragon/www/erp/app/Model/Accounting/AccountDetail.php
```
Ghi ra giấy: `createDataSaveDept()` gom theo khoá nào, `saveAccountDetail()` ghi ra bao nhiêu dòng.

- [x] **Step 2: Viết test TRƯỚC — 1 nhân viên, 2 khoản dương**

```php
public function test_mot_nhan_vien_hai_khoan_duong()
{
    $built = (new PaymentEmployeeAccountingService())->buildEntries([
        'bill' => ['id' => 999, 'account_has' => 2, 'payment_department_id' => 5, 'code' => 'TP.PC0825.00002', 'date_accounting' => '2026-08-19'],
        'payment_department' => ['id' => 5, 'company_id' => 1],
        'account_has_identify_number' => '1111',
        'works' => ['TTHHD' => 11, 'TNST' => 12, 'TNSQ' => 13, 'TT' => 14, 'TVC' => 15, 'CPK' => 16],
        'details' => [[
            'employee_id' => 77, 'payment_money_approve' => 3000000,
            'account_identify_number' => '3341',
            'payment_diff_employee' => 2000000, 'payment_commission_month' => 1000000,
            'payment_commission_quarter' => 0, 'payment_commission_bonus_quarter' => 0,
            'payment_delivery_money' => 0, 'payment_other_cost' => 0,
        ]],
    ]);

    // 2 dòng Nợ theo 2 khoản dương + 1 dòng Có tổng 3.000.000 trên account_has
    $debits = array_values(array_filter($built['entries'], fn ($e) => $e['type'] === AccountDetailEntry::TYPE_DEBT));
    $credits = array_values(array_filter($built['entries'], fn ($e) => $e['type'] === AccountDetailEntry::TYPE_HAS));
    $this->assertCount(2, $debits);
    $this->assertCount(1, $credits);
    $this->assertSame(3000000.0, $credits[0]['money_value']);
    $this->assertSame(11, $debits[0]['work_id']);
    $this->assertSame(5, $debits[0]['employee_department_id']);
    $this->assertSame(1, $debits[0]['employee_company_id']);
}
```

Viết thêm 2 test: **khoản âm đảo chiều** (`payment_other_cost = -500000` → dòng ghi `TYPE_HAS`, `money_value = 500000`, và tổng âm ra **1 dòng Nợ** trên `account_has`) · **dòng `payment_money_approve` rỗng bị bỏ qua**.

- [x] **Step 3: Chạy test để chắc chắn FAIL**

```bash
php artisan test Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php
```
Kỳ vọng: FAIL — class chưa tồn tại.

- [x] **Step 4: Viết `buildEntries()`**

Với mỗi dòng chi tiết có `payment_money_approve`, sinh 6 bút toán theo bảng spec §6.2. Quy tắc dấu:

```php
// ERP: createDataSaveDept(..., abs($value), $value > 0 ? TYPE_DEBT : TYPE_HAS, [1111], [...])
$type = $value > 0 ? AccountDetailEntry::TYPE_DEBT : AccountDetailEntry::TYPE_HAS;
$money = abs($value);
```

⚠️ ERP có **lỗi thiếu `> 0`** ở khoản thưởng quý: `$detail->payment_commission_bonus_quarter ? TYPE_DEBT : TYPE_HAS` (dùng truthy thay vì so sánh) — nghĩa là giá trị **âm** cũng ra `TYPE_DEBT`. Port **đúng theo 5 khoản còn lại** (`> 0`), và ghi chú lệch này trong docblock để người review biết đây là chủ ý.

Cuối cùng 2 dòng tổng trên `account_has`: 1 dòng **Có** = tổng các khoản dương, 1 dòng **Nợ** = tổng trị tuyệt đối các khoản âm; `refs` = danh sách `identify_number` đã dùng.

- [x] **Step 5: Chạy test để chắc chắn PASS**

```bash
php artisan test Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php
```
Kỳ vọng: 3 test PASS.

- [x] **Step 6: Verify đối chiếu ngược 5 phiếu loại 4 đã duyệt**

Giống Task 9 Step 6 nhưng cho `type = 4`: dựng lại bằng `buildEntries()`, diff từng trường với `account_details` mà ERP đã ghi (`invoiceable_id` = id phiếu).

Kỳ vọng: khớp 100%. Lệch → **DỪNG**, báo user. Đây là nhánh nguy hiểm nhất của feature (cơ chế gộp theo `identify_number`).

---

## Task 15: Duyệt 2 cấp nhánh B

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (rẽ nhánh trong `approve()`)

**Interfaces:**
- Consumes: `PaymentEmployeeAccountingService` (Task 14).
- Produces: `approve()` xử lý được cả 2 cấp của nhánh B — không đổi chữ ký.

- [x] **Step 1: Rẽ nhánh theo trạng thái trong `approve()`**

```php
// Nhánh B bước 1 — Kế toán trưởng duyệt: chỉ chuyển sang Chờ chi tiền, CHƯA ghi sổ cái.
if ($bill->status === BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE) {
    $bill->status = BillPayment::STATUS_AWAITING_APPROVE;
    // Sửa LỖI ERP #8: ERP gán `accounting_approved_id` = người LẬP lúc gửi duyệt.
    $bill->accounting_approved_id = auth()->id();
    $bill->save();

    $this->notifyService->notifySubmitted($bill); // -> Thủ quỹ
    return $bill;
}
```

Bước 2 (Thủ quỹ, `status = 2`) dùng chung code với nhánh A, chỉ khác **service ghi sổ**:

```php
$accountingService = (int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE
    ? $this->paymentEmployeeAccountingService
    : $this->accountingService;
```

Và **bỏ qua** 2 việc chỉ có ở nhánh A: cập nhật trạng thái đề nghị (8) và `syncPaymentMoneyApprove()` — nhánh B không có phiếu đề nghị.

- [x] **Step 2: Đảm bảo ghi sổ nằm TRONG transaction**

```php
/**
 * ⚠️ Khác ERP CÓ CHỦ Ý: ERP đẩy phần ghi sổ nhánh B vào job HandleAccountingPaymentEmployee
 * (ShouldQueue). HRM chạy QUEUE_CONNECTION=sync nên job vẫn chạy ngay, NHƯNG nằm ngoài
 * transaction của controller -> ghi sổ hỏng thì phiếu vẫn "Đã duyệt" mà sổ cái trống.
 * HRM gọi thẳng service trong CÙNG transaction, hỏng thì rollback cả hai. Spec §6.4.
 */
```

**KHÔNG** tạo Job, **KHÔNG** `dispatch()`.

- [x] **Step 3: Verify luồng 2 cấp**

```bash
php artisan tinker --execute="
DB::beginTransaction();
\$svc = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class);
\$before = DB::table('account_details')->count();
auth()->loginUsingId(<id kế toán trưởng>);
\$b = \$svc->approve(<id phiếu loại 4 status 5>, [...]);
echo 'sau KT truong: status=', \$b->status, ' acc=', \$b->accounting_approved_id, ' rows=', DB::table('account_details')->count() - \$before, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: `status=2`, `acc=<id kế toán trưởng>`, `rows=0` — **bước 1 chưa ghi sổ cái**.

- [x] **Step 4: Verify bước 2 mới ghi sổ**

Chạy tiếp `approve()` với danh tính **thủ quỹ** (lệnh tinker **riêng** — auth guard cache theo tiến trình). Kỳ vọng: `status=3` và `account_details` tăng đúng số dòng `buildEntries()` trả về. Rollback sau khi kiểm.

- [x] **Step 5: Verify baseline sổ cái**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Kỳ vọng: khớp đúng baseline Task 1 Step 2.

---

# Phase 5 — In & Xuất Excel

## Task 16: `BillPaymentPrintService` — 3 mẫu, 2 liên

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentPrintService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`printData()`)

**Interfaces:**
- Produces: `BillPaymentPrintService::render(BillPayment $bill): array{html: string, template_id: int}` · `GET /v1/finance/bill-payments/{id}/print-data`. Task 22 (FE) dùng.

**Khuôn để copy:** `Services/BillIncomePrintService.php` (686 dòng) — đã có sẵn cơ chế đọc `report_templates`, `fillReport()`, `clearNull()`.

- [x] **Step 1: Xác nhận 3 mẫu còn trong DB**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT id, name, CHAR_LENGTH(template) len FROM report_templates WHERE id IN (211,217,236);"
```
Kỳ vọng: 3 dòng — `211` (~3.079) · `217` (~2.091) · `236` (~3.887). Thiếu mẫu nào → **DỪNG**, báo user.

- [x] **Step 2: Viết `render()` — chọn mẫu theo loại chi**

```php
/** Port ERP `BillPaymentController::print()` :392-432. */
private function pickTemplateId(BillPayment $bill): int
{
    if ((int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
        return self::TEMPLATE_PAYMENT_EMPLOYEE; // 236, in 1 liên
    }
    if ((int) $bill->type === 12) {
        return self::TEMPLATE_SINGLE; // 211
    }

    return $bill->details()->count() === 1 ? self::TEMPLATE_SINGLE : self::TEMPLATE_MULTI; // 211 / 217
}
```

Ghép 2 liên: mẫu **211** → nối `<br>` × 9 giữa 2 liên (cùng 1 trang A4); mẫu **217** → chèn `<div class="page-break active"></div>`; mẫu **236** → **1 liên**, không ghép.

Liên 1 gọi `getPrintData($bill, 1)`, liên 2 gọi `getPrintData($bill, 2)` — tham số `numberDebit` của ERP quyết định nhãn liên.

- [x] **Step 3: Verify — dựng bản in cho 1 phiếu mỗi loại**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
\$svc = app(Modules\Finance\Services\BillPaymentPrintService::class);
foreach ([1,2,6,12,4] as \$t) {
  \$b = BillPayment::where('type', \$t)->where('status', 3)->first();
  if (!\$b) { echo \$t, ' - khong co phieu', PHP_EOL; continue; }
  \$r = \$svc->render(\$b);
  echo \$t, ' template=', \$r['template_id'], ' len=', strlen(\$r['html']), PHP_EOL;
}
"
```
Kỳ vọng: loại 4 → `236`; loại 12 → `211`; loại 1/2/6 → `211` hoặc `217` tùy số dòng chi tiết; `len` > 0 và **không còn chuỗi `{{`** nào chưa thay.

- [x] **Step 4: Verify không sót placeholder**

```bash
php artisan tinker --execute="
\$r = app(Modules\Finance\Services\BillPaymentPrintService::class)->render(Modules\Finance\Entities\BillPayment\BillPayment::where('status',3)->first());
preg_match_all('/\{\{[^}]+\}\}/', \$r['html'], \$m);
echo count(\$m[0]), ' placeholder con lai', PHP_EOL;
"
```
Kỳ vọng: `0 placeholder con lai`.

---

## Task 17: Xuất Excel 1 phiếu

**Files:**
- Create: `hrm-api/Modules/Finance/Exports/BillPaymentExport.php`
- Create: `hrm-api/Modules/Finance/Resources/views/exports/bill-payment.blade.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`export()`)

**Interfaces:**
- Produces: `GET /v1/finance/bill-payments/{id}/export` → tải `phieu_chi_tien_<mã>.xlsx`.

**Nguồn ERP:** `app/ExcelExports/BillPaymentExcel.php` + `BillPayment::excelBillPaymentTable()` :1236 và `excelBillPaymentWithExchangeTable()` :1124.

- [x] **Step 1: Viết blade export**

2 biến thể theo ERP: có tỷ giá (`excelBillPaymentWithExchangeTable`) và không (`excelBillPaymentTable`). Chọn theo `type_money_id != 1`.

- [x] **Step 2: Viết `export()` trong controller**

Gate bằng `canView()` (giống In). Trả `Excel::download()`.

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
auth()->loginUsingId(<id có quyền xem>);
\$b = Modules\Finance\Entities\BillPayment\BillPayment::where('status',3)->first();
\$file = (new Modules\Finance\Exports\BillPaymentExport(\$b))->raw(Maatwebsite\Excel\Excel::XLSX);
echo strlen(\$file), ' bytes', PHP_EOL;
"
```
Kỳ vọng: > 0 bytes, không exception.

---

# Phase 6 — Frontend

## Task 18: Màn danh sách `index.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/index.vue`

**Interfaces:**
- Consumes: `GET /v1/finance/bill-payments`, `GET /v1/finance/bill-payments/accounts`.
- Produces: route `/finance/bill-payments`.

**Khuôn để copy:** `hrm-client/pages/finance/bill-incomes/index.vue` (827 dòng) — copy pattern rồi đổi cột/bộ lọc.

- [x] **Step 1: Kiểm khoá cấu hình cột không trùng màn khác**

```bash
cd D:/laragon/www/hrm/hrm-client && grep -rn "finance_bill_payments" pages/ components/
```
Kỳ vọng: **0 kết quả** trước khi viết. Có kết quả → đổi khoá, báo user.

- [x] **Step 2: Dựng khung màn**

4 mixin bắt buộc: `PageTitleMixin` · `CheckPermission` · `filterStateMixin` · `columnCustomizationMixin`. `localStorageKey` = `columnScreenKey` = `'finance_bill_payments'`.

14 cột theo spec §11.1. Cột **Mã phiếu** là `<nuxt-link>` thật (chuột phải mở tab mới được), đặt `locked: true` cùng STT và Hành động. Sắp xếp mặc định `created_at DESC`.

Bảng trống hiện dòng **"Không có dữ liệu phù hợp"**. Phân trang mặc định 10, chọn 5/10/20/50/100, đổi số dòng nhảy về trang 1. STT dùng `getNumericalOrder(currentPage, pageSize, index)` — **không** `index + 1`.

- [x] **Step 3: Dựng bộ lọc**

10 trường (spec §11.1) → **có** popup "Cài đặt bộ lọc", **bỏ** khối nâng cao. Ô chọn tự tìm ngay khi chọn; ô gõ tay chờ Enter/nút Tìm kiếm. Placeholder `Chọn <X>` / `Nhập <X>` — **không** `Tất cả`, **không** `Chọn...`. Nút **Làm mới** xóa hết điều kiện **và** tải lại danh sách. Panel lọc **bỏ prop `title`**, dùng mặc định "Bộ lọc danh sách".

- [x] **Step 4: Cột hành động + toolbar**

Toolbar: **Thêm mới → Cấu hình cột** (màn này không có Import / Xuất danh sách).

Cột hành động: **Sửa → Xóa → menu "…"** (In · Xuất Excel · Duyệt · Hủy). Nút không dùng được thì **ẩn hẳn** (`visible` / `v-if`), **không** `disabled` (`V2BaseButton` không có prop đó). Không có nút "Xem chi tiết".

⚠️ `V2BaseRowActions` emit **chuỗi key**, so `action === 'edit'` chứ không phải `action.key`.

Mọi cờ quyền khởi tạo `false`, chỉ gán từ `is_can_*` của BE.

- [x] **Step 5: Verify — parse + kiểm cờ quyền**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/index.vue','utf8');
const t=s.match(/<template>([\s\S]*)<\/template>/)[1];
const r=c.compile(t);
console.log(r.errors.length? r.errors : 'template OK');
"
grep -nE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payments/index.vue
```
Kỳ vọng: `template OK` và grep **0 kết quả**.

⚠️ **Không** dùng `npx eslint` làm cổng verify — hrm-client không có ESLint config và fail trên Node 14.

- [x] **Step 6: Verify icon có thật trong font local**

```bash
grep "^\.ri-" assets/scss/custom/plugins/icons/_remixicon.scss | grep -E "<tên icon đã dùng>"
```
Kỳ vọng: mỗi icon dùng trong màn đều có 1 dòng. Thiếu → đổi icon khác, không để icon trống.

---

## Task 19: Form nhánh A + `create.vue` / `_id/edit.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/create.vue`
- Create: `hrm-client/pages/finance/bill-payments/_id/edit.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/BillPaymentForm.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/PaymentRequestSearchModal.vue`

**Interfaces:**
- Consumes: `GET /search-payment-requests`, `GET /accounts`, `POST /`, `PUT /{id}`, `POST /{id}/submit`.
- Produces: component `BillPaymentForm` với prop `value` (object phiếu) và `mode` (`'create' | 'edit'`).

**Khuôn để copy:** `pages/finance/bill-incomes/components/BillIncomeForm.vue` (1.018 dòng) và `IncomeRequestSearchModal.vue` (274 dòng). Khuôn form chuẩn là `CustomerForm.vue` — ⚠️ **không** chép khuôn từ `ProductTransferRequestForm.vue` (class `form-card` / `form-header` nằm trong `<style>` riêng của màn đó, không có ở v2-styles).

- [x] **Step 1: Viết `PaymentRequestSearchModal.vue`**

Popup chọn phiếu đề nghị. Mọi select trong popup dùng **`V2BaseSelectInModal`**, không `V2BaseSelect`.

⚠️ `V2BaseSelect` là select2 — **không có** prop `reduce` / `label`.
⚠️ **Không** đặt prop tên `errors` hoặc `fields` — vee-validate chiếm 2 tên đó, prop bị che, chỉ lộ khi mở trình duyệt.

- [x] **Step 2: Viết `BillPaymentForm.vue` — khối đầu phiếu nhánh A**

Chọn phiếu đề nghị → tự đổ và **khoá chỉ đọc**: Loại chi · Hình thức TT · Loại tiền · Tỷ giá · Lý do chi · Người đề nghị · Phòng ban. Tự nhập: Tài khoản có · Người nhận.

Ô chọn trong bảng dùng `V2BaseInput` readonly + popup, **không** tự chế nút.

- [x] **Step 3: Bảng chi tiết nhánh A**

Cột: Tài khoản nợ · Đối tượng (KH/NCC/NV) · Hợp đồng · Số tiền đề nghị chi · **Số tiền chi** · Ghi chú. Tiền căn phải, định dạng `.` ngăn nghìn `,` ngăn thập phân.

- [x] **Step 4: Validate + unsaved-changes**

Chỉ trường **Tên/bắt buộc tối thiểu** gắn `required` ở FE; required còn lại do BE trả 422. Lỗi hiện **inline ngay dưới ô** (`is-invalid` + `invalid-feedback`), dùng cờ `touched` để chỉ hiện sau lần submit đầu. Còn lỗi → **không gọi API**, con trỏ nhảy về ô lỗi đầu tiên.

Dùng `unsavedChangesMixin` (page) + gọi `markFormSaved()` sau khi lưu thành công. Chưa đổi gì mà bấm Hủy → **không** hiện popup confirm.

⚠️ Chọn đúng mixin theo kiểu màn — sai mixin thì popup **không bao giờ** hiện (xem mục 2b của `unsaved-changes/SKILL.md`).

- [x] **Step 5: 2 nút lưu**

Nút trong `V2Footer`, **không** tự dựng khối nút. "Lưu nháp" → `POST /` hoặc `PUT /{id}`. "Lưu và gửi duyệt" → lưu xong gọi tiếp `POST /{id}/submit`.

⚠️ Lưu dữ liệu dùng `apiPostMethod` với khoá `payload`, **không** phải `apiPost`.

- [x] **Step 6: Verify parse cả 4 file**

```bash
cd D:/laragon/www/hrm/hrm-client
for f in pages/finance/bill-payments/create.vue pages/finance/bill-payments/_id/edit.vue pages/finance/bill-payments/components/BillPaymentForm.vue pages/finance/bill-payments/components/PaymentRequestSearchModal.vue; do
  node -e "
  const c=require('vue-template-compiler'),fs=require('fs');
  const s=fs.readFileSync('$f','utf8');
  const t=(s.match(/<template>([\s\S]*)<\/template>/)||[])[1];
  const r=c.compile(t||'');
  console.log('$f', r.errors.length? r.errors : 'OK');
  "
done
grep -rnE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payments/
grep -rn "V2BaseSelect\b" pages/finance/bill-payments/components/PaymentRequestSearchModal.vue
```
Kỳ vọng: 4 dòng `OK`; 2 grep cuối **0 kết quả** (trong modal phải là `V2BaseSelectInModal`).

---

## Task 20: Bảng nhánh B `PaymentEmployeeTable.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/components/PaymentEmployeeTable.vue`
- Modify: `hrm-client/pages/finance/bill-payments/components/BillPaymentForm.vue` (rẽ nhánh theo Loại chi)

**Interfaces:**
- Consumes: `GET /v1/finance/bill-payments/payment-employees?department_id=`.
- Produces: component nhận `department_id`, emit `input` là mảng `details` nhánh B.

- [x] **Step 1: Rẽ nhánh trong `BillPaymentForm.vue`**

Loại chi = 4 → ẩn khối chọn phiếu đề nghị, hiện ô **Phòng ban chi**; Tài khoản có và Loại tiền hiện **chỉ đọc** (BE khoá cứng ở Task 13, FE chỉ hiển thị cho khớp).

- [x] **Step 2: Viết `PaymentEmployeeTable.vue`**

Đổi phòng ban → gọi API hút số liệu → đổ bảng. Cột: STT · Số tài khoản nợ · Tên tài khoản · Nhân viên · 6 khoản (đề nghị / thực chi) · Số TK ngân hàng · Tên ngân hàng · Chi nhánh · Tổng cộng. Dòng **Tổng cộng** cuối bảng.

Ô "thực chi" cho sửa, chặn vượt khoản đề nghị ngay tại FE (BE vẫn kiểm lại — Task 13 Step 3).

- [x] **Step 3: Nút lưu nhánh B**

"Lưu và gửi KT trưởng duyệt" thay cho "Lưu và gửi duyệt" — cùng gọi `POST /{id}/submit`, BE tự rẽ sang trạng thái 5.

- [x] **Step 4: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/components/PaymentEmployeeTable.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'OK');
"
```
Kỳ vọng: `OK`.

---

## Task 21: Màn chi tiết + popup duyệt

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/_id/index.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/ApproveBillPaymentModal.vue`

**Interfaces:**
- Consumes: `GET /{id}`, `POST /{id}/approve`, `POST /{id}/cancel`.

**Khuôn để copy:** `pages/finance/bill-incomes/_id/index.vue` (352 dòng) và `ApproveBillIncomeModal.vue` (326 dòng).

- [x] **Step 1: Dựng màn chi tiết**

Tiêu đề `Chi tiết phiếu chi: <mã>`, số phiếu hiện ngay dưới tiêu đề. Trạng thái dùng `V2BaseBadge`, text từ `status_text` của BE — **không** map số → chữ ở FE. Ô rỗng in `—`.

⚠️ Hành động ở màn chi tiết phải **khớp hệt** màn danh sách — cả danh sách nút lẫn điều kiện ẩn/hiện, đọc từ **cùng bộ cờ `is_can_*`**. Đây là bẫy đã dính (2 màn lệch số nút).

- [x] **Step 2: Viết `ApproveBillPaymentModal.vue`**

Nhập số tiền thực chi từng dòng rồi gửi `POST /{id}/approve`. Nhánh B hiện 6 khoản thay vì 1 ô số tiền.

Popup xác nhận dùng `base-confirm-modal` / `$confirm()`, **không** tự khai `b-modal`.

- [x] **Step 3: Nút Hủy phiếu**

Bắt buộc nhập lý do hủy (BE trả 422 nếu thiếu). Hiện rõ cho user biết lý do này **đi vào thông báo** gửi người lập.

- [x] **Step 4: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
for f in pages/finance/bill-payments/_id/index.vue pages/finance/bill-payments/components/ApproveBillPaymentModal.vue; do
  node -e "
  const c=require('vue-template-compiler'),fs=require('fs');
  const s=fs.readFileSync('$f','utf8');
  const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
  console.log('$f', r.errors.length? r.errors : 'OK');
  "
done
grep -rn "b-modal" pages/finance/bill-payments/components/ApproveBillPaymentModal.vue
```
Kỳ vọng: 2 dòng `OK`; grep `b-modal` **0 kết quả**.

---

## Task 22: Trang in `_id/print.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/_id/print.vue`

**Interfaces:**
- Consumes: `GET /{id}/print-data`.

**Khuôn để copy:** `pages/finance/bill-incomes/_id/print.vue` (359 dòng).

- [x] **Step 1: Dựng trang in**

Nhận HTML đã đổ mẫu từ BE, render vào khung giấy A4.

⚠️ `hrm-client/static/css/pdf.css` **không tồn tại** mà plugin in lại khai nạp → phải **tự bù rule** vào `options.styles`. **KHÔNG** thêm file vào `static/` (thư mục dùng chung toàn hệ thống). Bài học từ `finance-bill-adjust-dept-request`.

- [x] **Step 2: Kiểm các lỗi in hay gặp**

Đọc `.claude/skills/print-page/SKILL.md` và kiểm: viền phải/dưới khi sang trang · nội dung cột bị cắt · logo/letterhead · tự bật hộp thoại in (không bắt user Ctrl+P) · ô gộp `rowspan` khi in nhiều trang.

- [x] **Step 3: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/_id/print.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'OK');
"
grep -rn "pdf.css" pages/finance/bill-payments/_id/print.vue
```
Kỳ vọng: `OK`; grep `pdf.css` **0 kết quả** (rule phải nằm inline trong `options.styles`).

---

## Task 23: Menu + nút "Tạo phiếu chi" ở màn Đề nghị thanh toán

**Files:**
- Modify: `hrm-client/components/subsystem-menu/finance.js:83`
- Modify: `hrm-client/pages/finance/bill-payment-requests/_id/index.vue` (thêm nút)
- Modify: `hrm-api/Modules/Finance/Transformers/BillPaymentRequestResource/*` (thêm cờ `is_can_create_bill_payment`)

**Interfaces:**
- Produces: cờ BE `is_can_create_bill_payment` trên resource chi tiết Đề nghị thanh toán.

⚠️ **Đây là màn ĐÃ NGHIỆM THU** — phải test lại luồng cũ của nó sau khi sửa.

- [x] **Step 1: Gắn link menu**

Đổi `{ label: 'Phiếu chi' }` (dòng 83) thành:

```js
            { label: 'Phiếu chi', link: '/finance/bill-payments' },
```

Giữ nguyên 3 mục còn lại của nhóm. Đúng **1 lối vào**, không thêm mục `?mode=`.

- [x] **Step 2: Thêm cờ BE**

```php
/**
 * Đề nghị thanh toán đã đủ điều kiện lập Phiếu chi chưa (spec §11.7).
 * 3 điều kiện: đang ở trạng thái 6 · chưa có phiếu chi nào trỏ tới · có quyền Kế toán thanh toán.
 */
'is_can_create_bill_payment' => $this->status === self::STATUS_AWAITING_CREATE_BILL_PAYMENT
    && !BillPayment::existsForRequest($this->id)
    && BillPayment::currentEmployeeHasPermissionPublic(BillPayment::PERMISSION_ACCOUNTANT),
```

⚠️ `currentEmployeeHasPermission()` trong trait là `protected` — thêm 1 wrapper `public static` trên `BillPayment` thay vì đổi tầm nhìn của trait dùng chung.

- [x] **Step 3: Thêm nút ở màn chi tiết đề nghị**

Nút "Tạo phiếu chi" trong `V2Footer`, `v-if="detail.is_can_create_bill_payment"` (cờ khởi tạo `false`), điều hướng `/finance/bill-payments/create?bill_payment_request_id=<id>`.

- [x] **Step 4: Nhận query param ở `create.vue`**

`create.vue` đọc `$route.query.bill_payment_request_id` → nếu có thì tự nạp phiếu đề nghị vào form, bỏ qua bước mở popup.

- [x] **Step 5: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "require('@babel/parser').parse(require('fs').readFileSync('components/subsystem-menu/finance.js','utf8'),{sourceType:'module'});console.log('menu OK')"
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payment-requests/_id/index.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'detail OK');
"
grep -n "Phiếu chi" components/subsystem-menu/finance.js
```
Kỳ vọng: `menu OK` · `detail OK` · dòng menu có `link: '/finance/bill-payments'`.

- [x] **Step 6: Verify cờ BE trên dữ liệu thật**

```bash
cd D:/laragon/www/hrm/hrm-api && php artisan tinker --execute="
auth()->loginUsingId(<id kế toán thanh toán>);
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$co = BillPaymentRequest::where('status',6)->whereNotExists(function(\$q){\$q->selectRaw('1')->from('bill_payments')->whereColumn('bill_payments.bill_payment_request_id','bill_payment_requests.id');})->count();
\$da = BillPaymentRequest::where('status',6)->whereExists(function(\$q){\$q->selectRaw('1')->from('bill_payments')->whereColumn('bill_payments.bill_payment_request_id','bill_payment_requests.id');})->count();
echo 'duoc tao=', \$co, ' da co phieu=', \$da, PHP_EOL;
"
```
Kỳ vọng: 2 con số hợp lý; phiếu đã có phiếu chi thì cờ phải `false`.

---

## Checkpoint cuối — trước khi báo xong

- [x] Chạy lại toàn bộ unit test: `php artisan test Modules/Finance/Tests/Unit/`
- [x] Đếm lại baseline: `bill_payments` = **1302** · `bill_payment_details` = **3307** · `account_details` / `account_detail_refs` khớp số ghi ở Task 1 Step 2
- [x] `grep -rnE "can[A-Za-z]*\s*=\s*true" hrm-client/pages/finance/bill-payments/` → **0 kết quả**
- [x] `php -l` sạch trên toàn bộ file BE mới
- [x] Chạy checklist tự kiểm mục A–H của `.claude/skills/erp-to-hrm-screen/SKILL.md`
- [x] Báo user **rõ phần chưa kiểm chứng**: nhánh phân bổ phiếu xuất hàng (0 dòng dữ liệu) chỉ verify bằng đọc code; toàn bộ FE chưa mở trình duyệt
- [x] Cập nhật `plan.md` (đánh `[x]`) + `.plans/gop-db/STATUS.md`


---

### Checkpoint — 2026-08-19

Vua hoan thanh: TOAN BO 23/23 task (6 phase). BE 26 file, FE 9 file. 18/18 unit test PASS.
Dang lam do: khong con task nao trong plan.
Buoc tiep theo: user tu mo trinh duyet nghiem thu; quyet 5 diem con treo (xem design.md muc "Diem con treo").
Blocked: khong co.

**Luu y khi doc lai plan nay**: mot so step verify trong plan mo ta lenh khong chay duoc tren may nay
(`php artisan route:list`, `php artisan tinker <file>`) — da thay bang cach khac, ghi trong ledger.
Mot so step co ket qua LECH voi mo ta ban dau cua plan (namespace morph, ten bang, mau badge, cot
Khach hang/NCC, chu ky service, ten class ApprovalFlow) — plan va spec DA duoc sua theo du lieu that;
ly do tung thay doi ghi trong ledger `<scratchpad>/sdd/finance-bill-payment/progress.md`.

### Sửa lỗi file Excel xuất phiếu chi — 2026-08-20 (user yêu cầu, cùng bộ lỗi của Phiếu thu)

Cùng 3 triệu chứng đã sửa ở `.plans/gop-db/finance-bill-income/plan.md` mục F1-F5: thiếu logo
letterhead, cột quá hẹp, cột số tiền bị Excel cảnh báo "The number in this cell is formatted as
text". Phiếu chi nặng hơn Phiếu thu vì có **3 bố cục** (default / delivery / employee).

- [x] G1. `BillPaymentPrintService`: các hàm dựng bảng bản EXCEL + ô số tiền xuất SỐ THÔ.
      KHÔNG đụng bản IN.
- [x] G2. `BillPaymentExport` implement `WithColumnWidths` — bề rộng riêng cho từng bố cục.
- [x] G3. `BillPaymentExport` implement `WithDrawings` — nhúng letterhead vào A1 (bỏ quyết định cũ
      "không nhúng ảnh": lý do cũ là `safeImage()` của ERP luôn trả ảnh trong suốt, HRM nay tải
      thẳng URL nên ra ảnh thật).
- [x] G4. `registerEvents()`: tính lại vùng ô tiền theo bố cục (vùng cứng của ERP đang trỏ trượt —
      trước đây vô hại vì ô là chuỗi, nay ô là SỐ nên trỏ trượt = mất dấu phân cách).
- [x] G5. Kiểm chứng: dựng file cho mỗi bố cục, đọc lại xác nhận kiểu ô + bề rộng + drawing.
- [x] G6. Viết `.claude/skills/export-excel/SKILL.md` gói 3 quy tắc này (skill là tài sản chung →
      tạo file, KHÔNG commit, để user đưa qua PR).

**Cách làm chốt lại (khác đề xuất ban đầu ở G4):** không tính lại vùng ô nữa mà bỏ hẳn cơ chế vùng ô.
HTML reader của PhpSpreadsheet đọc thuộc tính `data-format` trên từng thẻ `<td>`
(`Reader/Html.php::processDomElementDataFormat()`), nên mỗi ô tiền tự khai `data-format="#,##0"`
ngay chỗ dựng HTML → không còn phụ thuộc số dòng. Đã áp cùng cách cho Phiếu thu (sửa lại F4).

Phần nhúng letterhead tách thành trait dùng chung
`Modules/Finance/Exports/Concerns/EmbedsCompanyLetterhead.php` (Phiếu thu + Phiếu chi cùng dùng).

**Kết quả kiểm chứng (dựng file thật cho cả 3 bố cục, đọc lại bằng PhpSpreadsheet):**

| Bố cục | Phiếu | Trước | Sau |
| --- | --- | --- | --- |
| default (loại 1) | 918, 25 dòng | cột F dòng 12-36 `General` → `1000000` | F+G `#,##0` từ dòng đầu tới dòng Tổng cộng |
| employee (loại 4) | 290, 20 dòng | ô "Số tiền thực chi" là CHUỖI `"120,058,380"`; bảng kê 2 mất định dạng từ dòng 46; cột Tổng cộng không bao giờ có | tất cả `[n]` + `#,##0`, hết bảng |
| delivery (loại 12) | 1316, 60 dòng | 2 ô tiền khối Liên/Nợ/Có là CHUỖI | `[n]` + `#,##0` |
| Bề rộng cột | cả 3 | A=7.14 · B=14.28 (đổi từ px) | đặt theo bố cục: vd default A=8 · C=30 · D/E=26 |
| Logo | cả 3 | không có | drawing A1, dòng 1 cao 58pt |

Bản IN của cả 3 loại chạy lại vẫn ra số có dấu phân cách như cũ (`render()` không đổi).

**Chưa kiểm chứng:** ảnh letterhead thật (local không với tới `erp.test:8080/uploads/...`) — test
bằng PNG tạm qua `file://`. Phiếu ngoại tệ: DB gộp 0 phiếu, chỉ đối chiếu code.

### Checkpoint — 2026-08-20 (G1-G6)
Vừa hoàn thành: sửa 3 lỗi file Excel phiếu chi + viết skill `.claude/skills/export-excel/SKILL.md`.
Đang làm dở: không có.
Bước tiếp theo: user tải lại Excel phiếu chi (thử cả loại 1, loại 4, loại 12) trên môi trường dev.
Blocked: không.

⚠️ `.claude/skills/export-excel/SKILL.md` và dòng mới trong bảng skill của `CLAUDE.md` là **tài sản
chung** → theo quy tắc team phải đưa qua PR, chưa commit.


---

## Phase I - Logo (letterhead) dung chung cach cua man Bao gia (2026-08-21)

Lam theo yeu cau user ngay sau khi xong ben Phieu thu (xem
`.plans/gop-db/finance-bill-income/plan.md` Phase G + H cho ly do day du).

- [x] I1 - `BillPaymentPrintService::headerUrl()`: lay cong ty theo `bill_payments.company_id`
      truoc, fallback cong ty nguoi tao (ERP lay theo nguoi tao)
- [x] I2 - Thieu `ERP_URL` -> tra nguyen path tuong doi thay vi `''` (dung nhanh
      `return company.header_url || h` cua bao gia)
- [x] I3 - Cap nhat docblock muc 5 cua class + docblock `headerUrl()`
- [x] I4 - Verify ban IN (ca 5 loai phieu / 2 mau 211 + 236) va ban EXCEL

**Chi sua 1 file**: `Modules/Finance/Services/BillPaymentPrintService.php` - 2 dong lenh, con lai
la comment. `BillPaymentExport` da dung san trait `EmbedsCompanyLetterhead` nen khong phai sua.

### Checkpoint - 2026-08-21 (I1-I4)
Vua hoan thanh: logo ban in + Excel phieu chi.

Do tren du lieu that (1.305 phieu chi): **0 phieu mat logo** truoc va sau (nguoi tao deu co
`company_id`), nhung **162 phieu** truoc day in ra logo KHAC cong ty ghi tren phieu -> nay dung.

Verify that:

| | Ket qua |
| --- | --- |
| `TPHP.PC0726.00001` (phieu cty 2, nguoi tao cty 1) | ban in mau 211 -> `.../cn-hp.png` (truoc la `ts-hn.png`) |
| `TPSG.PC0726.00011` (phieu cty 4, nguoi tao cty 5) | `.../tpsg.png` |
| Ca 5 loai phieu (type 1/2/4/6/12, mau 211 + 236) | deu co `<img src="https://erp.eteksofts.com/uploads/...">` |
| File Excel `BillPaymentExport::drawings()` | 1 drawing `letterhead 650x72 @A1` |

**Chua kiem chung:** anh hien that tren trinh duyet - can user mo lai ban in tren dev.
Blocked: khong.

---

## Phase J — Chỉnh nhãn cột màn danh sách (2026-08-22)

- [x] J1 — Đổi tiêu đề cột `createdAt`: "Ngày lập" → **"Ngày tạo"**
      (`hrm-client/pages/finance/bill-payments/index.vue:481`)
- [x] J2 — Đổi tiêu đề cột `createdByName`: "Người lập" → **"Người tạo"**
      (`hrm-client/pages/finance/bill-payments/index.vue:482`)

Chỉ đổi **nhãn hiển thị**, không đụng `key` (`createdAt` / `createdByName`) nên sort, cấu hình
ẩn/hiện cột và payload BE giữ nguyên.

**Chưa đổi (chờ user chốt)** — vẫn đang dùng chữ "lập" trên cùng màn danh sách:
bộ lọc `Ngày lập từ` / `Ngày lập đến` (dòng 53, 64), bộ lọc `Người lập` (dòng 423).
Ngoài màn danh sách: form chi tiết/sửa `BillPaymentForm.vue` (dòng 185, 189) và
popup chọn đề nghị thanh toán `PaymentRequestSearchModal.vue` (dòng 40, 74, 75).

### Checkpoint — 2026-08-22 (J1-J2)
Vừa hoàn thành: đổi nhãn 2 cột trên màn danh sách phiếu chi.
Đang làm dở: không.
Bước tiếp theo: chờ user chốt có đổi luôn nhãn bộ lọc + form chi tiết cho đồng bộ không.
Blocked: không.

## Phase K — Màn IN: chữ đậm không đậm ở PREVIEW (2026-08-22)

**Triệu chứng:** user báo "các text in đậm đang chưa được in đậm" trên màn in phiếu chi,
trong khi màn Phiếu thu hiển thị đúng.

**Root cause (đã xác minh, không đoán):**
- Mẫu in `report_templates` 211 / 217 / 236 đánh đậm HOÀN TOÀN bằng thẻ `<strong>`
  (đếm thực tế: 8 / 11 / 8 thẻ), **không** có `<b>`, **không** có inline `font-weight`.
- `assets/scss/bootstrap.scss:30` nạp `custom/components/_reboot.scss`, file này đặt
  `b, strong { font-weight: $font-weight-medium }` = **500** cho toàn hrm-client.
- Times New Roman không có nét 500 → trình duyệt vẽ ra như chữ thường → preview mất hết chỗ đậm.
- **Chỉ lệch ở PREVIEW.** Cửa sổ in là iframe chỉ nạp `/ckeditor/css/editor.css` +
  `/css/print-app.css`; đã grep, cả 2 file **không có** rule `b, strong` → giữ mặc định `bolder`.
- Màn Phiếu thu đã vá đúng chỗ này từ trước (`bill-incomes/_id/print.vue`), phiếu chi thì chưa.

- [x] K1 — Thêm `#content ::v-deep b, #content ::v-deep strong { font-weight: bold }` vào khối
      `<style lang="scss" scoped>` của `hrm-client/pages/finance/bill-payments/_id/print.vue`,
      kèm comment giải thích y như bản Phiếu thu.

**KHÔNG làm** (có chủ ý): không sửa `_reboot.scss` (file dùng chung toàn hệ thống),
không thêm rule vào `printContentStyles()` (iframe vốn đã đậm đúng, thêm là dư thừa).

### Checkpoint — 2026-08-22 (K1)
Vừa hoàn thành: fix chữ đậm màn in phiếu chi (preview).
Đang làm dở: không.
Bước tiếp theo: user mở lại `/finance/bill-payments/{id}/print` xác nhận preview đã đậm.
Chưa kiểm chứng bằng mắt: hiển thị thật trên trình duyệt (verify bằng đọc CSS + đếm thẻ trong
mẫu in + compile check, chưa mở browser).
Blocked: không.

## Phase L — Màn IN: khối "Liên số" bị vẽ thành bảng kẻ ô (2026-08-22)

**User báo:** "chỗ liên số làm gì có table đâu" — bản in phiếu chi hiện một bảng kẻ ô ở khối
Liên số, ERP/Phiếu thu không có.

**Root cause (đối chiếu mẫu in thật + pdf.css của ERP):**
- BE `BillPaymentPrintService::debitInfo()` đổ vào `{{LIEN}}` một `<table class="table table-bordered">`.
- Trong cả 3 mẫu 211 / 217 / 236, `{{LIEN}}` nằm **trong ô của một bảng `class="no-border"`**.
  ERP tắt viền bằng `.no-border td { border: none !important }` — selector **HẬU DUỆ** nên phủ
  luôn bảng con ⇒ ERP in ra khối Liên số **không viền**.
- `print.vue` phiếu chi lại dùng `#content table:not(.no-border) td { border: 1px solid black !important }`.
  Specificity (1 id, 1 class, 2 element) **thắng** `#content .no-border td` (1 id, 1 class, 1 element)
  ⇒ bảng Liên số bị kẻ viền đen.
- Gốc sâu hơn: file này viết 2026-08-19, **trước** khi `static/css/pdf-erp.css` (bản sao nguyên văn
  `pdf.css` của ERP) được thêm 2026-08-20 cho màn Phiếu thu. Phiếu chi vẫn đang tự bù CSS bằng
  `print-app.css` + `editor.css` + `printContentStyles()` ⇒ lệch ERP ở nhiều chỗ, không chỉ Liên số.

**Đối chiếu mẫu — bảng nào có viền, bảng nào không:**

| Khối | Vị trí trong mẫu | ERP in ra |
| --- | --- | --- |
| Mọi `<table>` có sẵn trong mẫu (letterhead, thông tin, khối ký) | đều `class="no-border"` | không viền |
| `{{LIEN}}` (BE đổ) | trong ô của bảng `.no-border` | **không viền** |
| `{{CHI_TIET}}` (217), `{{BANG_KE_*}}` (236) | ngoài mọi bảng | có viền đen |

- [x] L1 — Iframe in chỉ nạp `/css/pdf-erp.css` (bỏ `print-app.css` + `ckeditor/css/editor.css`),
      body bỏ class `document-editor` — y hệt `bill-incomes/_id/print.vue`
- [x] L2 — `printBaseStyles()` chép đúng khối `<style>` của ERP `print.blade.php::printPDF()`
      (@page, `.MsoBodyTextIndent`, `page-break.active`, `.no-print`) + 2 deviation có chủ ý cho
      bảng `width:827px` (`#content table { max-width:100% }`, `table.block td` nowrap)
- [x] L3 — Xoá `printContentStyles()` (toàn bộ rule đã có sẵn trong pdf-erp.css)
- [x] L4 — `head()` bỏ `link` `/css/print-app.css` (nạp toàn cục sẽ kéo cả sidebar sang font Times)
- [x] L5 — Khối `<style scoped>` preview dựng lại theo đúng pdf.css: `td, th { border 1px black }`
      cho MỌI ô + `.no-border td { border: none !important }` hậu duệ, `#content` khổ A4
      210mm + padding đúng lề in, `line-height: normal`, giữ fix chữ đậm của Phase K

**Có chủ ý bỏ đi so với bản cũ (vì ERP không có, giữ lại là lệch):**
- `word-break / overflow-wrap: break-word` trên ô bảng (user đã bác ở màn Phiếu thu 2026-08-22)
- `thead { display: table-header-group }` — ERP **không** lặp header bảng chi tiết ở trang sau.
  Muốn giữ tính năng này thì thêm lại 1 dòng, nhưng khi đó phiếu chi khác phiếu thu/ERP.
- `-webkit-print-color-adjust: exact` — mẫu in không có nền màu.

### Checkpoint — 2026-08-22 (L1-L5)
Vừa hoàn thành: đưa môi trường CSS bản in phiếu chi về đúng ERP, khối Liên số hết viền.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/{id}/print` cho cả 3 mẫu (loại 1/2/6/12 một chi
tiết → 211, nhiều chi tiết → 217, loại 4 → 236) đối chiếu với bản in ERP.
Chưa kiểm chứng bằng mắt: verify bằng đọc `pdf-erp.css` + dump mẫu 211/217/236 từ DB + tính
specificity + compile check (template/script/scss đều pass), chưa mở trình duyệt.
Blocked: không.

## Phase M — Màn IN: giãn dòng "Ngày … Tháng … Năm …" khỏi hàng chữ ký (2026-08-22)

**User báo:** dòng "Ngày 23 Tháng 07 Năm 2026" và phần bên dưới (hàng chữ ký) quá sát nhau.

**Nguyên nhân:** `pdf.css` của ERP không đặt `margin` cho `table`, cộng thêm deviation
`table.block td { padding: 2px 4px }` (thêm ở Phase L để 5 nhãn chữ ký nằm gọn 1 dòng) → 2 khối
gần như dính. ERP thật cũng vậy → đây là **thay đổi có chủ ý, khác ERP**.

**Mẫu để 2 khối đó ở 2 dạng khác nhau nên phải 2 rule** (đã dump mẫu từ DB để xác nhận):

| Mẫu | Cấu trúc | Rule dùng |
| --- | --- | --- |
| 211, 236 | "Ngày …" và hàng chữ ký là **2 bảng `.block` liền kề** | `table.block + table.block { margin-top: 8mm }` |
| 217 | cả hai nằm trong **1 bảng `.block`**, mỗi khối 1 hàng | `table.block tr + tr td { padding-top: 8mm }` |

Hai rule không chồng nhau: 211/236 mỗi bảng chỉ 1 hàng nên `tr + tr` không khớp; 217 chỉ có 1
bảng `.block` nên `table.block + table.block` không khớp.

- [x] M1 — Thêm 2 rule vào `printBaseStyles()` (cửa sổ in)
- [x] M2 — Thêm 2 rule tương ứng vào `<style scoped>` (preview) để xem trước khớp bản in

Khoảng cách chọn **8mm** (~2 dòng chữ 16px) — muốn thưa/khít hơn thì đổi đúng 2 con số này.

### Checkpoint — 2026-08-22 (M1-M2)
Vừa hoàn thành: giãn khối ngày ↔ chữ ký trên bản in phiếu chi.
Đang làm dở: không.
Bước tiếp theo: user xem lại bản in 3 mẫu, chốt 8mm hay đổi số khác.
Chưa kiểm chứng bằng mắt: verify bằng dump cấu trúc mẫu 211/217/236 từ DB + compile check.
Blocked: không.

## Phase N — Cột "Mã phiếu đề nghị chi" ở màn danh sách mở tab mới (2026-08-22)

**User yêu cầu:** ở `/finance/bill-payments`, click mã phiếu đề nghị chi phải mở sang tab khác.

Cột này link sang màn **khác** (`/finance/bill-payment-requests/{id}`) — mở tab mới để không mất
bộ lọc/trang đang xem. Làm giống hệt cột "Mã phiếu đề nghị thu" ở màn Phiếu thu tiền
(`pages/finance/bill-incomes/index.vue:144`), ERP cũng để `target="_blank"`.

Cột "Mã phiếu" (chính) GIỮ NGUYÊN điều hướng trong tab hiện tại — nó là lối vào duy nhất của màn
chi tiết cùng phân hệ (spec §11.1), chuột phải vẫn mở tab mới được.

- [x] N1 — `pages/finance/bill-payments/index.vue` slot `#cell-requestCode`: thêm `target="_blank"`
      + `rel="noopener"` vào `<nuxt-link>` (vue-router tự bỏ qua click khi có `target` → trình
      duyệt điều hướng thật, không phải chuyển trang SPA)

### Checkpoint — 2026-08-22 (N1)
Vừa hoàn thành: cột Mã phiếu đề nghị chi ở màn danh sách phiếu chi mở tab mới.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments` click thử 1 dòng có mã đề nghị.
Chưa kiểm chứng bằng mắt: verify bằng compile check template (vue-template-compiler, 0 lỗi).
Blocked: không.

## Phase O — Rà nút màn chi tiết theo màn Phiếu thu tiền (2026-08-22)

**User yêu cầu:** màn `/finance/bill-payments/{id}` các button dùng đúng quy tắc V2Base,
**tham khảo màn Phiếu thu tiền** (`pages/finance/bill-incomes/_id/index.vue`).

**Hiện trạng:** toàn bộ nút ĐÃ là `V2BaseButton` (có icon `#prefix`, có `size="sm"`, dùng prop
`primary/secondary/tertiary` chứ không `type=`). Lệch màn phiếu thu ở 3 chỗ:

| Lệch | Sửa |
| --- | --- |
| Nút **Duyệt** để `status="success"` (#16a34a) — cả footer lẫn popup duyệt | Bỏ `status` → `primary` trần = teal `#1abc9c`, đúng như phiếu thu + `V2Footer` (skill `button-convention` mục 2b, user chốt 2026-08-20) |
| Chữ nút: `Duyệt` / `Hủy phiếu` | Đổi thành **`Duyệt phiếu chi` / `Hủy phiếu chi`** — song song `Duyệt phiếu thu` / `Hủy phiếu thu` |
| Icon nút **Xác nhận** trong popup hủy dùng `ri-close-circle-line` | Đổi `ri-check-line` (mục 3: close-circle dành cho "Từ chối"); ngữ cảnh hủy đã có icon đỏ ở header + màu danger |

⚠️ **Thứ tự nút GIỮ NGUYÊN `Duyệt → Hủy → In → Xuất Excel → Xóa`** — cố ý lệch skill mục 5
(chính → phụ → nguy hiểm). Cặp Duyệt / Hủy phải đứng cạnh nhau, đúng quy ước user chốt ở màn phiếu
thu 2026-08-20. Trong phiên này từng sắp lại cho "đúng skill" rồi **hoàn tác**; đã ghi comment cảnh
báo ngay trong file, đừng sửa lại lần nữa.

- [x] O1 — `_id/index.vue`: nút Duyệt bỏ `status="success"`, đổi chữ `Duyệt phiếu chi`
- [x] O2 — `_id/index.vue`: nút Hủy đổi chữ `Hủy phiếu chi`, giữ vị trí ngay sau Duyệt
- [x] O3 — `components/ApproveBillPaymentModal.vue`: nút Duyệt trong popup bỏ `status="success"`
- [x] O4 — `_id/index.vue`: icon nút Xác nhận popup hủy → `ri-check-line`

Giữ nguyên (đã khớp phiếu thu): In = `secondary`, Xuất Excel = `secondary status="success"`,
Hủy / Xóa = `primary status="danger"`, footer popup = primary → tertiary "Đóng" đứng cuối.
Khác biệt còn lại có chủ ý: `BaseConfirmModal` xóa của phiếu chi có prop `danger` (phiếu thu không)
— giữ vì Xóa là thao tác phá huỷ.

### Checkpoint — 2026-08-22 (O1-O4)
Vừa hoàn thành: chuẩn hoá nút màn chi tiết phiếu chi theo khuôn màn Phiếu thu tiền.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/1320` đối chiếu với `/finance/bill-incomes/{id}`.
Chưa kiểm chứng bằng mắt: verify bằng compile check 2 file (0 lỗi), chưa mở trình duyệt.
Blocked: không.

## Phase N — Bản in tràn khỏi lề phải (2026-08-22)

Phát hiện khi đo màn Phiếu thu — đo luôn phiếu chi bằng cùng cách (render HTML thật qua
`BillPaymentPrintService::render()`, dựng lại môi trường cửa sổ in, ép bề ngang 180mm = 680px,
Chromium headless).

**Đo TRƯỚC khi sửa — phiếu chi tràn NẶNG HƠN phiếu thu:**

| Mẫu | Phần tử tràn | Tràn |
| --- | --- | --- |
| 211 | hàng chữ ký (rộng **772px**) | **91.4px ≈ 24mm** |
| 236 | hàng chữ ký (rộng **863px**) | **182.3px ≈ 48mm** |
| 217 | khối "Liên số / Quyển số / Nợ / Có" (232px) | 13.1px |

**Root cause hàng chữ ký — do chính Phase L:** khi đưa CSS về giống ERP tôi copy nguyên
`table.block td { white-space: nowrap }` từ màn Phiếu thu. Deviation đó chỉ đúng cho phiếu thu vì
ô chữ ký bên đó chỉ có **1 dòng nhãn**. Ô chữ ký của mẫu 211/217/236 có **3 dòng** —
nhãn + "(ký, họ tên đóng dấu)" + tên người ký — ép nowrap thì bảng phình tới 772-863px.

**Root cause khối Liên số:** giống hệt phiếu thu — bảng nằm trong ô cuối của bảng đầu trang
(`table-layout: fixed`, ô 227px, trừ padding còn 211px) nhưng cần 232-240px ở cỡ chữ 16px.

- [x] N1 — Bỏ `nowrap` ở `table.block td` (giữ `vertical-align: top` để 5 ô vẫn bắt đầu cùng mức),
      padding còn 2px
- [x] N2 — Khối Liên số: `font-size: 12px`, `padding: 0 2px`, `margin: 0 -8px`, `nowrap` từng hàng
- [x] N3 — Áp cả `printBaseStyles()` lẫn `<style scoped>`
- [x] N4 — Sửa lỗi tự gây: comment trong `printBaseStyles()` lọt **dấu backtick** làm đứt template
      literal (đúng cái bẫy đã ghi sẵn trong chính comment đó) — babel parse fail, đã bỏ

**Đo lại SAU khi sửa: tràn = 0px ở cả 3 mẫu 211 / 217 / 236.**
Thứ tự rule đã kiểm: `table.block td { padding: 2px 2px }` KHÔNG đè `tr + tr td { padding-top: 8mm }`
của Phase M vì rule sau có specificity cao hơn.

### Checkpoint — 2026-08-22 (N1-N4)
Vừa hoàn thành: bản in phiếu chi hết tràn lề phải.
Đang làm dở: không.
Bước tiếp theo: user mở bản in 3 mẫu xác nhận hàng chữ ký (nay cho xuống dòng) và cỡ chữ khối
Liên số 12px có chấp nhận được không.
Chưa kiểm chứng bằng mắt: chỉ đo hình học.
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

### Điều tra — cột "Khách hàng / Nhà cung cấp" trống ở màn danh sách (2026-08-22)

**User báo:** màn `finance/bill-payments` không hiện thông tin cột Khách hàng / Nhà cung cấp.

- [x] Trace DB → API → FE: **không phải bug**. API trả đúng cho loại 1 (`supplier_code-supplier_name`)
      và loại 2 (`customer_code-customer_name`); FE đọc đúng key `object_name`; không có bản ghi
      `user_column_settings` cho `finance_bill_payments` nên cột không bị ẩn.
- [x] Đếm lại dữ liệu thật (`bill_payment_details`): loại 1 = 1.318/1.318 có NCC; loại 2 = 163/163
      có KH; loại 4 = 1.022 dòng, loại 6 = 359, loại 12 = 182 — **0 dòng** có KH/NCC.
      Tra ngược bảng đề nghị: loại 6 chỉ có `contract_code` (537/537), loại 12 không có gì
      (đối tượng nằm ở chuyến xe `delivery_trip_accounting_id`).
- [x] **User chốt 2026-08-22: GIỮ NGUYÊN NHƯ ERP** — chỉ loại 1 và 2 có đối tác, loại 4/6/12 hiện
      `—`. KHÔNG tra ngược hợp đồng/chuyến xe. Không sửa code.

### Checkpoint — 2026-08-22
Vừa hoàn thành: điều tra cột KH/NCC màn danh sách phiếu chi — kết luận không sửa (user chốt giữ như ERP).
Đang làm dở: không.
Bước tiếp theo: không có việc tồn từ mục này.
Blocked: không.

### Fix — cột "Khách hàng / Nhà cung cấp" trống trên server (2026-08-22, bổ sung)

**Điều tra lại bằng Playwright trên `hrm-crm.eteksofts.com`** (mục trước kết luận "không phải bug"
là do chỉ đo trên DB local — SAI):

- 7/7 phiếu **loại 1** ở trang đầu server trả `object_name = null`, trong khi đề nghị nguồn vẫn ghi
  đủ NCC (vd `TPE.PC0826.00010` ← `TPE.DNTT0726.00142`, header `supplier_name` =
  "CÔNG TY CỔ PHẦN SẢN XUẤT XÂY DỰNG CKT").
- **Nguyên nhân:** chỗ lưu đối tác đổi theo hình thức thanh toán của đề nghị —
  TM (`type_payment=1`) lưu trên TỪNG DÒNG chi tiết, CK (`type_payment=2`) lưu ở HEADER đề nghị
  (`bill_payment_requests.supplier_*` / `customer_*`), dòng chi tiết để NULL. Code chỉ đọc dòng
  chi tiết → phiếu CK luôn trống. Local không lộ vì 1.318/1.318 phiếu đã lập đều từ đề nghị TM.
- Màn Đề nghị thanh toán đã xử lý đúng luật này từ trước (`BillPaymentRequestListResource::objectName()`).
  ERP gốc cũng chỉ đọc dòng chi tiết (`BillPaymentController::searchData()` :73-82) → HRM cố ý sửa.

- [x] BE1 — `BillPaymentListResource::objectName()`: đọc snapshot dòng chi tiết trước, rỗng thì
      lấy snapshot header đề nghị (0 query thêm, `billPaymentRequest` đã eager load). Tách helper
      `joinCodeName()` giữ đúng khuôn "MÃ-TÊN" của ERP.
- [x] BE2 — `BillPaymentPrintService`: bản in/Excel cũng trống ô **"Đơn vị" + "Địa chỉ"** với phiếu
      CK (đo thật trên server: `TPE.PC0826.00010` ra "Đơn vị: " rỗng). Bù từ header đề nghị khi
      2 nhánh cũ không ra gì — vá luôn ca phiếu CK NHIỀU dòng chi tiết (nhánh `count() === 1`
      không chạy nên trước đây `KHACH_HANG` không hề được gán).
- [x] BE3 — `BillPaymentDetailResource`: trả thêm `supplier_code/name`, `customer_code/name` trong
      khối `bill_payment_request` để FE bù cột "Đối tượng". Chỉ để hiển thị.
- [x] FE1 — `BillPaymentForm.buildPartyLabel(d, header)` + 2 chỗ gọi (nạp từ đề nghị → `data`,
      nạp phiếu chi → `data.bill_payment_request`).
- [x] FE2 — `ApproveBillPaymentModal.buildPartyLabel(d, this.bill?.bill_payment_request)`.

**Kiểm chứng:** API local trước/sau fix ra kết quả Y HỆT (không hồi quy trên dữ liệu TM);
giả lập trong bộ nhớ dạng CK (dòng chi tiết rỗng, header có NCC) → danh sách ra
"MOCK-NCC-CONG TY MOCK CHUYEN KHOAN", bản in ra "Đơn vị: MOCK-NCC - CONG TY MOCK CHUYEN KHOAN".
KHÔNG ghi gì vào DB. FE: compile template + parse script sạch.
**Chưa kiểm chứng bằng mắt trên server** — cần deploy rồi mở lại màn.

### Checkpoint — 2026-08-22
Vừa hoàn thành: fix cột Khách hàng/NCC cho phiếu chi CHUYỂN KHOẢN (danh sách + bản in + màn chi tiết + modal duyệt).
Đang làm dở: không.
Bước tiếp theo: deploy `gop_db` lên hrm-crm rồi mở lại `/finance/bill-payments` xác nhận cột đã hiện.
Blocked: không.

---

## Phase — Bỏ "Hủy phiếu" khỏi màn danh sách (2026-08-24)

Đồng bộ quy tắc mới ở `.claude/skills/list-page/SKILL.md` mục 1 (chốt cùng ngày ở màn Phiếu thu):
"Hủy phiếu" / "Không duyệt" chỉ đặt ở màn CHI TIẾT. Ở danh sách nó chỉ là link điều hướng.

- [x] Xóa action `key: 'cancel'` + `case 'cancel'` trong `pages/finance/bill-payments/index.vue`,
      sửa comment cho khớp. Giữ "Duyệt", không đụng màn chi tiết và BE.

### Checkpoint — 2026-08-24
Vừa hoàn thành: bỏ "Hủy phiếu" khỏi cột hành động màn danh sách Phiếu chi.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt xác nhận menu ⋮ không còn "Hủy phiếu"; màn chi tiết vẫn hủy được.
Chưa kiểm chứng bằng mắt: chỉ parse template + script.
Blocked: không.

---

## Phase — Mặc định loại chi + Lưu nháp không bắt buộc trường (2026-08-24)

User yêu cầu ở `/finance/bill-payments/create`:
1. Vào màn là **mặc định chọn sẵn "Chi trả nhà cung cấp"** (loại chi 1).
2. **Lưu nháp thì không bắt validate gì cả** — hiện đang chặn ngay ở FE (`Người nhận` gắn
   `required`) và ở BE (`BillPaymentStoreRequest` bắt buộc `type` · `account_has` · `receiver` ·
   `details` + bộ trường theo nhánh, áp cho MỌI lần lưu).

**Quyết định thiết kế:** phiếu chi luôn được tạo ở trạng thái NHÁP (`status` do server đặt, client
không gửi), "Lưu và gửi duyệt" = 2 API tuần tự (`POST` rồi `POST /{id}/submit`). Nên FE gửi thêm cờ
**`submit_after`** để BE biết lần lưu này có gửi duyệt ngay không:
- `submit_after` falsy → **lưu nháp**: bỏ hết `required`, chỉ giữ rule ĐỊNH DẠNG (`in` / `exists` /
  `numeric`) để không ghi rác xuống DB.
- `submit_after = true` → giữ NGUYÊN bộ luật hiện tại, fail **trước khi** tạo phiếu (không đẻ ra
  phiếu nháp rác rồi mới báo lỗi, cũng không tạo trùng khi bấm lại).

Cờ này KHÔNG phải `status`: `status` vẫn do server đặt, và `BILL_COLUMNS_FROM_CLIENT` không có
`submit_after` nên nó không thể lọt xuống DB.

- [x] **FE-1** `BillPaymentForm.vue` `mounted()` — màn TẠO và chưa có phiếu đề nghị theo query thì
      đặt `form.type = 1`. Đặt TRƯỚC `markFormPristine()` để không bị hỏi "chưa lưu" oan.
- [x] **FE-2** `BillPaymentForm.vue` — bỏ `required` khỏi `v-validate` của `Người nhận` (giữ
      `max:255`), đúng skill `form-validate` mục 1: FE chỉ gắn `required` cho ô Tên, required khác
      do BE quyết theo trạng thái. Dấu `*` trên nhãn giữ nguyên (vẫn bắt buộc khi gửi duyệt).
- [x] **FE-3** `buildPayload()` — gửi kèm `submit_after`.
- [x] **BE-1** `BillPaymentStoreRequest` (Update kế thừa) — nhánh nháp bỏ hết `required`.
- [x] **BE-2** `BillPaymentWriteService::submit()` — chốt chặn: phiếu nháp thiếu trường bắt buộc thì
      **không cho gửi duyệt** (422). Không có bước này thì gọi thẳng `POST /{id}/submit` là lách được
      toàn bộ luật vừa nới.
- [x] **Verify** gọi thật 2 luồng bằng HTTP kernel: lưu nháp form gần như trống → 200; gửi duyệt
      thiếu trường → 422 đúng câu lỗi; submit thẳng phiếu nháp thiếu trường → 422.

**Verify (chạy thật qua HTTP kernel + JWT, bọc transaction rồi rollback — DB không còn dấu vết):**

| Luồng | Kết quả |
| --- | --- |
| `POST /bill-payments` với payload **rỗng** (`submit_after = 0`) | **200**, tạo phiếu nháp |
| `POST /bill-payments` `submit_after = 1`, thiếu trường | **422** — `type` · `account_has` · `receiver` · `details` |
| `POST /bill-payments/{id}/submit` gọi THẲNG trên phiếu nháp rỗng | **422** đủ 5 câu lỗi tiếng Việt, phiếu **giữ nguyên trạng thái 1** |

FE: compile template + parse script `BillPaymentForm.vue` — OK.

- [x] **FE-4** Ô "Loại chi" thêm `:allow-clear="false"` — bỏ nút × của select2, chỉ cho ĐỔI sang
      loại khác chứ không xóa trắng (user yêu cầu 2026-08-24). Prop có sẵn trong `V2BaseSelect`
      (mặc định `true`), không phải sửa component dùng chung.

### Đợt 2 — nới `required` ở FormRequest vẫn CHƯA đủ (user báo lại 2026-08-24)

Bấm Lưu nháp khi mới chỉ có loại chi vẫn hỏng. Bộ luật `required` chỉ là **lớp thứ nhất**; test
đúng payload FE gửi mới lộ thêm 2 lớp chặn nữa nằm sâu hơn:

| # | Chặn ở đâu | Triệu chứng | Cách xử lý |
| --- | --- | --- | --- |
| 1 | `BillPaymentWriteService::guardRequestLink()` — luật "nhánh A bắt buộc có đề nghị nguồn" | 422 `Bắt buộc chọn phiếu đề nghị thanh toán.` (dấu chấm cuối câu — khác câu của FormRequest, đó là dấu vết lần ra) | Thêm tham số `$requireRequest`; lưu nháp thì bỏ vế BẮT BUỘC NHẬP, **giữ nguyên** vế chống 2 phiếu cùng trỏ 1 đề nghị |
| 2 | Chính bảng DB: `account_has` · `receiver` (và `account_dept` ở bảng chi tiết) là **NOT NULL không có mặc định** | 500 `Column 'account_has' cannot be null` | `draftSafeAttributes()` ghi **0 / chuỗi rỗng** khi lưu nháp |

Chọn ghi 0 thay vì đổi cột sang nullable: `bill_payments` là **bảng dùng chung ERP+HRM**, đổi schema
phải hỏi user trước. 0 không trùng id tài khoản nào (đo: 1.305/1.305 phiếu hiện có đều trỏ tài khoản
thật), quan hệ `accountHas()` là `belongsTo` null-safe — không có JOIN nào ở cả HRM lẫn ERP nên màn
danh sách không vỡ.

Kèm 2 việc bắt buộc đi cùng số 0 đó, thiếu là đẻ bug mới:
- `BillPaymentStoreRequest::prepareForValidation()` đưa `0` về `null` TRƯỚC khi validate — nếu không,
  mở lại phiếu nháp rồi Lưu nháp lần nữa sẽ dính `exists:accounts,id` với đúng số 0
  ("Tài khoản có không tồn tại"), tức không sửa nổi phiếu nháp của chính mình.
- `BillPaymentDetailResource` trả `null` thay cho `0` để select ở FE hiện placeholder.

- [x] **BE-3** `guardRequestLink()` nhận `$requireRequest`; `savingAsDraft()` chỉ nhận diện nháp khi
      payload NÓI RÕ `submit_after = false` (đường gọi service nội bộ không gửi khóa này → vẫn chặt).
- [x] **BE-4** `draftSafeAttributes()` + `account_dept ?? 0` trong `syncDetails()`.
- [x] **BE-5** `prepareForValidation()` chuẩn hoá 0/'' → null.
- [x] **BE-6** `BillPaymentDetailResource` trả null thay 0 cho `account_has` / `account_dept`.

**Verify đợt 2 (HTTP kernel + JWT, transaction rồi rollback — DB vẫn 1.305 phiếu, 0 phiếu `account_has = 0`):**

| Luồng | Kết quả |
| --- | --- |
| Lưu nháp **chỉ có loại chi** | **200**, sinh mã `TPE.PC0826.00004` |
| Mở lại phiếu nháp đó | 200, `account_has` trả `null` (không phải 0) |
| Lưu nháp **lần 2** trên chính phiếu đó | **200** |
| Lưu nháp có 1 dòng chi tiết **chưa chọn tài khoản nợ** | **200** |
| Gửi duyệt phiếu nháp thiếu trường | **422** — `account_has` · `receiver` · `details` · `bill_payment_request_id` |
| Lưu + gửi duyệt thiếu trường | **422** — cùng bộ lỗi |

### Checkpoint — 2026-08-24
Vừa hoàn thành: mặc định loại chi "Chi trả nhà cung cấp" ở màn tạo + lưu nháp CHỈ CẦN loại chi
(gỡ đủ 3 lớp chặn: FormRequest → guard service → cột NOT NULL) + bỏ nút xóa ở ô Loại chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/create` xác nhận loại chi chọn sẵn và bấm Lưu nháp
với form trống.
Chưa kiểm chứng bằng mắt: chỉ compile FE; 3 luồng BE đã gọi thật.
Blocked: không.

## Đồng nhất icon nút Duyệt (2026-08-27)

- [x] **FE-x** `pages/finance/bill-payments/index.vue` — cột hành động: icon "Duyệt" đổi
      `ri-check-line` → `ri-checkbox-circle-line` cho giống màn `finance/prepick-cancel-requests`.
      Chỉ đổi icon; vị trí nút, chữ, điều kiện `is_can_approve` và nút "Duyệt phiếu chi" ở màn chi
      tiết giữ nguyên (màn chi tiết đã cùng icon `ri-check-line` với V2Footer của prepick).

### Checkpoint — 2026-08-27
Vừa hoàn thành: đồng nhất icon nút Duyệt ở cột hành động màn danh sách phiếu chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments` xem lại icon trong menu ⋮.
Chưa kiểm chứng bằng mắt: chỉ compile template (vue-template-compiler), chưa mở trình duyệt.
Blocked: không.

### Kẹp trần ô "Số tiền duyệt chi" (2026-08-27)

- [x] **FE** `pages/finance/bill-payments/components/BillPaymentForm.vue` — ô "Số tiền duyệt chi" khai `:max="Number(detail.payment_money_request || 0)"`.
      Lý do: bản cũ chỉ kẹp ở handler `@input` của màn (`clampApprove()`), mà ô được điền sẵn ĐÚNG
      BẰNG số đề nghị chi → kẹp về đúng giá trị đang giữ → Vue coi là "không đổi" → ô vẫn HIỆN số to
      vừa gõ tới khi rời ô. Nay `V2BaseCurrencyInput` có prop `max` kẹp ngay trong `onInput()`.
      Chi tiết + 9 ca test: `.plans/gop-db/finance-bill-income/plan.md` mục "ô vẫn hiện số to hơn trần".
      `clampApprove()` giữ nguyên làm lớp phòng thủ cho giá trị đặt bằng code.

### Duyệt / Hủy phiếu xong về màn danh sách (2026-08-27)

- [x] **FE** `pages/finance/bill-payments/_id/index.vue` — thêm `goToList()` (gọi
      `markFormSaved()` rồi `$router.push('/finance/bill-payments')`), dùng chung cho 3 luồng:
      - `@approved` của `ApproveBillPaymentModal`: trước đây `reloadDetail` → nay `goToList`
      - `submitCancel()` thành công (Hủy phiếu chi): trước đây `reloadDetail` → nay `goToList`
      - `handleDelete()`: thay `$router.push(...)` trần bằng `goToList()`
      Giữ nguyên `reloadDetail` cho các nhánh LỖI (409 người khác vừa xử lý, 403/423 hết quyền) —
      những ca đó vẫn phải ở lại chi tiết để cờ `is_can_*` khớp DB.
      Theo đúng khuôn màn Phiếu thu tiền (`bill-incomes/_id/index.vue` — user chốt 2026-08-21).

### Checkpoint — 2026-08-27
Vừa hoàn thành: duyệt / hủy phiếu chi xong tự quay về màn danh sách.
Đang làm dở: không.
Bước tiếp theo: user mở 1 phiếu chi chờ duyệt, bấm Duyệt và bấm Hủy phiếu, xác nhận về
`/finance/bill-payments` và danh sách đã cập nhật trạng thái.
Chưa kiểm chứng bằng mắt: chỉ compile template + parse script, chưa mở trình duyệt.
Blocked: không.

### Màn in — dòng "Ngày …" và nhãn hàng ký bị xuống dòng (2026-08-27)

User báo qua ảnh chụp `/finance/bill-payments/{id}/print`: dòng "Ngày 27 Tháng 08 Năm 2026" ngay
dưới chữ "PHIẾU CHI" gãy làm 2 dòng, và ô "KẾ TOÁN TRƯỞNG" lệch hẳn so với 4 ô ký còn lại.
Đo bằng Chromium headless ở đúng bề ngang vùng in (180mm = 680px) — tái hiện cả ở BẢN IN, không
riêng preview:

| Chỗ | Trước | Sau |
| --- | --- | --- |
| span "Ngày … Tháng … Năm …" (đầu phiếu) | `lines=2` | `lines=1` |
| Nhãn "KẾ TOÁN TRƯỞNG" / "NGƯỜI NHẬN TIỀN" | `labelLines=2` (3 ô kia = 1) | cả 5 ô `labelLines=1` |
| Chiều cao hàng ký | 94px | 76px |
| Tràn mép phải bảng ký | 0 | 0 (giữ nguyên) |

- [x] **FE** `pages/finance/bill-payments/_id/print.vue` — thêm 2 rule vào **CẢ 2 nơi**
      (`printBaseStyles()` cho cửa sổ in **và** `<style scoped>` cho preview — scoped CSS không sang
      cửa sổ in):
      1. `table.no-border[style*="table-layout"] > tbody > tr > td:nth-child(2)`: `white-space: nowrap`
         + bỏ padding ngang. Ô giữa 227px, trừ padding 8px×2 của pdf.css còn 211px, chuỗi ngày cỡ
         18px cần 214px → gãy dòng. Bỏ padding là vừa, **giữ nguyên cỡ 18px của ERP**.
         Đã loại phương án `table-layout: auto`: đo ra cột trái co còn 32px, tiêu đề "PHIẾU CHI"
         hết nằm giữa trang.
      2. `table.block td span[style*="font-size:15px"]`: `font-size: 14px` + `nowrap`. Ô ký 136px,
         nhãn 15px cần ~140px. Chỉ nowrap **span nhãn**, KHÔNG nowrap cả ô (skill print-page: nowrap
         cả ô làm bảng phình 772/863px so với 680px vùng in vì dòng tên người bị ép 1 dòng).
         Bám `font-size:15px` thay vì `span:first-child` để không đụng mẫu 217 (nhãn "NGƯỜI LẬP
         PHIẾU" bên đó 18px, ô 275px, vốn đã 1 dòng).
      Dòng "Đã duyệt ĐNTT" (`BillPaymentPrintService::approvedSignature()`) **giữ nguyên** theo yêu
      cầu user — chỉ sửa cách hiển thị cho thẳng hàng, không đụng nội dung.
      Stress test với tên nhân viên dài nhất trong DB (24 ký tự) ở 560/620/680px: `overflowRight = 0`.

⚠️ Bẫy đã dính lại lần nữa: viết dấu backtick trong **chú thích CSS nằm trong template literal**
của `printBaseStyles()` → đứt chuỗi, babel báo "Missing semicolon". Skill print-page mục 8a đã ghi.

### Checkpoint — 2026-08-27
Vừa hoàn thành: sửa dòng "Ngày …" đầu phiếu và nhãn hàng chữ ký ở màn in phiếu chi (bản in +
preview khớp nhau).
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/1321/print` xem lại 2 chỗ đã khoanh đỏ.
Chưa kiểm chứng bằng mắt: đo bằng Chromium headless ở đúng khổ in + compile
(vue-template-compiler / babel / node-sass), chưa mở trình duyệt thật.
Blocked: không.

### Form phiếu chi lệch ERP — thứ tự trường + thiếu 2 loại chi + thiếu khối đối tượng/ngân hàng (2026-08-27)

User báo màn `/finance/bill-payments/create` không giống ERP `admin/income-expenditure/bill_payments/create`:
số phiếu đề nghị phải đứng đầu, và loại chi ERP có 7 mà HRM mới 5.

Đối chiếu nguồn ERP (`income_expenditure/bill_payments/form.blade.php` +
`partials/classes/IncomeExpenditure/BillPayment.blade.php` + `BillPaymentRequest::TYPE`):

| Hạng mục | ERP | HRM trước | Kết luận |
| --- | --- | --- | --- |
| Loại chi | 7 (`TYPE` bật 1·2·3·4·6·10·12) | 5 (`TYPES_FOR_SELECT = [1,2,6,12,4]`) | thiếu 3 "Chi thưởng NVKD" + 10 "Chi khác" |
| Nhánh A | `has_bill_payment_request` = type ∈ 1·2·3·6·10·12 | `TYPES_FROM_REQUEST = [1,2,6,12]` | thiếu 3 · 10 |
| Thứ tự trường | Số phiếu đề nghị (dòng riêng) → Mã phiếu → TK có → Loại chi → Hình thức TT → Người nhận → Loại tiền → Tỷ giá → Người đề nghị → Phòng ban → Lý do chi | Loại chi → Số phiếu đề nghị → Mã phiếu → TK có → Người nhận → Hình thức TT → … | sắp lại |
| Loại đối tượng (đề nghị type = 10) | có | không | bổ sung |
| Khách hàng / Nhân viên / Nhà cung cấp / Phí | có (theo hình thức TT + loại) | không | bổ sung |
| Khối thông tin ngân hàng (đề nghị CK) | có — 5 dòng trong nước, thêm Swift/IBAN/địa chỉ + NH trung gian với NCC nước ngoài | không | bổ sung |

Đo dữ liệu thật (DB gộp, 2026-08-27) trước khi quyết định port khối ngân hàng:
đề nghị `status = 6` chưa có phiếu chi = **96 phiếu, trong đó 80 là CHUYỂN KHOẢN** (popup chọn đề
nghị của màn phiếu chi cố ý KHÔNG lọc `type_payment`, đúng ERP) → khối ngân hàng gặp thật, không
phải nhánh chết. Ngược lại `type_object` toàn NULL trên 4.052 phiếu và loại 3 · 10 có **0 phiếu**
ở cả `bill_payment_requests` lẫn `bill_payments` — vẫn port cho khớp ERP, nhưng đây là lý do
`TYPES_ALLOWED` của màn Đề nghị thanh toán GIỮ NGUYÊN 4 loại (user đã chốt trước đó).

⚠️ KHÔNG dùng `supplier->type` như ERP (`BillPaymentRequestController@getData` :461) để nhận biết
NCC nước ngoài: model `Supplier` của ERP trỏ bảng `customers`, mà `customers` trên DB gộp **không
có cột `type`** (chỉ có `customer_type`) — copy nguyên là 500. Nhận biết bằng dữ liệu có sẵn ngay
trên phiếu đề nghị (`swift_code` / `iban_number` / `cost` / `mid_bank_name`), khối chỉ đọc nên
hiện-dòng-nào-có-giá-trị là đủ.

- [x] **BE** `Entities/BillPayment/BillPayment.php` — `TYPES_FROM_REQUEST` `[1,2,6,12]` →
      `[1,2,3,6,10,12]` (khớp getter `has_bill_payment_request` của ERP). Luật `type` của
      `BillPaymentStoreRequest` derive từ hằng này nên tự lan ra 7 giá trị hợp lệ.
- [x] **BE** `Services/BillPaymentService.php` — `TYPES_FOR_SELECT` → `[1,2,3,4,6,10,12]`.
      ERP màn phiếu chi dùng `type_for_select()` KHÔNG tham số cho CẢ ô lọc danh sách lẫn dropdown
      form (khác màn UNC — bên đó ô lọc bỏ loại 4), nên 1 danh sách dùng chung là đúng.
- [x] **BE** `Transformers/BillPaymentRequestResource/BillPaymentRequestDetailResource.php` —
      thêm `type_object` + `type_object_name` (nguồn cho trường "Loại đối tượng").
- [x] **BE** `Transformers/BillPaymentResource/BillPaymentDetailResource.php` — khối
      `bill_payment_request` trả thêm: `type_payment`, `type_object(+_name)`, `cost(+_name)`,
      `employee_code/name`, và bộ ngân hàng (`account_number`, `account_name`, `bank_name`,
      `bank_branch`, `bank_province_name`, `swift_code`, `iban_number`, `bank_address`, `mid_*`)
      để màn Sửa/Xem hiện đúng như màn Tạo.
- [x] **FE** `pages/finance/bill-payments/components/BillPaymentForm.vue`
      - `TYPES_FROM_REQUEST` → `[1,2,3,6,10,12]`; thêm `TYPES_OF_REQUEST = [1,2,6,12]` truyền vào
        popup chọn đề nghị (ô lọc "Loại chi" trong popup chỉ liệt kê loại mà ĐỀ NGHỊ thật sự có —
        để loại 3/10 ở đó là lựa chọn chọn xong luôn ra 0 dòng; cùng cách màn UNC đã làm).
      - sắp lại thứ tự trường theo ERP, Số phiếu đề nghị lên đầu form.
        🔶 Sửa lại 2026-08-27 theo user: KHÔNG tách dòng riêng như ERP (`<div class="row">` bọc
        riêng, bỏ trống 9 cột) mà để CHUNG một `form-row` với các ô còn lại — vẫn là ô đầu tiên.
      - bổ sung trường chỉ đọc: Loại đối tượng · Khách hàng · Nhân viên · Nhà cung cấp · Phí.
      - bổ sung khối "Thông tin chuyển khoản" (chỉ đọc) khi đề nghị là CK.
      - `requestInfo` + `applyPaymentRequest()` + `loadDetail()` map thêm các field trên.

### Checkpoint — 2026-08-27
Vừa hoàn thành: form phiếu chi bám lại ERP — Số phiếu đề nghị lên đầu form, thứ tự 10 trường theo
đúng `form.blade.php`, dropdown Loại chi đủ 7 loại (BE + FE), thêm 3 khối chỉ đọc "Đối tượng nhận
tiền" / "Tài khoản nhận tiền" / "Ngân hàng trung gian".
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/create`, mở dropdown Loại chi đếm đủ 7, chọn 1 phiếu
đề nghị CHUYỂN KHOẢN trong popup và xem 3 khối mới đổ dữ liệu; mở lại 1 phiếu cũ ở màn Sửa/Xem để
đối chiếu cùng bố cục.
Chưa kiểm chứng bằng mắt: compile template + parse script (vue-template-compiler / babel), `php -l`
4 file BE, và gọi thẳng 2 Resource + `typesForSelect()` trên dữ liệu thật — CHƯA mở trình duyệt.
Blocked: không.

### Đối chiếu ERP về loại chi — 2 màn KHÁC còn lệch, user chốt LÀM SAU (2026-08-27)

User hỏi có mở thêm loại chi cho màn Đề nghị thanh toán không → chốt "cứ làm hệt như bên ERP",
rồi chốt tiếp "làm màn phiếu chi trước đã, màn ủy nhiệm chi làm sau".

Soát lại toàn bộ chỗ ERP gọi `BillPaymentRequest::type_for_select()`:

| Màn ERP | Gọi thế nào | Số loại | HRM hiện tại | Khớp? |
| --- | --- | --- | --- | --- |
| Phiếu chi — ô lọc danh sách (`index`/`approved`/`forApproved`) | `type_for_select()` | 7 | 7 (đã sửa) | ✅ |
| Phiếu chi — form lập/sửa (`formJs` :1) | `type_for_select()` | 7 | 7 (đã sửa) | ✅ |
| Đề nghị thanh toán — **form lập/sửa** (`formJs` :2) | `type_for_select([3,4,10])` | **4** | 4 (`TYPES_ALLOWED`) | ✅ — KHÔNG cần mở thêm |
| Đề nghị thanh toán — ô lọc danh sách (`index` :63) | `type_for_select([4])` | **6** | 4 (`typeForSelect()`) | ❌ thiếu Chi thưởng NVKD + Chi khác |
| Đề nghị thanh toán — ô lọc `approved`/`forApproved` | `type_for_select()` | 7 | (HRM gộp còn 1 màn) | — |
| Ủy nhiệm chi — ô lọc / form | `type_for_select([4])` / `type_for_select()` | 6 / 7 | 6 / 7 | ✅ |

⚠️ Bẫy: `type_for_select($ignore)` nhận danh sách loại **BỊ LOẠI**, không phải danh sách được chọn.
Đọc nhầm chiều là ra kết quả ngược hẳn.

**KHÔNG LÀM — user chốt 2026-08-27: "màn phiếu đề nghị thanh toán không sửa gì vào đấy nhé"**

- ~~ô LỌC màn danh sách Đề nghị thanh toán 4 → 6 loại cho khớp ERP `index.blade.php` :63~~
  → **BỎ.** Chênh lệch này đã biết và cố ý để nguyên, đừng "sửa cho đúng ERP" ở lần soát sau.
  (Chỉ có 4 loại đề nghị tồn tại trên DB nên 2 loại thêm vào cũng luôn ra 0 dòng.)

**Chưa làm (user chốt để sau):**

- [ ] **FE** Ủy nhiệm chi (`BillPaymentAuthorizationForm.vue`) — thứ tự trường + Số phiếu đề nghị
      lên đầu form, đồng bộ với màn Phiếu chi vừa sửa.

ℹ️ Thay đổi DUY NHẤT chạm vào file của màn Đề nghị thanh toán trong đợt này:
`BillPaymentRequestDetailResource` trả THÊM `type_object` + `type_object_name` (và hằng
`TYPE_OBJECTS`). Đây là nguồn dữ liệu cho ô "Loại đối tượng" của FORM PHIẾU CHI — endpoint
`GET finance/bill-payments/payment-requests/{id}` dùng chính resource này. Chỉ THÊM khóa vào
response, không sửa truy vấn/luật/giao diện của màn Đề nghị thanh toán; FE màn đó không đọc 2 khóa
mới nên hành vi không đổi.

**Cố ý KHÁC ERP ở popup chọn đề nghị của màn phiếu chi (giữ nguyên, không hạ xuống cho bằng ERP):**
ERP `BaseSearchModal` chỉ có 2 ô lọc (Mã phiếu đề nghị · Người lập) và 3 cột (STT · Mã · Người lập);
HRM có thêm ô lọc Loại chi + 4 cột (Loại chi · KH/NCC · Số tiền · Ngày lập). Đây là phần HRM làm
tốt hơn, bỏ đi chỉ làm người dùng khó tìm phiếu.

### Dấu `*` bắt buộc trên form phiếu chi lệch ERP (2026-08-27)

User bắt lỗi: "ở erp số phiếu đề nghị có bắt buộc đâu?". Soát toàn bộ nhãn trong ERP
`income_expenditure/bill_payments/form.blade.php` (`required-label` hoặc `<span class="text-danger">*</span>`):

| Trường | Nhánh lập từ đề nghị | Nhánh Chi thu nhập cho nhân viên | HRM trước |
| --- | --- | --- | --- |
| Số phiếu đề nghị (:33) | không | — | ❌ có `*` |
| Tài khoản có (:60 · :400) | **có** | **có** | ✅ |
| Loại chi (:76 · :416) | không | **có** | ❌ có `*` cả 2 nhánh |
| Hình thức thanh toán (:89 · :429) | không | không | ❌ có `*` ở nhánh loại 4 |
| Người nhận tiền (:102 · :442) | **có** | **có** | ✅ |
| Loại tiền (:113 · :453) · Tỷ giá (:127 · :466) · Người đề nghị (:142 · :481) | không | không | ❌ Tỷ giá có `*` ở nhánh loại 4 |
| Phòng ban (:149 · :487) | không | **có** | ✅ |
| Lý do chi (:158 · :501) | không | **có** | ✅ |
| Cột bảng "Số tài khoản nợ" | **có `(*)`** | — | ✅ |
| Cột bảng "Số tiền" | không | — | ❌ có `*` |

- [x] **FE** `BillPaymentForm.vue` — gỡ `*` ở 5 chỗ thừa (Số phiếu đề nghị · Loại chi nhánh A ·
      Hình thức thanh toán · Tỷ giá · cột "Số tiền chi"); `Loại chi` đổi thành
      `<Required v-if="isEmployeeBranch" />`.

⚠️ **Gỡ dấu `*` KHÔNG đụng luật validate** — đúng ERP: ERP cũng không đánh dấu `*` cho
`bill_payment_request_id` nhưng vẫn trả 422 "Bắt buộc nhập" và in lỗi ngay dưới ô
(`<% errors.bill_payment_request_id[0] %>`, :44-46). HRM giữ y vậy: lỗi inline hiện lúc GỬI DUYỆT.

ℹ️ Một chỗ HRM CỐ Ý chặt hơn ERP, **giữ nguyên, không nới**: ERP chỉ bắt buộc
`bill_payment_request_id` khi `type == 1 || 2 || 3`, nên "Chi thưởng thực hiện hợp đồng" (278 phiếu)
và "Thanh toán chi phí vận chuyển NCC" (63 phiếu) rơi khỏi MỌI nhánh validate — gửi duyệt được
phiếu không đề nghị, không dòng chi tiết. HRM bắt buộc cho cả 6 loại nhánh A (lý do đã ghi ở
docblock `BillPaymentStoreRequest`).

### Hạ luật đường "Lưu và gửi duyệt" về ĐÚNG ERP (2026-08-27)

User chốt: **lưu nháp giữ nguyên** (không bắt buộc trường nào — quyết định 2026-08-24), **lưu và
gửi duyệt thì validate y như ERP**. Đã được nêu rõ hệ quả trước khi chốt.

ERP `BillPaymentStoreRequest` :31-59 — 3 luật chung (`type` · `account_has` · `receiver`) + 2 nhánh:
`if ($this->type == 1 || 2 || 3)` và `if ($this->type == 4)`. **Chi thưởng thực hiện hợp đồng ·
Chi khác · Thanh toán chi phí vận chuyển NCC không thuộc nhánh nào** → không bắt buộc phiếu đề nghị,
cũng không bắt buộc dòng chi tiết.

- [x] **BE** `BillPayment.php` — thêm hằng `TYPES_REQUIRE_REQUEST = [1, 2, 3]` (hẹp hơn
      `TYPES_FROM_REQUEST`), kèm cảnh báo "đây là CỐ Ý, đừng siết lại".
- [x] **BE** `BillPaymentStoreRequest::rules()` — dựng lại đúng cấu trúc ERP: `details` +
      `details.*.account_dept` chuyển từ bộ luật CHUNG vào TỪNG nhánh; `bill_payment_request_id`
      required chỉ với `TYPES_REQUIRE_REQUEST`, 3 loại còn lại của nhánh A hạ về
      `nullable|exists`. Mọi `required` vẫn bật theo cờ `submit_after` (nháp không đụng).
- [x] **BE** `BillPaymentWriteService::assertReadyForSubmit()` — lớp chốt chặn thứ 2 (chống gọi
      thẳng `POST /{id}/submit`) khớp lại: `details` chỉ bắt buộc với `TYPES_REQUIRE_REQUEST` + loại
      4; `bill_payment_request_id` chỉ bắt buộc với `TYPES_REQUIRE_REQUEST` (giữ chặn khi `type`
      rỗng). Luật "dòng nào CÓ thì phải chọn tài khoản nợ" vẫn áp cho mọi loại — đó là chống dữ
      liệu rác, không phải bắt buộc nhập.
- [x] **BE** `BillPaymentWriteService::guardRequestLink()` — lớp 3, đổi
      `TYPES_FROM_REQUEST` → `TYPES_REQUIRE_REQUEST` ở vế "bắt buộc có đề nghị nguồn". Vế chống
      2 phiếu chi cùng trỏ 1 đề nghị GIỮ NGUYÊN (bảo vệ dữ liệu, chạy mọi lần lưu kể cả nháp).

**Đo thật sau khi sửa** (`Validator` dựng từ chính `rules()`, và gọi `assertReadyForSubmit()` qua
reflection trên object chưa lưu — không đụng dữ liệu):

| Ca | FormRequest | assertReadyForSubmit |
| --- | --- | --- |
| Gửi duyệt · Chi trả nhà cung cấp · trống đề nghị + trống chi tiết | ❌ `details` + `bill_payment_request_id` | ❌ cả 2 |
| Gửi duyệt · Chi thưởng NVKD · trống đề nghị | ❌ `details` + `bill_payment_request_id` | ❌ cả 2 |
| Gửi duyệt · Chi thưởng thực hiện hợp đồng · trống cả 2 | ✅ qua | ✅ qua |
| Gửi duyệt · Chi khác · trống cả 2 | ✅ qua | ✅ qua |
| Gửi duyệt · Thanh toán chi phí vận chuyển NCC · trống cả 2 | ✅ qua | ✅ qua |
| Lưu nháp · Chi trả nhà cung cấp · trống trơn | ✅ qua | (không chạy) |

⚠️ 3 lớp kiểm phải sửa CÙNG NHAU, lệch một lớp là hoặc thủng hoặc chặn oan:
`BillPaymentStoreRequest::rules()` → `assertReadyForSubmit()` → `guardRequestLink()`.

ℹ️ **KHÔNG đụng** nhánh Chi thu nhập cho nhân viên: ERP chỉ `required` 4 khoản
(`payment_diff_employee`, `payment_commission_month`, `payment_commission_quarter`,
`payment_commission_bonus_quarter`), HRM đang bắt đủ 6 (thêm `payment_delivery_money` +
`payment_other_cost`). Ngoài phạm vi câu hỏi của user — đã nêu để user quyết.

### Gọn lại bố cục khối chỉ đọc (2026-08-27)

- [x] **FE** bỏ 3 nhãn nhóm `<span class="group-label">` ("Đối tượng nhận tiền" / "Tài khoản nhận
      tiền" / "Ngân hàng trung gian") + xoá luôn style `.group-label` không còn ai dùng.
- [x] **FE** các ô đối tượng (Loại đối tượng · Khách hàng · Nhà cung cấp · Nhân viên · Phí) gộp
      CHUNG `form-row` với khối tài khoản nhận tiền — tên đối tượng đứng ngay trước số tài khoản
      của chính đối tượng đó (user chốt 2026-08-27: "cắt cái nhà cung cấp xuống cùng hàng với stk").
      Đã thử đặt chúng sau "Lý do chi" trong lưới thông tin chung nhưng user không chọn phương án đó.
      Dùng `<template v-if>` bọc từng nhóm thay vì `v-if` + `v-for` trên cùng element.
      ⚠️ Điều kiện của `<div class="form-row">` là `showPartyBlock || showBankBlock`, KHÔNG phải
      riêng `showBankBlock` — phiếu TIỀN MẶT không có khối tài khoản, gắn nhầm một điều kiện là mất
      luôn tên nhà cung cấp (đúng 16/96 đề nghị đang chờ tạo phiếu chi là tiền mặt).
      Khối "Ngân hàng trung gian" (6 ô, chỉ NCC nước ngoài) vẫn giữ `form-row` riêng.

### Gỡ nút riêng "Lưu và gửi KT trưởng duyệt" (2026-08-27)

User: "sao ở loại chi thu nhập cho nhân viên button lưu và gửi duyệt lại chuyển thành Lưu và gửi
KT trưởng duyệt vậy, để giống bên erp đi".

ERP `create.blade.php` :22-26 chỉ có MỘT nút `submitAndSendApprove()` mang chữ **"Lưu và gửi duyệt"**
cho mọi loại chi; cấp duyệt kế tiếp do LOGIC quyết chứ không do chữ trên nút — `status = 2` (Thủ quỹ),
riêng Chi thu nhập cho nhân viên thì `status = 5` (Kế toán trưởng).

- [x] **FE** `BillPaymentForm.vue` — `footerMenu.save_and_submit_approve` từ `!isEmployeeBranch`
      → `true`; xoá slot `#custom-actions` + nút riêng, xoá method `confirmSubmitEmployeeBranch()`
      (V2Footer đã tự hỏi xác nhận "Xác nhận lưu và gửi duyệt"), gỡ luôn import `V2BaseButton`
      không còn ai dùng.
      Luồng trạng thái KHÔNG đổi: `POST /{id}/submit` ở BE vẫn tự chọn `Chờ KT trưởng duyệt` (5)
      cho loại 4 và `Chờ chi tiền` (2) cho các loại còn lại — FE chưa bao giờ khai `status`.

### Form khóa quá tay khi CHƯA chọn phiếu đề nghị (2026-08-27)

User: "sao tôi chọn loại chi khác nó đang khác với bên erp vậy? bên erp chọn được loại tiền và
người đề nghị nó cũng tự gen ra mà?".

ERP khóa các ô copy-từ-đề-nghị bằng `ng-disabled="form.bill_payment_request_id"` — tức **chỉ khóa
sau khi đã gắn phiếu đề nghị**. HRM để `:disabled="true"` CỨNG nên form chết ngay từ đầu. Ngoài ra
2 ô "Người đề nghị" / "Phòng ban" của ERP có giá trị mặc định là NGƯỜI ĐANG ĐĂNG NHẬP, lấy từ getter
`_created_by_name || DEFAULT_USER.fullname` (`BillPaymentRequest.blade.php` :39-52 · `BillPayment.blade.php`
:60-70) — HRM để trống.

| Ô | ERP | HRM trước |
| --- | --- | --- |
| Loại tiền | `<select>`, khóa khi đã gắn đề nghị; nhánh Chi thu nhập cho nhân viên khóa cứng VND | input khóa cứng |
| Tỷ giá | input khóa, **nhảy theo loại tiền** (setter `type_money_id` đọc `TYPE_MONEYS[].exchange_rate`) | khóa, không nhảy |
| Người đề nghị | mặc định = tên người đăng nhập | trống |
| Phòng ban | mặc định = phòng ban người đăng nhập | trống |
| Lý do chi | nhập được, khóa khi đã gắn đề nghị | khóa cứng |

- [x] **FE** thêm computed `isRequestLocked` (`readonly || bill_payment_request_id`) — MỘT nguồn
      cho mọi ô copy-từ-đề-nghị, thay cho `:disabled="true"` rải rác.
- [x] **FE** Loại tiền: `V2BaseSelect` khi `canPickCurrency`, ngược lại giữ input chỉ đọc.
      `onCurrencyChange()` kéo `exchange_rate` từ danh mục (VND → 1; loại tiền chưa khai tỷ giá thì
      GIỮ số cũ, ghi đè 0 là mọi dòng quy đổi ra 0 đồng). `loadCurrencies()` phải giữ lại cột
      `exchange_rate` trong options — trước đó map bỏ mất.
- [x] **FE** `currentTypeMoneyId` đọc `form.type_money_id` khi chưa gắn đề nghị (trước đây luôn đọc
      `requestInfo`, nên chọn loại tiền xong cột ngoại tệ vẫn không đổi).
- [x] **FE** `proposerName` / `departmentDisplay` fallback về `creatorInfo` — lấy từ
      `meta.creator` (`{name, department_name}`) của endpoint đề nghị mà `loadTypePayments()` VỐN ĐÃ
      gọi, nên không thêm request nào và **không đụng màn Đề nghị thanh toán**.
      ⚠️ Không tra `$store.state.departments` để suy phòng ban: danh sách đó lọc `status = 1` nên
      người thuộc phòng ban đã khóa sẽ thấy ô trống (lý do BE đã ghi ở `currentEmployeeInfo()`).
- [x] **FE** Lý do chi: đổi `v-if="isRequestBranch"` → `v-if="isRequestLocked"` nên nhập được khi
      chưa gắn đề nghị.

### Bảng nhân viên thiếu 2 tab + ô tick "Cần thanh toán" (2026-08-28)

User: "loại chi thu nhập cho nhân viên ở dưới phần chi tiết nó có chia ra làm 2 tab, 1 tab chi tiết
và 1 tab chi tiết vụ việc mà?" · "và có cả cái tick chọn nữa cơ mà?".

ERP `bill_payments/form.blade.php` :673-700 (UNC :760-785 include **CÙNG 2 blade**):

| Tab | Cột |
| --- | --- |
| **Chi tiết** (`table_payment_employee.blade.php`) | tick · STT · Số tài khoản nợ · Tên tài khoản · Nhân viên · **Số dư** (`payment_money_request`) · **Số tiền chi** (`payment_money_approve`, ô nhập) · *(3 cột ngân hàng — CHỈ khi `$type == 'bill_payment_authorization'`)* |
| **Chi tiết vụ việc** (`table_payment_employee_detail.blade.php`) | tick · STT · Nhân viên · 6 khoản Số dư + Tổng · 6 khoản Số tiền chi (ô nhập) + Tổng |

Bản HRM trước gộp 18 cột vào MỘT bảng — đúng dữ liệu 6 khoản nhưng **thiếu hẳn ô "Số tiền chi" tổng
của tab 1**, mà chính số đó mới là vế ERP đối chiếu với tổng 6 khoản.

Quan hệ giữa 2 tab (ERP `BillPaymentDetail`):
- `sum_payment` (tổng 6 khoản chi) **phải bằng** `payment_money_approve` → không thì
  `is_valid_money` chặn: *"Tổng số tiền chi theo mã vụ việc và tổng số tiền đề nghị chi khác nhau!"*
- ô "Số tiền chi" khóa khi `!need_payment || payment_money_request <= 0`
- 6 ô khoản chi khóa khi `!need_payment || payment_money_approve <= 0` → **phải khai tổng ở tab 1
  trước, rồi mới bổ ra từng mã vụ việc ở tab 2**

- [x] **FE** `PaymentEmployeeTable.vue` — viết lại thành 2 `b-tab` (bootstrap-vue, đã dùng ở nhiều
      màn khác), mỗi tab một bảng đúng cột ERP; thêm cột tick + tick "chọn tất cả" ở tiêu đề; dòng
      bỏ tick làm mờ (`opacity: .45` — ERP tô chữ `#e9e9e9` gần như không đọc nổi trên nền trắng);
      2 hàm khóa ô nhập theo đúng 2 điều kiện ERP ở trên.
- [x] **FE** prop mới `showBankColumns` (mặc định **false**) cho 3 cột ngân hàng ở tab Chi tiết —
      đúng ERP: phiếu chi là chi TIỀN MẶT nên không có; màn Ủy nhiệm chi truyền `show-bank-columns`
      để giữ nguyên hành vi cũ. Trước đây 3 cột này hiện ở CẢ 2 màn.
- [x] **FE** `BillPaymentForm.vue` — `need_payment: true` khi hút nhân viên và khi mở phiếu cũ;
      computed `submittableDetails` (lọc theo tick) dùng cho `buildPayload`; `validateEmployeeMoney()`
      chặn trước khi gọi API với đúng câu ERP.
- [x] **FE** `BillPaymentAuthorizationForm.vue` — CHỈ 2 việc giữ cho khỏi thủng (KHÔNG đụng bố cục,
      màn đó vẫn để đợt sau): gán `need_payment: true` ở 3 chỗ nạp dòng, và `buildPayload` lọc theo
      tick qua computed `submittableDetails`. Thiếu 2 việc này thì bỏ tick ở màn UNC vẫn gửi dòng
      lên — mất tiền im lặng.

⚠️ `need_payment` để THẲNG trên từng dòng, không bắt chước map `form.employee_ids[employee_id]` của
ERP: map đó vỡ khi 1 nhân viên có 2 dòng (2 tài khoản nợ khác nhau) — bỏ tick dòng này là dòng kia
tắt theo.

### Hình thức thanh toán ở nhánh Chi thu nhập cho nhân viên (2026-08-28)

User: "khi chọn loại chi thu nhập cho nhân viên thì hình thức thanh toán để mặc định là TM và không
cho sửa mà".

ERP: `form.blade.php` :430 để `<select ng-model="form.type_payment" disabled>` ở nhánh loại 4, và
`create.blade.php` :47 gán sẵn `$scope.form.type_payment = 1` (TM) ngay khi mở màn Tạo — phiếu chi
thu nhập luôn chi tiền mặt. Nhánh lập-từ-đề-nghị thì :90 dùng
`ng-disabled="form.bill_payment_request_id"` → CHỌN ĐƯỢC khi chưa gắn đề nghị.

- [x] **FE** hằng `TYPE_PAYMENT_CASH = 1`; `form.type_payment` khởi tạo bằng hằng này thay vì `null`.
- [x] **FE** computed `isTypePaymentLocked` (`isEmployeeBranch || isRequestLocked`) + `typePaymentDisplay`
      + helper `typePaymentLabel()` — ô khóa hiện chữ "TM" lấy từ danh mục BE, không hard-code.
- [x] **FE** `onTypeChange()` ép `type_payment = TYPE_PAYMENT_CASH` khi chuyển sang nhánh Chi thu
      nhập cho nhân viên. ⚠️ BẮT BUỘC: ô đã khóa nên nếu không tự ép, hình thức của loại chi vừa bỏ
      (có thể là CK) vẫn nằm trong payload mà người dùng không thấy.

### Lý do hủy không được lưu + thiếu ô Ghi chú khi duyệt (2026-08-28)

User: "khi phiếu chi thu nhập cho nhân viên ở trạng thái Chờ KT trưởng duyệt, tôi vào hủy phiếu và
nhập lý do hủy đang không lưu lại, phải lưu lại cho tôi và khi xem chi tiết phải hiển thị lý do đó
lên" · "ở bên erp tôi thấy khi vào duyệt nó còn có trường nhập ghi chú nữa mà".

**Vì sao trước đây mất:** bảng `bill_payments` KHÔNG có cột `note` (verify `SHOW CREATE TABLE` —
24 cột, không có). ERP vẫn dựng ô "Ghi chú" ở `formShow.blade.php` :135 · :460 và khai
`'note' => Rule::requiredIf($this->status == 4)` trong `BillPaymentStoreRequest` cho một cột không
tồn tại → **bên ERP chữ gõ vào cũng bay hơi**. Bản HRM trước bám theo, lý do hủy chỉ đi vào nội dung
thông báo chuông; riêng nhánh Chi thu nhập cho nhân viên còn không có đề nghị nguồn để ghi nhờ lịch
sử → mất sạch. Đây là chỗ **ĐỔI quyết định 2026-08-19**.

**Nơi lưu:** `catalog_histories` (chuẩn đang dùng cho phiếu Finance) — KHÔNG migration trên bảng
dùng chung với cổng ERP.

- [x] **BE** `app/Services/CatalogHistoryService.php` — thêm `'bill_payments'` vào whitelist
      `TABLES`. ⚠️ File DÙNG CHUNG: chỉ THÊM một entry vào hằng, không đụng logic, không ảnh hưởng
      18 màn đang dùng (tiền lệ: `bill_payment_requests` đã được thêm ở chính feature này).
- [x] **BE** `BillPayment` — thêm `statusName()` + `logStatusHistory($id, $old, $new, $note)`, khuôn
      copy nguyên `BillPaymentRequest::logStatusHistory()`. Ghi chú suông (không đổi trạng thái) vẫn
      lưu; lỗi log `catch (\Throwable)` để không làm hỏng nghiệp vụ duyệt/hủy.
- [x] **BE** `BillPaymentApprovalFlowService::cancel()` — ghi lịch sử kèm `$reason`.
- [x] **BE** `BillPaymentApprovalFlowService::approve()` — nhận thêm `$note`, ghi lịch sử ở CẢ 2 mốc
      (Kế toán trưởng duyệt · Thủ quỹ chi tiền).
- [x] **BE** `BillPaymentWriteService::submit()` — ghi lịch sử mốc gửi duyệt, để timeline liền mạch.
- [x] **BE** `BillPaymentApproveRequest` — thêm `'note' => 'nullable|string|max:500'`; Controller
      truyền xuống service.
- [x] **BE** `BillPaymentDetailResource` — trả `cancel_reason` + `approve_note`, đọc từ
      `catalog_histories` (1 truy vấn, cache tĩnh theo id cho cả 2 khóa).
      ⚠️ So theo **TÊN** trạng thái (`{"Trạng thái":"Hủy"}`) vì service lưu nhãn tiếng Việt chứ
      không lưu id — đó là hợp đồng của `CatalogHistoryService`, đổi sang id là vỡ mọi màn khác.
      `approve_note` lấy dòng mới nhất có ghi chú ở mốc "Đã duyệt" HOẶC "Chờ chi tiền" — phiếu
      Chi thu nhập cho nhân viên đi qua 2 cấp nên không cố định một trạng thái.
- [x] **FE** `ApproveBillPaymentModal.vue` — thêm ô "Ghi chú" (không bắt buộc, đúng ERP: chỉ khi HỦY
      mới bắt buộc), gửi kèm payload. ⚠️ `onShow()` phải reset `note = ''`: popup không hủy component
      khi đóng nên ghi chú của lần duyệt trước còn nguyên trong ô.
- [x] **FE** `_id/index.vue` — khối hiển thị "Lý do hủy" (chữ đỏ) + "Ghi chú của người duyệt" (chữ
      thường), ẩn hẳn khi không có.
      🔶 Sửa vị trí 2026-08-28: bản đầu đặt SAU form (trên khối nút) với lý do "không đẩy phiếu
      xuống" — SAI trong thực tế. User hủy phiếu thật rồi báo "vẫn không thấy đâu" trong khi dữ liệu
      đã lưu đúng (log id 213, phiếu TPE.PC0826.00008, note `huyrrrrrrrr`) và API cũng trả đúng
      `cancel_reason`: bảng chi tiết nhánh Chi thu nhập cho nhân viên dài cả màn hình nên phải cuộn
      tới cuối trang mới nhìn thấy. Nay đặt ĐẦU MÀN, trước cả phiếu, nền vàng nhạt + viền trái cam
      để không lẫn vào các card trắng của form.
      ⚠️ Bài học: "đặt cuối trang cho khỏi chiếm chỗ" chỉ đúng khi trang ngắn — màn này có bảng
      18 cột × N nhân viên.

**Đo thật** (transaction rồi rollback, phiếu id 1360): ghi 2 dòng log → Resource trả
`cancel_reason = "Sai so tien, huy de lap lai"` · `approve_note = "Da doi chieu chung tu"`. ✅


### 🐞 Khối "Lý do hủy" không hiện dù dữ liệu đúng — computed bị data che (2026-08-28)

User báo 2 lần "vẫn không thấy đâu". Đã loại trừ bằng đo đạc trước khi đoán:

| Kiểm tra | Kết quả |
| --- | --- |
| DB `catalog_histories` | ✅ có dòng note `huyrrrrrrrr` cho phiếu 1360 |
| Resource gọi trực tiếp | ✅ `cancel_reason = "huyrrrrrrrr"` |
| API qua HTTP kernel (JWT user 13) | ✅ HTTP 200, `cancel_reason` đúng |
| Compile FE (template + babel) | ✅ sạch |
| **Trình duyệt** | ❌ khối không render |

**Nguyên nhân:** `_id/index.vue` đã có `cancelReason: ''` trong `data()` (ô nhập của popup Hủy
phiếu). Computed `cancelReason` thêm vào bị Vue 2 **bỏ qua im lặng** — chỉ `[Vue warn]: The computed
property "cancelReason" is already defined in data.` trong console. Khối luôn đọc chuỗi rỗng của ô
nhập ⇒ `v-if` không bao giờ đúng.

- [x] **FE** đổi tên computed → `savedCancelReason` / `savedApproveNote`, docblock ghi rõ cái bẫy.

⚠️ **Bài học:** compile + test API SẠCH vẫn có thể là màn trắng. Khối `v-if` không hiện mà dữ liệu
chắc chắn đúng → việc ĐẦU TIÊN là đọc console tìm `[Vue warn]`, không phải nghi cache/build.
Trước khi thêm computed vào component có sẵn: grep tên đó trong CẢ file (`data` / `props` / `methods`).

**Verify bằng Playwright (user cho phép mở trình duyệt vì soi code đã hết đường):**

| Phiếu | Loại chi | Kết quả |
| --- | --- | --- |
| TPE.PC0826.00008 (1360) | Chi thu nhập cho nhân viên, đã hủy | ✅ khối vàng "Lý do hủy: huyrrrrrrrr" ở đầu màn; 2 tab "Chi tiết" / "Chi tiết vụ việc" |
| TPE.PC0826.00007 (1359) | Chi thu nhập cho nhân viên, hủy TRƯỚC khi có code | ✅ không hiện khối (đúng — không có dữ liệu); 2 tab render đúng cột |
| TPE.PC0826.00006 (1358) | Chi trả nhà cung cấp, CK | ✅ hiện khối "Nhà cung cấp" + "Số tài khoản" / "Tên ngân hàng"; **0 lỗi console** |

🔶 **Còn tồn đọng (chưa xử lý, không chặn chức năng):** màn chi tiết phiếu **Chi thu nhập cho nhân
viên** in 1 lỗi console `[vee-validate] Validating a non-existent field: "#1". Use "attach()" first.`
Xuất hiện ở CẢ 1359 và 1360, KHÔNG có ở phiếu loại 1 (1358). Chưa xác định được là lỗi có sẵn hay
mới — cần so với bản trước khi đổi `PaymentEmployeeTable`. Màn vẫn hiển thị đủ, không vỡ.

### Popup Hủy: thêm ô Ghi chú, bỏ dòng chú thích đã sai (2026-08-28)

User: "thêm trường ghi chú vào cho tôi như bên erp nữa, ngoài cái lý do hủy vẫn thêm cả cái ghi chú
nữa và bỏ cái text này *Lý do này được gửi kèm trong thông báo tới người lập phiếu, hệ thống không
lưu lại trên phiếu chi.* đi".

Dòng chú thích đó ĐÃ SAI kể từ khi có `logStatusHistory()` — nay lưu thật, nên bỏ hẳn chứ không
sửa chữ.

**Cách lưu 2 giá trị trong 1 dòng log** (bảng `bill_payments` không có cột nào chứa được):
`catalog_histories.note` giữ **Lý do hủy**, còn **Ghi chú** vào khóa `'Ghi chú'` của `new_value`
(cùng chỗ với `{"Trạng thái":"Hủy"}`). Không thêm bảng, không migration.

- [x] **BE** `BillPayment::logStatusHistory()` — nhận thêm `array $extraNew = []`, merge vào
      `new_value`.
- [x] **BE** `BillPaymentCancelRequest` — thêm `'note' => 'nullable|string|max:500'` + 2 câu lỗi;
      docblock viết lại (bản cũ khẳng định "KHÔNG được lưu xuống DB" — nay sai).
- [x] **BE** `BillPaymentApprovalFlowService::cancel($id, $reason, $note = null)` — ghi
      `['Ghi chú' => $note]` khi có; Controller truyền `note` xuống.
- [x] **BE** `BillPaymentDetailResource` — thêm helper `statusExtra()` và khóa `cancel_note`.
- [x] **FE** `_id/index.vue` — popup Hủy thêm ô "Ghi chú" (tùy chọn, dưới ô Lý do hủy), XÓA dòng
      chú thích cũ; `cancelNote` trong data + reset khi mở popup + gửi kèm payload; khối vàng đầu
      màn hiện 3 dòng: Lý do hủy (đỏ) · Ghi chú · Ghi chú của người duyệt.

**Verify Playwright** (mở popup, KHÔNG bấm Xác nhận — không đụng dữ liệu nghiệp vụ thật):
phiếu TPE.PC0826.00005 (Chi thu nhập cho nhân viên, Chờ KT trưởng duyệt) → popup có đúng 2 ô
`["Lý do hủy *", "Ghi chú"]`, dòng text cũ đã biến mất (`stillHasOldText: false`).
**Verify BE** (transaction rollback): ghi log kèm `['Ghi chú' => ...]` → Resource trả
`cancel_reason = "Sai phong ban"` · `cancel_note = "Lap lai vao thang sau"`. ✅


## Đợt sửa nhanh — màn Tạo phiếu chi: bỏ loại chi mặc định + 3 chỉnh ô nhập (2026-08-28)

User: *"trong màn tạo phiếu chi, khi vào không để mặc định là loại chi trả nhà cung cấp nữa, và
thêm nút xóa vào dropdown cho tôi, loại tiền cũng thêm dropdown vào, thêm kí hiệu required vào cái
loại chi nữa"*.

⚠️ **ĐẢO LẠI yêu cầu 2026-08-24** (mục "Phiếu chi — màn Tạo bám lại ERP"): hôm đó user chốt chọn
sẵn "Chi trả nhà cung cấp" + bỏ nút × để ô "Số phiếu đề nghị" bấm được ngay. Nay bỏ cả hai. Đừng
"sửa về cho đúng ERP" ở lượt sau — cả 2 điểm đều là quyết định của user, không phải lệch cổng port.

- [x] **FE** `pages/finance/bill-payments/components/BillPaymentForm.vue`
      - `mounted()`: xóa nhánh `else { this.form.type = TYPE_PAYMENT_SUPPLIER }` → màn Tạo vào
        thẳng thì ô Loại chi **để trống**. Gỡ luôn hằng `TYPE_PAYMENT_SUPPLIER` (hết chỗ dùng).
      - Ô **Loại chi**: bỏ `:allow-clear="false"` → hiện nút ×.
      - Ô **Loại tiền**: bỏ `:allow-clear="false"` → hiện nút ×.
      - Nhãn **Loại chi**: `<Required v-if="isEmployeeBranch" />` → `<Required />` (mọi nhánh).
- [x] **BE** không đụng gì.

**Vì sao bỏ mặc định vẫn an toàn** (đã soi trước khi xóa, không đoán):
- `isRequestBranch` (`:770-772`) đã coi `typeNumber === null` là nhánh A → ô "Số phiếu đề nghị"
  vẫn render và bấm mở popup được ngay khi chưa chọn loại chi. Đây đúng là lý do của yêu cầu
  2026-08-24, và nó vốn đã được xử lý bằng computed chứ không cần giá trị mặc định.
- `PaymentRequestSearchModal` nhận `:type-options="requestTypeOptions"` (lọc từ danh mục BE),
  **không** lọc theo `form.type` → popup không bị rỗng.
- `applyPaymentRequest()` tự gán `this.form.type = data.type` khi chọn phiếu đề nghị.
- Xóa trắng Loại tiền: `onCurrencyChange()` (`:1121-1131`) gặp id rỗng thì đưa `exchange_rate = 1`,
  `isVnd` thành true → không có trạng thái "ngoại tệ mà thiếu tỷ giá".
- Xóa trắng Loại chi khi ĐÃ gắn đề nghị là không thể: `isTypeLocked` khóa ô ngay khi có
  `bill_payment_request_id`.

⚠️ **Dấu `*` ở Loại chi CỐ Ý lệch ERP**: ERP để nhãn trần ở nhánh lập-từ-đề-nghị (`form.blade.php`
:76), chỉ nhánh loại 4 mới `required-label` (:416). BE cũng chỉ bắt buộc `type` khi **gửi duyệt**
(`BillPaymentStoreRequest.php:105` — `$required = $this->submittingForApprove() ? 'required' :
'nullable'`), lưu nháp vẫn để trống được. Dấu `*` mang nghĩa "bắt buộc để hoàn tất phiếu", giống ô
Tài khoản có / Người nhận tiền.

**Verify:** `vue-template-compiler` + `@babel/parser` parse sạch. Đã grep xác nhận
`TYPE_PAYMENT_SUPPLIER` không còn chỗ nào dùng, `Required` và `isEmployeeBranch` vẫn còn dùng nơi
khác nên import/computed không thừa.
⚠️ Chưa mở trình duyệt.

📌 File này là **LF** (khác `create.vue` và `PaymentRequestSearchModal.vue` cùng thư mục — CRLF).
Repo `hrm-client` trộn 2 kiểu xuống dòng, sửa bằng script thì phải dò từng file chứ đừng ép chung.

### Checkpoint — 2026-08-28
Vừa hoàn thành: màn Tạo phiếu chi bỏ loại chi mặc định, thêm nút × cho Loại chi + Loại tiền, thêm
dấu `*` cho Loại chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/create` — xác nhận ô Loại chi trống khi vào, có
nút ×, có dấu `*`; ô "Số phiếu đề nghị" vẫn bấm mở popup được khi chưa chọn loại chi; chọn 1 phiếu
đề nghị xem Loại chi tự điền theo phiếu.
Blocked: không.


## Bổ sung cùng đợt — xóa loại tiền phải xóa tỷ giá + lưu nháp bắt buộc loại chi (2026-08-28)

### 1. Xóa loại tiền -> tỷ giá phải trống

User: *"khi xóa loại tiền đi thì tỉ giá phải mất chứ"*. Đúng — bản vừa thêm nút × còn sai:
`onCurrencyChange()` gộp 2 trường hợp `!id || id === CURRENCY_VND_ID` nên **xóa trắng loại tiền
vẫn ra tỷ giá = 1**, người dùng tưởng phiếu đang là VND.

- [x] **FE** `BillPaymentForm.vue::onCurrencyChange()` — tách nhánh: `!id` → `exchange_rate = ''`;
      `id === CURRENCY_VND_ID` → `= 1`; còn lại lấy theo danh mục như cũ.
      Ô Tỷ giá lúc đó vẫn disabled (`isVnd` true khi chưa có loại tiền) và hiện placeholder "Tỷ giá".
      Không sợ NaN: chỗ tính quy đổi dùng `Number(this.form.exchange_rate || 1)` (:1630, :1634).

### 2. Lưu nháp BẮT BUỘC chọn loại chi

User: *"khi lưu nháp thì bắt buộc chọn loại chi chứ?"* — đúng, và đây chính là điều đã chốt cho màn
**Ủy nhiệm chi** ngày 2026-08-27 ("Lưu nháp chỉ bắt buộc mỗi Loại chi"); Phiếu chi chưa theo.

- [x] **BE** `Modules/Finance/Http/Requests/BillPayment/BillPaymentStoreRequest.php` —
      `'type' => $required . '|integer|in:…'` → **`'required|integer|in:…'`** (luôn bắt buộc).
      `BillPaymentUpdateRequest` **extends** class này nên màn Sửa ăn theo, không phải sửa 2 chỗ.
      Sửa kèm docblock dòng "LƯU NHÁP … KHÔNG bắt buộc trường nào cả" để ghi rõ ngoại lệ.
- [x] **FE** đã có sẵn dấu `*` ở nhãn Loại chi (làm ở mục trên) và `applyServerErrors()` map 422 vào
      ô — không cần thêm validate FE, giống hệt Ủy nhiệm chi (nơi cũng chỉ để `<Required />` + dựa
      vào 422 của BE).

**Verify BE — dựng FormRequest thật rồi chạy `Validator`, không đoán theo mắt:**

| Trường hợp | Kết quả |
| --- | --- |
| Lưu nháp, KHÔNG có `type` | ❌ 422 "Bắt buộc chọn loại chi" |
| Lưu nháp, `type = 1` | ✅ hợp lệ, **không bắt buộc thêm trường nào** |
| Lưu nháp, `type = 99` (rác) | ❌ "Loại chi không hợp lệ" — whitelist vẫn nguyên |
| Lưu và duyệt, KHÔNG có `type` | ❌ "Bắt buộc chọn loại chi" |
| Lưu và duyệt, chỉ có `type = 1` | ❌ vẫn đòi `account_has`, `receiver`, `details`, `bill_payment_request_id` |

`php -l` sạch · FE parse sạch. ⚠️ Chưa mở trình duyệt.

### Checkpoint — 2026-08-28
Vừa hoàn thành: xóa loại tiền thì tỷ giá trống theo; `type` luôn bắt buộc kể cả lưu nháp (BE),
khớp khuôn màn Ủy nhiệm chi.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/create` — bấm Lưu nháp khi chưa chọn Loại chi phải
thấy lỗi đỏ ngay dưới ô; chọn ngoại tệ rồi bấm × ở Loại tiền phải thấy ô Tỷ giá trống.
Blocked: không.


## Khối ngân hàng màn Tạo phiếu chi — bám ERP y nguyên (2026-08-28)

User mở `/finance/bill-payments/create`, chọn đề nghị **TPE.DNTT0726.00240**: *"phần ngân hàng nó
đang khác vậy, bên erp nó cho chọn ngân hàng và có cả phần ngân hàng trung gian nữa mà"*.
Hướng đã chốt: **bám ERP y nguyên** (kể cả chỗ ERP làm dở).

**Dữ liệu thật của phiếu 4162** (đo, không đoán): `type=1` · `type_payment=2` · `supplier_id=11745`
· `bank_id=45` · `swift_code=URCBCN2H` · `iban` rỗng · toàn bộ `mid_*` rỗng.
NCC 11745: `customers.customer_type = 3` (nước ngoài), có **1** dòng `supplier_banks` (`is_main=1`),
`mid_banks` rỗng.

### 4 chỗ lệch đã tìm ra

| # | ERP `bill_payments/form.blade.php` | HRM (trước sửa) |
| --- | --- | --- |
| 1 | Select **"Ngân hàng"** :238-247, liệt kê `supplier_banks` `is_main=1` | Không có ô này |
| 2 | Khối **"Ngân hàng trung gian"** :294-350 **luôn dựng** khi NCC nước ngoài (select `disabled` + 6 ô, chưa có dữ liệu thì in `____`) | `showMidBankBlock` đòi phải CÓ dữ liệu `mid_*` → mất hẳn khối |
| 3 | Nhánh nước ngoài **không có** Chi nhánh / Thành phố (2 ô đó thuộc nhánh trong nước :353-386) | Đẩy cả 2 ô vào → 2 ô trống thừa |
| 4 | Phân biệt bằng `supplier->type == 3` (`BillPaymentRequestController@getData` :461) | Đoán bằng `swift_code \|\| iban_number` |

⚠️ **Chỗ 4 — comment cũ trong code SAI một nửa**: nó viết "customers KHÔNG có cột `type`, copy
nguyên là 500". Không có `type` là đúng, nhưng cột đó trên DB gộp tên là **`customers.customer_type`**
— chính là cái ERP so. Cách đoán cũ sai 2 chiều: NCC nước ngoài chưa khai swift/iban thì rơi nhầm
sang khối trong nước; phiếu trong nước lỡ có swift lại hiện khối nước ngoài.

### ⚠️ 2 ô chọn ngân hàng bên ERP là NÚT CHẾT — đã kiểm 3 lớp trước khi bê sang

1. Select "Ngân hàng" của màn phiếu chi **không có `ng-change`** (:239) — khác hẳn màn Đề nghị
   thanh toán (`bill_payment_requests/form.blade.php` :235 có `ng-change="form.changeBank()"`)
   ⇒ đổi ngân hàng thì 6 ô bên dưới KHÔNG đổi theo.
2. `BillPayment.submit_data` (`partials/classes/.../BillPayment.blade.php` :405-427) **không gửi**
   `bank_id` / `mid_bank_id`.
3. `BillPaymentController@update` :219 chỉ nhận `bill_payment_request_id` / `account_has` / `receiver`.

⇒ Bên ERP chọn ngân hàng khác rồi lưu thì **không có gì được lưu**. Select "Ngân hàng trung gian"
ERP để `disabled` sẵn. HRM nay copy đúng hành vi đó: 2 ô bind vào `requestInfo` (dữ liệu chỉ đọc,
KHÔNG nằm trong payload, không kích guard "chưa lưu"). **Đừng "sửa cho nó chạy" ở lượt sau** —
muốn cho sống là đổi nghiệp vụ, phải hỏi user.

### Việc đã làm

- [x] **BE** `BillPaymentRequestDetailResource` — thêm `supplier_type` · `banks` · `mid_banks`;
      2 helper `public static supplierType()` / `supplierBanks($item, $isMain)` đọc thẳng
      `customers.customer_type` và `supplier_banks` theo `supplier_id` (endpoint chỉ trả 1 phiếu
      nên không N+1; entity cố ý không có quan hệ `supplier()`).
      Map tên cột: `supplier_banks.iban` → `iban_number`, `.address` → `bank_address` (đúng
      `changeBank()` của ERP).
- [x] **BE** `BillPaymentDetailResource` (màn Sửa / Xem) — thêm `bank_id` · `mid_bank_id` ·
      `supplier_type` · `banks` · `mid_banks`, **gọi lại 2 helper static ở trên**. Thiếu bước này
      là mở lại phiếu đã lưu thì khối ngân hàng biến mất sạch (cả 2 cờ hiển thị đều cần
      `supplier_type`) — suýt thành lỗi hồi quy.
- [x] **FE** `BillPaymentForm.vue` — port 6 getter điều kiện của ERP
      (`BillPaymentRequest.blade.php` :102-148): `isSupplierParty` · `isCustomerParty` ·
      `isRequestTransfer` · `isForeignBank` · `isInlandSupplierBank` + `supplierTypeNumber`.
      · Khối **trong nước** (`type_supplier_transfer_inland || type_customer_transfer ||
        type_employee_has_contract_transfer`): đúng **5 ô** chỉ đọc, bỏ Swift/IBAN/Địa chỉ.
      · Khối **NCC nước ngoài**: select "Ngân hàng" (chọn được, không lưu) + 6 ô · select
        "Ngân hàng trung gian" (`disabled`) + 6 ô — **luôn dựng**, kể cả khi mid_* rỗng.
      · `requestInfo` thêm `supplier_type` · `bank_id` · `mid_bank_id` · `banks` · `mid_banks`
        (khai sẵn trong `emptyRequestInfo()` — Vue 2 không reactive với khóa thêm sau).
      · Helper `toBankOptions()` ghép nhãn `"<tên tài khoản> - <số tài khoản>"` đúng ERP.

**Verify (đo thật, không đoán):**

| Kiểm tra | Kết quả |
| --- | --- |
| `php -l` 3 file BE | Sạch |
| FE `vue-template-compiler` + `@babel/parser` | Sạch |
| `BillPaymentRequestDetailResource` phiếu 4162 | `supplier_type=3` · `bank_id=45` · `banks` 1 dòng · `mid_banks` 0 |
| `BillPaymentDetailResource` phiếu chi 1358 (NCC Ý, TPE.DNTT0726.00236) | `supplier_type=3` · `bank_id=103` · `banks` 1 dòng · `mid_banks` 0 |
| Phân bố `customer_type` của NCC (đề nghị loại 1 + CK) | 1: 35 · 2: 1.842 · 3: 718 — **không có NULL** nên đổi sang so `supplier_type` không làm màn nào mất khối |

⚠️ Chưa mở trình duyệt.

### Checkpoint — 2026-08-28
Vừa hoàn thành: dựng lại khối ngân hàng màn Tạo/Sửa phiếu chi theo đúng 2 nhánh của ERP, thêm
2 ô chọn ngân hàng (tra cứu, không lưu — như ERP), BE trả `banks`/`mid_banks`/`supplier_type` ở
CẢ 2 endpoint.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/bill-payments/create`, chọn TPE.DNTT0726.00240 — phải thấy ô
"Ngân hàng" có 1 lựa chọn (HAINING ZELL … - 2010 0016 0123 337) đang chọn sẵn, 6 ô Số TK/Tài
khoản/Tên NH/Swift/IBAN/Địa chỉ, rồi ô "Ngân hàng trung gian" khóa + 6 ô trống. Kiểm thêm 1 phiếu
NCC trong nước (chỉ 5 ô, có Chi nhánh/Thành phố) và mở lại phiếu chi cũ 1358 xem khối còn nguyên.
Blocked: không.


User: *"để riêng phần ngân hàng với phần ngân hàng trung gian ra cho dễ nhận biết"* → sau đó chốt
lại: *"đừng để thành card như thế để mỗi bên 2 cột ấy"*.

Bản đầu để cả 14 ô trong MỘT `form-row` — mà 2 nhóm **trùng tên nhau cả 6 ô** (Số tài khoản /
Tài khoản / Tên ngân hàng / Swift Code / IBAN Number / Địa chỉ) nên nhìn không ra ô nào của nhóm
nào. Bản thử thứ 2 bọc mỗi nhóm trong 1 khung có viền + tiêu đề — **user không lấy**.

- [x] **FE** `BillPaymentForm.vue` — bố cục CUỐI bám đúng ERP: `form-row` ngoài chứa 2 nửa
      `col-md-6` (trái = Ngân hàng, phải = Ngân hàng trung gian); trong mỗi nửa, ô CHỌN đứng riêng
      một `form-row` ở đầu cột, 6 ô chỉ đọc xếp `col-md-6` (2 ô mỗi hàng).
      Khớp ERP `form.blade.php` :234 / :293 (2 `col-md-6`) + ô con `col-md-6`.
      Ranh giới 2 nhóm nhận ra bằng **vị trí trái/phải**, không bằng viền → nhãn 2 ô chọn giữ
      nguyên chữ ERP: "Ngân hàng" và "Ngân hàng trung gian".
- [x] **FE** gỡ bỏ 2 class `.bank-group` / `.bank-group-title` đã thêm ở bản thử.

**Verify:** FE parse sạch, đã grep xác nhận không còn class `bank-group` nào sót. ⚠️ Chưa mở trình duyệt.

<!-- bản thử (đã bỏ) -->
### ~~Bản thử: 2 khung có viền~~ — ĐÃ BỎ theo yêu cầu user (giữ lại để không thử lại lần nữa)

User: *"để riêng phần ngân hàng với phần ngân hàng trung gian ra cho dễ nhận biết"*.

Bản trước để cả 14 ô trong MỘT `form-row` — mà 2 nhóm **trùng tên nhau cả 6 ô** (Số tài khoản /
Tài khoản / Tên ngân hàng / Swift Code / IBAN Number / Địa chỉ) nên nhìn không ra ô nào của nhóm
nào. ERP cũng tách, bằng 2 cột `col-md-6` cạnh nhau (:234 và :293).

- [x] **FE** `BillPaymentForm.vue` — 2 khung `.bank-group` xếp DỌC, mỗi khung có viền mảnh +
      tiêu đề nhỏ **"NGÂN HÀNG NHẬN TIỀN"** / **"NGÂN HÀNG TRUNG GIAN"**. Xếp dọc chứ không 2 cột
      như ERP để 6 ô bên trong không bị bóp còn nửa bề rộng.
      Nhãn ô chọn bên trong rút gọn còn **"Ngân hàng"** ở CẢ HAI khung — tên khung đã mang chữ
      "trung gian" rồi, không lặp 2 lần trong cùng một khung.
- [x] **FE** thêm 2 class `.bank-group` / `.bank-group-title` vào `<style lang="scss" scoped>` của
      màn (v2-styles không có sẵn, cùng lý do với `.card-header.section-header` đã copy trước đó).

**Verify:** FE parse sạch. ⚠️ Chưa mở trình duyệt.


### CHỐT bố cục khối ngân hàng: hàng ngang, KHÔNG chia khung (2026-08-28)

User: *"thôi bạn lại để hàng ngang như vừa xong đi, không chia card ra là được"*.

**Đã thử 3 phương án, chốt phương án 1** — ghi lại đủ để không ai dựng lại 2 phương án đã bị bỏ:

| # | Phương án | Kết quả |
| --- | --- | --- |
| 1 | 14 ô `col-md-3` xếp hàng ngang liên tục | ✅ **CHỐT** |
| 2 | Mỗi nhóm 1 khung có viền + tiêu đề, xếp dọc | ❌ *"đừng để thành card như thế"* |
| 3 | 2 nửa `col-md-6` cạnh nhau + ô con `col-md-6` (đúng ERP) | ❌ *"để hàng ngang như vừa xong"* |

- [x] **FE** `BillPaymentForm.vue` — trả về MỘT `form-row`, 14 ô cùng cỡ `col-md-3` như mọi ô khác
      của form. Ranh giới 2 nhóm nhận ra bằng chính 2 ô CHỌN ("Ngân hàng" / "Ngân hàng trung gian")
      đứng mở đầu mỗi nhóm.
- [x] **FE** không còn class riêng nào (`.bank-group` / `.bank-group-title` đã gỡ ở bước trước).

⚠️ Ghi chú chống lặp đã cắm ngay trong template (khối comment trên `showForeignBankBlock`):
**đừng "sửa cho giống ERP" bằng cách chia 2 cột, và đừng bọc khung** — cả hai đều đã bị user bỏ.

**Verify:** FE parse sạch; grep xác nhận không còn `bank-group`, `col-md-6` duy nhất còn lại là ô
"Lý do chi" vốn có. ⚠️ Chưa mở trình duyệt.


### CHỐT LẦN CUỐI — hàng ngang + 1 dòng tiêu đề ngăn nhóm (2026-08-28)

User: *"ý tôi là để hàng ngang nhưng phân biệt rõ ra là phần nào với phần nào ấy"*.

Bảng 4 phương án đã thử (giữ lại để khỏi quay vòng lần nữa):

| # | Phương án | Kết quả |
| --- | --- | --- |
| 1 | 14 ô `col-md-3` chảy liền, không phân nhóm | ❌ không nhìn ra nhóm (2 nhóm trùng tên cả 6 ô) |
| 2 | Mỗi nhóm 1 khung có viền + tiêu đề, xếp dọc | ❌ *"đừng để thành card như thế"* |
| 3 | 2 nửa `col-md-6` cạnh nhau (đúng ERP) | ❌ *"để hàng ngang như vừa xong"* |
| 4 | Hàng ngang `col-md-3` + **1 dòng tiêu đề `col-12`** chen giữa | ✅ **CHỐT** |

- [x] **FE** `BillPaymentForm.vue` — trong CÙNG một `form-row`, chèn 2 dòng
      `<div class="col-12"><p class="field-group-title">…</p></div>`:
      **"NGÂN HÀNG NHẬN TIỀN"** trước 7 ô đầu, **"NGÂN HÀNG TRUNG GIAN"** trước 7 ô sau.
      `col-12` chiếm trọn bề ngang nên tự đẩy nhóm sau xuống dòng mới — không cần khung, không
      cần chia cột. Ô vẫn `col-md-3` như mọi ô khác của form.
      Nhãn ô CHỌN của nhóm 2 rút còn "Ngân hàng" (tên nhóm đã mang chữ "trung gian").
- [x] **FE** class `.field-group-title` trong `<style scoped>`: chữ nhỏ IN HOA xám + **1 đường kẻ
      mảnh dưới**, KHÔNG viền bao, KHÔNG nền — đúng ranh giới user chấp nhận.

**Verify:** FE parse sạch. ⚠️ Chưa mở trình duyệt.


## Đợt sửa — Số tiền chi vượt Số tiền đề nghị chi: báo lỗi + chặn lưu/duyệt (2026-08-28)

User: *"cả màn duyệt phiếu chi tiền nữa"* (làm sau khi sửa y hệt cho màn Ủy nhiệm chi rồi Phiếu thu —
xem `.plans/gop-db/finance-bill-payment-authorization/plan.md` và `.plans/gop-db/finance-bill-income/plan.md`).

Cùng một lỗi ở **2 chỗ** của màn Phiếu chi, sửa cả hai cho khớp nhau:

**A. Popup DUYỆT** (`components/ApproveBillPaymentModal.vue`) — ô "Số tiền thực chi" của thủ quỹ:
- [x] `onAmountInput()` bỏ kẹp cận trên, chỉ còn chặn số ÂM.
- [x] Thêm `isAmountOverRequest(row)` + `amountErrorText(row, index)` -> ô viền đỏ + chữ đỏ
      *"Không được lớn hơn số tiền đề nghị chi (<số>)"* ngay lúc gõ (popup dùng `div.text-small-error`
      chứ không phải `V2BaseError`).
- [x] `validateRows()` thêm nhánh chặn -> `submit()` KHÔNG gọi API.

**B. Màn TẠO / SỬA** (`components/BillPaymentForm.vue`) — ô "Số tiền chi" ở bảng chi tiết nhánh A:
- [x] Bỏ prop `:max`; `clampApprove()` chỉ còn chặn số ÂM.
- [x] Thêm `isApproveOverRequest` + `approveErrorText` (qua `V2BaseError`).
- [x] `validateApproveAmounts()` chặn ngay đầu `save()` — cho CẢ "Lưu nháp" lẫn "Lưu và gửi duyệt",
      toast nói rõ dòng số mấy. Đặt TRƯỚC `validateForm()`.
- [x] **BE** `BillPaymentStoreRequest` (Update kế thừa) + closure `approveNotOverRequestRule()` cho
      `details.*.payment_money_approve`, chỉ ở nhánh A. Viết bằng closure, KHÔNG dùng
      `lte:details.*.payment_money_request` (luật đó ném `InvalidArgumentException` -> **500** khi
      trường đem so vắng mặt; đây là ô CHỈ ĐỌC do FE kéo từ đề nghị). Vế so thiếu / <= 0 -> bỏ qua.

🚨 **BE đường DUYỆT: CỐ Ý KHÔNG thêm luật** — đã có sẵn
`BillPaymentApprovalFlowService::guardPaymentMoneyCeiling()` chặn bằng 422 *"Số tiền chi không được
vượt quá số dư!"*, và guard đó so bằng **`abs()` cho nhánh B** vì `payment_money_request` của loại 4
là SỐ DƯ CÓ DẤU (âm = nhân viên nợ lại công ty). Bản nháp của đợt này có thêm luật `>` đơn giản vào
`BillPaymentApproveRequest` rồi **gỡ ra**: khai lại ở tầng FormRequest là chặn oan 48/1.021 dòng thật
có số dư âm — đúng cái bẫy docblock của file đó đã ghi sẵn. File chỉ còn thêm 1 khối chú thích.

**Verify (tinker, dựng `Validator` thật từ `BillPaymentStoreRequest`):**
vượt 200>100 -> *"Không được lớn hơn số tiền đề nghị chi"* · bằng -> không lỗi · thiếu
`payment_money_request` -> không lỗi (không nổ 500) · **lưu nháp mà vượt** -> có lỗi ·
**loại 4 (nhánh B)** -> KHÔNG áp luật (đúng thiết kế, trần của nhánh đó nằm ở service).
`php -l` sạch 2 file BE · template parse sạch 2 file FE, hàm mới nằm đúng trong `methods`, không
trùng tên, hết `:max`. ⚠️ Chưa mở trình duyệt.

📌 6 ô khoản chi nhánh B (`PaymentEmployeeTable::clampToLimit()` + `onEmployeeAmountInput()` trong
popup duyệt) VẪN kẹp cứng — luật của chúng có thêm ràng buộc CÙNG DẤU, chưa đụng, chờ user yêu cầu.

### Checkpoint — 2026-08-28
Vừa hoàn thành: ô Số tiền chi (màn tạo/sửa) và Số tiền thực chi (popup duyệt) cho gõ vượt, báo đỏ
dưới ô và chặn lưu/duyệt; BE chặn thêm ở đường lưu (đường duyệt vốn đã có guard).
Đang làm dở: không.
Bước tiếp theo: user gõ số vượt ở cả 2 chỗ, xác nhận thấy chữ đỏ và nút không gọi API.
Blocked: không.


## Phase L — Lịch sử thay đổi phiếu chi (user yêu cầu 2026-09-03)

User: *"bổ sung lịch sử thay đổi màn phiếu chi luôn cho tôi"* — làm ngay sau màn Phiếu thu tiền,
**cùng phạm vi đã chốt ở đó**: Tạo mới · Thay đổi thông tin · Bảng chi tiết theo TỪNG DÒNG · Duyệt
(kèm số duyệt chi) · Hủy (kèm lý do) · Xóa. Trạng thái luôn đi DÒNG RIÊNG (skill §3a).

### Hiện trạng trước khi làm

`bill_payments` ĐÃ có trong whitelist `CatalogHistoryService::TABLES` nhưng **chỉ 1 cột `status`**:
mới log đổi trạng thái (`BillPayment::logStatusHistory()` gọi từ `submit()` / `approve()` /
`cancel()`). FE **chưa có gì** — không popup ở danh sách, không khối ở chi tiết.

⚠️ **RÀNG BUỘC KHÔNG ĐƯỢC PHÁ**: `BillPaymentDetailResource` ĐỌC NGƯỢC `catalog_histories` để dựng
`cancel_reason` / `cancel_note` / `approve_note` (bảng `bill_payments` KHÔNG có cột `note`). Nó lọc
`action = 'change_status'` rồi so `new_value['Trạng thái']` với TÊN trạng thái. Vì vậy:
- giữ nguyên cách `logStatusHistory()` ghi (khóa nhãn `'Trạng thái'` + khóa phụ `'Ghi chú'`);
- log nội dung mới dùng action `update` nên KHÔNG lọt vào bộ lọc đó;
- giữ `'status' => 'Trạng thái'` trong whitelist để 2 dòng log THẬT đang có (id 213, 216) vẫn đọc đúng.

### BE

- [x] `CatalogHistoryService::TABLES['bill_payments']` — mở rộng từ 1 cột lên đủ cột phẳng + 2 khoá
      ẢO dạng BẢNG (`details_rows`, `export_request_rows`), GIỮ `status`
- [x] `Modules/Finance/Services/BillPaymentHistoryService.php` — khuôn `BillIncomeHistoryService`:
      · `catalogColumns()` KHÔNG chứa `status` (đã có dòng riêng từ `logStatusHistory()`)
      · dòng chi tiết đọc cột DENORMALIZED (`customer_name` / `supplier_name` / `employee_name` /
        `contract_code`) — không join, log tự chứa sẵn
      · 6 khoản thu nhập nhân viên (nhánh B) chỉ ghi khi KHÁC 0, tránh phiếu nhánh A dài vô ích
      · `__key` = khoá TỰ NHIÊN (TK nợ | KH | NCC | NV | hợp đồng) vì `syncDetails()` xoá-tạo-lại
- [x] `BillPaymentWriteService::store()` → `logCreate()` (sau `syncDetails()`)
- [x] `BillPaymentWriteService::update()` → snapshot ở ĐẦU transaction, `logUpdate()` sau `syncDetails()`
- [x] `BillPaymentWriteService::destroy()` → snapshot TRƯỚC khi xoá dòng con, `logDelete()`
- [x] `BillPaymentApprovalFlowService::approve()` nhánh Thủ quỹ → snapshot trước
      `applyApprovedMoney()`, `logUpdate()` sau khi lưu (Số duyệt chi từng dòng + Ngày hạch toán +
      2 cột tổng). Dòng trạng thái GIỮ NGUYÊN `logStatusHistory()` đang có — không ghi trùng.
- [x] Nhánh Kế toán trưởng duyệt (5→2) và `submit()` / `cancel()`: KHÔNG thêm log nội dung,
      chúng chỉ đổi trạng thái (+`accounting_approved_id` không theo dõi)

### FE — ĐỦ 2 NƠI (§5.1)

- [x] `pages/finance/bill-payments/index.vue` — mục `Lịch sử` + `CatalogHistoryModal`
- [x] `pages/finance/bill-payments/_id/index.vue` — khối `SystemInfoSection` trong thân trang

### Verify

- [x] tinker trong transaction rồi ROLLBACK: tạo/sửa/gửi duyệt/duyệt/hủy/xóa → đúng số dòng, đúng nhóm
- [x] Đọc lại `cancel_reason` / `approve_note` của `BillPaymentDetailResource` — KHÔNG được đổi giá trị
- [x] 2 dòng log thật id 213/216 vẫn đọc ra đúng như trước khi sửa whitelist
- [x] Compile FE + Playwright 2 màn

### Kiểm chứng đã chạy

**Không hồi quy** (điểm rủi ro số 1 của màn này): chụp baseline `getLogs()` + 3 khóa
`cancel_reason` / `cancel_note` / `approve_note` của `BillPaymentDetailResource` cho 2 dòng log THẬT
(id 213 phiếu 1360, id 216 phiếu 1357) TRƯỚC khi sửa whitelist, so lại SAU khi sửa → **diff rỗng**.

**Luồng đầy đủ** (tinker, toàn bộ trong transaction rồi ROLLBACK; `BillPaymentNotifyService` được
thay bằng bản no-op vì notify publish Redis NGOÀI transaction, rollback không gỡ được):
tạo → 1 dòng `create` · sửa người nhận + lý do chi + số duyệt chi dòng 1 + thêm dòng 2 → **1 dòng**
`update` đúng 4 trường phẳng + 1 dòng thêm + 1 dòng sửa ĐÚNG CỘT · lưu lại y nguyên → **không sinh
log rác** · gửi duyệt → **đúng 1 dòng `change_status`, KHÔNG có dòng `update` thừa** · duyệt →
**2 dòng** (`update`: Ngày hạch toán + 2 cột tổng + Số tiền chi từng dòng · `change_status` kèm ghi
chú Thủ quỹ) · hủy → `change_status` mang cả lý do (`note`) lẫn khóa `Ghi chú` · xóa → snapshot +
2 dòng chi tiết đã xóa. `approve_note` / `cancel_reason` đọc lại vẫn đúng sau mỗi bước.

**Trình duyệt (Playwright)**: gieo 2 dòng log nội dung cho phiếu THẬT `TPE.PC0826.00006` (id 1358)
rồi xem giao diện, xong xoá đúng 2 dòng đó (id 278/279) — 2 dòng log thật 213/216 GIỮ NGUYÊN, phiếu
1358 giữ `updated_at = 2026-08-27 23:52:30`, 1 dòng chi tiết.
- Màn danh sách: dòng còn nhiều hành động thì "Lịch sử" nằm trong menu ⋮ cạnh "Duyệt"; dòng ít hành
  động thì hiện thẳng icon `ri-history-line`.
- Popup: timeline mới → cũ, cũ ĐỎ / mới XANH, nhóm "Bảng chi tiết thêm mới / sửa thông tin".
  Phiếu ngoại tệ (EURO) hiện thêm cột "(VND)" — đúng logic `exchangeText()`.
- Màn chi tiết: khối "Lịch sử" badge `2` trong THÂN TRANG, `V2Footer` vẫn nguyên bộ nút
  (Duyệt phiếu chi / Hủy phiếu chi / In / Xuất Excel / Quay lại). Form phía trên không vỡ vì thêm slot.
- Console: **0 lỗi** ở cả 2 màn.

`php -l` sạch 4 file BE · compile FE (vue-template-compiler + babel) sạch 3 file.

### Sửa kèm — áp cho CẢ màn Phiếu thu

Log "Xóa" in ra dòng vô nghĩa `<Nhãn>: (trống) → (trống)` cho mọi cột đang rỗng (phiếu chi nhánh A
không có "Phòng ban được chi" nên dính ngay). `forFullLog()` của **cả 2** service
(`BillIncomeHistoryService` + `BillPaymentHistoryService`) nay lọc bỏ cả `null` / `''` chứ không chỉ
mảng rỗng.

### Checkpoint — 2026-09-03
Vừa hoàn thành: lịch sử thay đổi màn Phiếu chi tiền — nâng từ "chỉ trạng thái" lên ĐẦY ĐỦ, BE
(whitelist + service ghi log + 4 điểm nối) và FE (popup ở danh sách + khối Lịch sử ở chi tiết).
Đang làm dở: không.
Bước tiếp theo: user nghiệm thu.
Blocked: không.
